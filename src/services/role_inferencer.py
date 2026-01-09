"""Role inference service for job role recommender"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

from ..models.role_recommendation import RoleRecommendation, RecommendedRole
from ..models.profile_signals import ProfileSignals
from ..services.knowledge_base import get_role_archetype_loader
from ..utils.constants import (
    MIN_ROLES_PER_INDUSTRY, MAX_ROLES_PER_INDUSTRY,
    ROLE_INFERENCE_TIMEOUT, CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, CONFIDENCE_LOW
)


class RoleInferencer:
    """Inferences relevant roles based on profile signals and industry selection"""

    def __init__(self):
        self.knowledge_base = get_role_archetype_loader()
        self.logger = logging.getLogger(__name__)

    async def infer_roles(
        self,
        profile_signals: ProfileSignals,
        industries: List[str],
        max_roles: int = MAX_ROLES_PER_INDUSTRY,
        timeout: int = ROLE_INFERENCE_TIMEOUT
    ) -> RoleRecommendation:
        """
        Infer relevant roles based on profile signals and target industries.

        Args:
            profile_signals: Aggregated signals from resume and profile analysis
            industries: List of target industries to search for roles
            max_roles: Maximum number of roles to recommend per industry
            timeout: Timeout for role inference in seconds

        Returns:
            RoleRecommendation: Recommended roles with justifications
        """
        start_time = time.time()
        self.logger.info(f"Starting role inference for {len(industries)} industries with {len(profile_signals.aggregated_skills)} skills")

        try:
            # Load archetypes for the specified industries
            self.knowledge_base.load_archetypes()

            all_recommended_roles = []
            confidence_factors = []

            for industry in industries:
                self.logger.debug(f"Processing industry: {industry}")
                # Load archetypes specifically for this industry
                industry_archetypes = await self._load_industry_archetypes(industry)

                if not industry_archetypes:
                    self.logger.warning(f"No archetypes found for industry: {industry}")
                    continue

                self.logger.debug(f"Found {len(industry_archetypes)} archetypes for industry: {industry}")

                # Score each archetype against the profile signals
                scored_archetypes = []
                for archetype in industry_archetypes:
                    try:
                        self.logger.debug(f"Scoring archetype: {archetype.title}")
                        score, justification = self._score_archetype_vs_profile(archetype, profile_signals)
                        scored_archetypes.append((archetype, score, justification))
                    except Exception as e:
                        self.logger.error(f"Error scoring archetype {archetype.title}: {e}")
                        continue  # Skip this archetype and continue with others

                # Sort by score (descending)
                scored_archetypes.sort(key=lambda x: x[1], reverse=True)

                # Take top roles up to max_roles
                top_archetypes = scored_archetypes[:max_roles]

                # Create RecommendedRole objects
                for archetype, score, justification in top_archetypes:
                    if time.time() - start_time > timeout:
                        self.logger.warning(f"Role inference timed out after {timeout} seconds")
                        break

                    # Determine seniority level based on experience and skills
                    seniority_level = self._infer_seniority_level(profile_signals, archetype)

                    # Create confidence factors
                    confidence_factors.extend(self._generate_confidence_factors(
                        profile_signals, archetype, score
                    ))

                    # Create RecommendedRole
                    recommended_role = RecommendedRole(
                        role_id=f"{archetype.title.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}",
                        title=archetype.title,
                        industry=archetype.industry,
                        seniority_level=seniority_level,
                        fit_score=score,
                        justification=justification,
                        confidence_factors=confidence_factors,
                        skill_gaps=self._identify_skill_gaps(profile_signals, archetype),
                        improvement_suggestions=self._generate_improvement_suggestions(
                            profile_signals, archetype
                        )
                    )

                    all_recommended_roles.append(recommended_role)

            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(
                all_recommended_roles, profile_signals
            )

            self.logger.info(f"Generated {len(all_recommended_roles)} role recommendations with overall confidence {overall_confidence:.2f}")

            # Create RoleRecommendation object
            recommendation = RoleRecommendation(
                recommendation_id=f"rec_{profile_signals.signals_id}",
                session_id=profile_signals.signals_id,
                roles=all_recommended_roles,
                overall_confidence=overall_confidence,
                confidence_factors=confidence_factors,
                recommendation_timestamp=datetime.now(),
                industry=industries[0] if industries else "General"  # Using first industry as default
            )

            return recommendation

        except Exception as e:
            self.logger.error(f"Error during role inference: {e}")
            # Return a fallback recommendation with minimal data
            fallback_recommendation = RoleRecommendation(
                recommendation_id=f"rec_{profile_signals.signals_id}_fallback",
                session_id=profile_signals.signals_id,
                roles=[],
                overall_confidence=0.0,
                confidence_factors=["Error occurred during role inference"],
                recommendation_timestamp=datetime.now(),
                industry="General"
            )
            return fallback_recommendation

    async def _load_industry_archetypes(self, industry: str) -> List['RoleArchetype']:
        """
        Load role archetypes specifically constrained to an industry.

        Args:
            industry: The target industry

        Returns:
            List of RoleArchetype objects for the industry
        """
        # Use the knowledge base to get archetypes for the specific industry
        industry_archetypes = self.knowledge_base.get_archetypes_by_industry(industry)

        # Log the number of archetypes found
        self.logger.info(f"Loaded {len(industry_archetypes)} archetypes for industry: {industry}")

        return industry_archetypes

    def _score_archetype_vs_profile(
        self,
        archetype: 'RoleArchetype',
        profile_signals: ProfileSignals
    ) -> tuple[float, Dict[str, str]]:
        """
        Score how well an archetype matches the profile signals.

        Args:
            archetype: The role archetype to score
            profile_signals: The profile signals to match against

        Returns:
            Tuple of (score, justification)
        """
        # Get profile data
        resume_signals = profile_signals.resume_signals
        profile_signals_data = profile_signals.profile_signals
        aggregated_skills = profile_signals.aggregated_skills
        experience_summary = profile_signals.experience_summary

        # Initialize scoring components
        skill_alignment_score = 0.0
        experience_alignment_score = 0.0
        project_relevance_score = 0.0
        technology_match_score = 0.0

        # Calculate skill alignment score
        required_skills = set(s.lower() for s in archetype.required_skills)
        preferred_skills = set(s.lower() for s in archetype.preferred_skills)
        profile_skills = set(s.lower() for s in aggregated_skills)

        # Count matched required skills
        matched_required = required_skills.intersection(profile_skills)
        required_match_ratio = len(matched_required) / len(required_skills) if required_skills else 1.0

        # Count matched preferred skills
        matched_preferred = preferred_skills.intersection(profile_skills)
        preferred_match_ratio = len(matched_preferred) / len(preferred_skills) if preferred_skills else 1.0

        # Weighted skill score
        skill_alignment_score = (required_match_ratio * 0.7) + (preferred_match_ratio * 0.3)

        # Calculate experience alignment score
        experience_years = experience_summary.get('total_years', 0.0)
        experience_domains = experience_summary.get('domains', [])

        # Determine expected experience range based on archetype requirements
        expected_min_years = self._extract_min_experience_from_archetype(archetype)
        expected_max_years = expected_min_years + 5  # Assume 5 years range

        # Score based on experience match
        if expected_min_years <= experience_years <= expected_max_years:
            experience_alignment_score = 1.0
        elif experience_years < expected_min_years:
            # Under-experienced - reduce score proportionally
            experience_alignment_score = max(0.0, experience_years / expected_min_years if expected_min_years > 0 else 1.0)
        else:
            # Over-experienced - still a good match
            experience_alignment_score = min(1.0, 0.8 + (min(2.0, experience_years - expected_max_years) * 0.1))

        # Calculate project relevance score
        project_highlights = profile_signals.project_highlights
        project_relevance_score = self._calculate_project_relevance(
            project_highlights, archetype
        )

        # Calculate technology match score
        archetype_techs = set(t.lower() for t in archetype.technologies)
        tech_match_ratio = len(archetype_techs.intersection(profile_skills)) / len(archetype_techs) if archetype_techs else 1.0
        technology_match_score = tech_match_ratio

        # Weighted overall score
        total_score = (
            skill_alignment_score * 0.4 +
            experience_alignment_score * 0.3 +
            project_relevance_score * 0.2 +
            technology_match_score * 0.1
        )

        # Generate structured justification using prompting
        justification = self._generate_structured_justification(
            archetype, profile_signals, skill_alignment_score,
            project_relevance_score, technology_match_score,
            experience_alignment_score, required_match_ratio
        )

        # Add detailed justification generation
        detailed_justification = self._generate_detailed_justification(
            archetype, profile_signals, justification
        )

        return min(total_score, 1.0), detailed_justification

    def _generate_structured_justification(
        self,
        archetype: 'RoleArchetype',
        profile_signals: ProfileSignals,
        skill_alignment_score: float,
        project_relevance_score: float,
        technology_match_score: float,
        experience_alignment_score: float,
        required_match_ratio: float
    ) -> Dict[str, str]:
        """
        Generate structured justification using prompting approach.
        This creates a clear, understandable explanation for why a role fits.
        """
        # Get profile data
        aggregated_skills = profile_signals.aggregated_skills
        experience_summary = profile_signals.experience_summary
        project_highlights = profile_signals.project_highlights

        # Calculate experience years
        experience_years = experience_summary.get('total_years', 0.0)

        # Determine expected experience range
        expected_min_years = self._extract_min_experience_from_archetype(archetype)

        # Get matched required skills
        required_skills = set(s.lower() for s in archetype.required_skills)
        profile_skills = set(s.lower() for s in aggregated_skills)
        matched_required = required_skills.intersection(profile_skills)

        # Generate structured justification
        justification = {
            'skill_alignment': self._format_skill_alignment_justification(
                skill_alignment_score, matched_required, archetype.required_skills
            ),
            'project_relevance': self._format_project_relevance_justification(
                project_relevance_score, project_highlights, archetype
            ),
            'technology_match': self._format_technology_match_justification(
                technology_match_score, profile_skills, archetype.technologies
            ),
            'experience_alignment': self._format_experience_alignment_justification(
                experience_alignment_score, experience_years, expected_min_years
            )
        }

        return justification

    def _format_skill_alignment_justification(
        self,
        score: float,
        matched_skills: set,
        required_skills: List[str]
    ) -> str:
        """Format the skill alignment justification."""
        match_percentage = int(score * 100)
        matched_list = list(matched_skills)[:3]  # Limit to top 3 matches

        if matched_list:
            return (f"Skill alignment is {match_percentage}% based on matching "
                   f"{len(matched_list)} of {len(required_skills)} required skills: "
                   f"{', '.join(matched_list[:3])}")
        else:
            return f"Skill alignment is {match_percentage}% with limited matching skills"

    def _format_project_relevance_justification(
        self,
        score: float,
        project_highlights: List[Dict[str, Any]],
        archetype: 'RoleArchetype'
    ) -> str:
        """Format the project relevance justification."""
        match_percentage = int(score * 100)

        if project_highlights:
            return f"Project relevance is {match_percentage}% based on alignment with role responsibilities and technologies"
        else:
            return f"Project relevance is {match_percentage}% but no project examples provided"

    def _format_technology_match_justification(
        self,
        score: float,
        profile_skills: set,
        archetype_techs: List[str]
    ) -> str:
        """Format the technology match justification."""
        match_percentage = int(score * 100)
        matched_techs = list(profile_skills.intersection(set(t.lower() for t in archetype_techs)))[:3]

        if matched_techs:
            return (f"Technology match is {match_percentage}% based on matching technologies: "
                   f"{', '.join(matched_techs[:3])}")
        else:
            return f"Technology match is {match_percentage}% with limited technology alignment"

    def _format_experience_alignment_justification(
        self,
        score: float,
        experience_years: float,
        expected_min_years: float
    ) -> str:
        """Format the experience alignment justification."""
        match_percentage = int(score * 100)

        return (f"Experience alignment is {match_percentage}% with {experience_years} years of experience "
               f"compared to expected ~{expected_min_years} years for this role")

    def _generate_detailed_justification(
        self,
        archetype: 'RoleArchetype',
        profile_signals: ProfileSignals,
        basic_justification: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Generate detailed justification with skill alignment, project relevance,
        technology match, and experience alignment.
        """
        # Get profile data
        aggregated_skills = profile_signals.aggregated_skills
        project_highlights = profile_signals.project_highlights
        experience_summary = profile_signals.experience_summary

        # Enhance the basic justification with more details
        detailed_justification = basic_justification.copy()

        # Enhance skill alignment with specific examples
        required_skills = set(s.lower() for s in archetype.required_skills)
        profile_skills = set(s.lower() for s in aggregated_skills)
        matched_required = required_skills.intersection(profile_skills)

        if matched_required:
            detailed_justification['skill_alignment'] += (
                f". Specific matched skills: {', '.join(list(matched_required)[:3])}."
            )

        # Enhance project relevance with specific examples
        relevant_projects = []
        for project in project_highlights:
            project_techs = set(t.lower() for t in project.get('technologies', []))
            archetype_techs = set(t.lower() for t in archetype.technologies)
            if project_techs.intersection(archetype_techs):
                relevant_projects.append(project.get('name', 'Unnamed project'))

        if relevant_projects:
            detailed_justification['project_relevance'] += (
                f" Relevant projects: {', '.join(relevant_projects[:2])}."
            )

        # Enhance technology match with specific examples
        archetype_techs = set(t.lower() for t in archetype.technologies)
        matched_techs = list(archetype_techs.intersection(profile_skills))[:3]
        if matched_techs:
            detailed_justification['technology_match'] += (
                f" Specific matched technologies: {', '.join(matched_techs)}."
            )

        # Enhance experience alignment with domain alignment
        experience_domains = experience_summary.get('domains', [])
        archetype_domains = [archetype.industry]  # Simplified - in reality this could be more complex
        domain_alignment = len(set(experience_domains).intersection(set(archetype_domains)))

        if domain_alignment > 0:
            detailed_justification['experience_alignment'] += (
                f" Domain alignment in {archetype.industry}."
            )

        # Add seniority-specific justification
        from .seniority_detector import get_seniority_detector
        seniority_detector = get_seniority_detector()
        seniority_info = seniority_detector.detect_seniority_with_context(
            profile_signals, archetype.title, archetype.industry
        )

        detailed_justification['seniority_alignment'] = (
            f"Seniority level {seniority_info['seniority_level']} with confidence "
            f"{seniority_info['confidence_score']:.2f}. Reasoning: "
            f"{'; '.join(seniority_info['reasoning'][:2])}"
        )

        # Add conflict detection and explanation
        conflict_explanation = self._detect_and_explain_conflicts(
            archetype, profile_signals, aggregated_skills
        )

        if conflict_explanation:
            detailed_justification['conflict_explanation'] = conflict_explanation

        return detailed_justification

    def _detect_and_explain_conflicts(
        self,
        archetype: 'RoleArchetype',
        profile_signals: ProfileSignals,
        profile_skills: List[str]
    ) -> Optional[str]:
        """
        Detect conflicting signals in the profile that might suggest multiple role paths.

        Args:
            archetype: The role archetype being evaluated
            profile_signals: Profile signals to analyze for conflicts
            profile_skills: List of profile skills

        Returns:
            String explanation of conflicts if detected, None otherwise
        """
        conflicts = []

        # Check for conflicting technology stacks (e.g., frontend vs backend focus)
        frontend_techs = {'javascript', 'react', 'vue', 'angular', 'html', 'css', 'sass', 'scss'}
        backend_techs = {'python', 'java', 'node.js', 'php', 'ruby', 'go', 'rust', 'database', 'sql', 'api'}
        ml_ds_techs = {'python', 'r', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn', 'jupyter'}

        profile_tech_set = set(skill.lower() for skill in profile_skills)

        frontend_matches = profile_tech_set.intersection(frontend_techs)
        backend_matches = profile_tech_set.intersection(backend_techs)
        ml_ds_matches = profile_tech_set.intersection(ml_ds_techs)

        # Detect if profile shows strong signals in multiple different areas
        strong_areas = 0
        if len(frontend_matches) >= 3:
            strong_areas += 1
        if len(backend_matches) >= 3:
            strong_areas += 1
        if len(ml_ds_matches) >= 3 and 'python' not in ml_ds_matches:  # Avoid counting python twice
            strong_areas += 1

        if strong_areas > 1:
            conflicts.append(
                f"Profile shows strong skills in {strong_areas} different technical areas "
                f"(frontend: {len(frontend_matches)}, backend: {len(backend_matches)}, ML/DS: {len(ml_ds_matches)}), "
                f"suggesting potential for multiple role paths."
            )

        # Check for conflicting experience levels
        experience_summary = profile_signals.experience_summary
        experience_years = experience_summary.get('total_years', 0)
        leadership_indicators = experience_summary.get('leadership_indicators', [])

        # If someone has many years of experience but few leadership indicators, there might be a mismatch
        if experience_years >= 5 and len(leadership_indicators) == 0:
            conflicts.append(
                f"Profile has {experience_years} years of experience but limited leadership indicators, "
                f"which may suggest a specialist vs leadership role path."
            )

        # Check for conflicting domain experience
        experience_domains = experience_summary.get('domains', [])
        if len(experience_domains) > 3:
            conflicts.append(
                f"Profile spans {len(experience_domains)} different domains ({', '.join(experience_domains[:3])}), "
                f"indicating diverse experience that could lead to multiple role specializations."
            )

        # Check for conflicting role signals in project descriptions
        project_highlights = profile_signals.project_highlights
        role_signals = {'management', 'technical', 'design', 'research', 'business'}
        detected_signals = set()

        for project in project_highlights:
            description = project.get('description', '').lower()
            for signal in role_signals:
                if signal in description:
                    detected_signals.add(signal)

        if len(detected_signals) > 2:
            conflicts.append(
                f"Projects indicate involvement in multiple role types ({', '.join(detected_signals)}), "
                f"suggesting versatility but also potential for multiple career paths."
            )

        if conflicts:
            return " | ".join(conflicts)

        return None

    def _generate_alternative_role_paths(
        self,
        profile_signals: ProfileSignals,
        current_archetype: 'RoleArchetype',
        all_matching_archetypes: List['RoleArchetype']
    ) -> List[Dict[str, Any]]:
        """
        Generate alternative role paths based on conflicting signals in the profile.

        Args:
            profile_signals: Profile signals to analyze
            current_archetype: Current archetype being recommended
            all_matching_archetypes: All archetypes that match the profile

        Returns:
            List of dictionaries representing alternative role paths
        """
        alternative_paths = []

        # Look for archetypes that represent different career directions
        current_domain = current_archetype.industry.lower()

        for archetype in all_matching_archetypes:
            if archetype.title != current_archetype.title:
                # Calculate how different this path is from the current recommendation
                domain_diff = archetype.industry.lower() != current_domain
                skill_diff = len(set(archetype.required_skills) - set(current_archetype.required_skills))

                if domain_diff or skill_diff > 2:
                    alternative_paths.append({
                        'title': archetype.title,
                        'industry': archetype.industry,
                        'similarity': 1.0 / (1 + skill_diff),  # Lower similarity for more different roles
                        'reasoning': f"This role represents a {'different industry' if domain_diff else 'different skill focus'} path."
                    })

        # Sort by similarity (to show most related alternatives first)
        alternative_paths.sort(key=lambda x: x['similarity'], reverse=True)

        return alternative_paths[:2]  # Return top 2 alternatives

    def _generate_justification_summary(self, justification: Dict[str, str]) -> str:
        """
        Generate a brief justification summary (1-2 sentence overview).

        Args:
            justification: Detailed justification dictionary

        Returns:
            str: Brief justification summary
        """
        summary_parts = []

        # Extract key information from justification
        if 'skill_alignment' in justification:
            # Extract the percentage and key skills from skill alignment
            skill_text = justification['skill_alignment']
            summary_parts.append(f"Strong skill alignment based on relevant experience.")

        if 'experience_alignment' in justification:
            exp_text = justification['experience_alignment']
            summary_parts.append(f"Good experience match for the role requirements.")

        # Create a concise summary
        if len(summary_parts) >= 2:
            return f"{summary_parts[0]} {summary_parts[1]}"
        elif summary_parts:
            return summary_parts[0]
        else:
            return "Good overall alignment with the role requirements."

    def _extract_min_experience_from_archetype(self, archetype: 'RoleArchetype') -> float:
        """Extract minimum required experience from archetype requirements."""
        # In a real implementation, this would parse the archetype's seniority requirements
        # For now, we'll use a simple heuristic based on the seniority level in the title
        title_lower = archetype.title.lower()

        if any(level in title_lower for level in ['junior', 'entry', 'associate']):
            return 0.0
        elif any(level in title_lower for level in ['senior', 'lead', 'principal', 'architect']):
            return 5.0
        else:
            # Mid-level default
            return 2.0

    def _calculate_project_relevance(
        self,
        project_highlights: List[Dict[str, Any]],
        archetype: 'RoleArchetype'
    ) -> float:
        """Calculate how relevant the user's projects are to the archetype."""
        if not project_highlights:
            return 0.0

        relevant_projects = 0
        total_projects = len(project_highlights)

        archetype_techs = set(t.lower() for t in archetype.technologies)
        archetype_responsibilities = ' '.join(archetype.responsibilities).lower()

        for project in project_highlights:
            project_techs = set(t.lower() for t in project.get('technologies', []))
            project_description = project.get('description', '').lower()

            # Check if project techs match archetype techs
            tech_match = len(project_techs.intersection(archetype_techs)) > 0

            # Check if project description matches archetype responsibilities
            responsibility_match = any(resp.lower() in project_description for resp in archetype.responsibilities)

            if tech_match or responsibility_match:
                relevant_projects += 1

        return relevant_projects / total_projects if total_projects > 0 else 0.0

    def _infer_seniority_level(
        self,
        profile_signals: ProfileSignals,
        archetype: 'RoleArchetype'
    ) -> str:
        """Infer the appropriate seniority level based on profile data."""
        experience_summary = profile_signals.experience_summary
        experience_years = experience_summary.get('total_years', 0.0)
        leadership_indicators = experience_summary.get('leadership_indicators', [])

        # Determine seniority based on experience and leadership indicators
        if experience_years >= 6 or len(leadership_indicators) >= 2:
            return 'SENIOR'
        elif experience_years >= 3 or len(leadership_indicators) >= 1:
            return 'MID'
        else:
            return 'JUNIOR'

    def _generate_confidence_factors(
        self,
        profile_signals: ProfileSignals,
        archetype: 'RoleArchetype',
        score: float
    ) -> List[str]:
        """Generate factors that contribute to the confidence in the recommendation."""
        factors = []

        if score >= CONFIDENCE_HIGH:
            factors.append("Strong skill alignment")
        elif score >= CONFIDENCE_MEDIUM:
            factors.append("Moderate skill alignment")
        else:
            factors.append("Limited skill alignment")

        # Check if there's good project alignment
        project_relevance = self._calculate_project_relevance(
            profile_signals.project_highlights, archetype
        )
        if project_relevance >= 0.7:
            factors.append("Strong project experience alignment")

        # Check technology match
        archetype_techs = set(t.lower() for t in archetype.technologies)
        profile_skills = set(s.lower() for s in profile_signals.aggregated_skills)
        tech_match_ratio = len(archetype_techs.intersection(profile_skills)) / len(archetype_techs) if archetype_techs else 1.0

        if tech_match_ratio >= 0.7:
            factors.append("Good technology stack match")

        return factors

    def _identify_skill_gaps(
        self,
        profile_signals: ProfileSignals,
        archetype: 'RoleArchetype'
    ) -> List[str]:
        """Identify skills that the user lacks for the target role."""
        required_skills = set(s.lower() for s in archetype.required_skills)
        preferred_skills = set(s.lower() for s in archetype.preferred_skills)
        profile_skills = set(s.lower() for s in profile_signals.aggregated_skills)

        missing_required = required_skills - profile_skills
        missing_preferred = preferred_skills - profile_skills

        # Combine and limit to top gaps
        all_gaps = list(missing_required) + list(missing_preferred)

        # Return the most critical gaps (required first, then preferred)
        return [skill.title() for skill in list(missing_required)[:3] + list(missing_preferred)[:3]]

    def _generate_improvement_suggestions(
        self,
        profile_signals: ProfileSignals,
        archetype: 'RoleArchetype'
    ) -> List[str]:
        """Generate improvement suggestions based on skill gaps."""
        suggestions = []
        skill_gaps = self._identify_skill_gaps(profile_signals, archetype)

        for gap in skill_gaps[:2]:  # Limit to top 2 suggestions
            suggestions.append(f"Learn {gap} to better align with {archetype.title} requirements")

        # Add project-related suggestion if applicable
        if not profile_signals.project_highlights:
            suggestions.append("Add project examples to your portfolio that demonstrate relevant skills")

        return suggestions

    def _calculate_overall_confidence(
        self,
        recommended_roles: List[RecommendedRole],
        profile_signals: ProfileSignals
    ) -> float:
        """Calculate overall confidence in the recommendations."""
        if not recommended_roles:
            return 0.0

        # Average of role fit scores
        avg_fit_score = sum(role.fit_score for role in recommended_roles) / len(recommended_roles)

        # Factor in profile completeness
        profile_completeness = self._estimate_profile_completeness(profile_signals)

        # Weighted confidence (70% fit score, 30% profile completeness)
        overall_confidence = (avg_fit_score * 0.7) + (profile_completeness * 0.3)

        return min(overall_confidence, 1.0)

    def _estimate_profile_completeness(
        self,
        profile_signals: ProfileSignals
    ) -> float:
        """Estimate how complete the profile data is."""
        completeness_score = 0.0
        total_factors = 4  # Number of completeness factors we'll check

        # Check if resume signals exist
        if profile_signals.resume_signals:
            completeness_score += 0.25

        # Check if profile signals exist
        if profile_signals.profile_signals:
            completeness_score += 0.25

        # Check if skills are populated
        if profile_signals.aggregated_skills:
            completeness_score += 0.25

        # Check if project highlights exist
        if profile_signals.project_highlights:
            completeness_score += 0.25

        return completeness_score

    def _handle_minimal_profile_data(
        self,
        profile_signals: ProfileSignals,
        industries: List[str]
    ) -> RoleRecommendation:
        """
        Handle cases where profile data is minimal, providing best-effort recommendations with low confidence.

        Args:
            profile_signals: The minimal profile signals
            industries: List of target industries

        Returns:
            RoleRecommendation: Recommendations with appropriate low confidence
        """
        self.logger.info("Handling minimal profile data scenario")

        # Create fallback recommendations based on industry defaults
        fallback_roles = []

        for industry in industries[:2]:  # Limit to first 2 industries to avoid too many recommendations
            # Create generic roles for the industry based on common archetypes
            generic_role_titles = [
                f"Entry Level {industry.split()[-1]} Position",
                f"Junior {industry.split()[0]} Role" if len(industry.split()) > 0 else f"Junior {industry} Role"
            ]

            for title in generic_role_titles:
                fallback_role = RecommendedRole(
                    role_id=f"fallback_{title.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}",
                    title=title,
                    industry=industry,
                    seniority_level="JUNIOR",  # Default to junior for minimal data
                    fit_score=0.2,  # Low confidence score for minimal data
                    justification={
                        'skill_alignment': "Limited skills provided, general alignment with industry",
                        'project_relevance': "No project data provided",
                        'technology_match': "Limited technology data available",
                        'experience_alignment': "Minimal experience data provided"
                    },
                    confidence_factors=["Minimal profile data provided", "Limited skill information"],
                    skill_gaps=["Additional skills", "More project experience", "Detailed experience"],
                    improvement_suggestions=[
                        "Add more skills to your profile",
                        "Include project examples",
                        "Provide more detailed experience information"
                    ]
                )
                fallback_roles.append(fallback_role)

        # Create a fallback recommendation with low confidence
        fallback_recommendation = RoleRecommendation(
            recommendation_id=f"fallback_rec_{profile_signals.signals_id}",
            session_id=profile_signals.signals_id,
            roles=fallback_roles,
            overall_confidence=0.2,  # Low confidence for minimal data
            confidence_factors=[
                "Minimal profile data provided",
                "Recommendations are generic and may not match specific skills",
                "More complete profiles will yield better recommendations"
            ],
            recommendation_timestamp=datetime.now(),
            industry=industries[0] if industries else "General"
        )

        self.logger.info(f"Created {len(fallback_roles)} fallback recommendations for minimal data")
        return fallback_recommendation

    def infer_roles_with_graceful_degradation(
        self,
        profile_signals: ProfileSignals,
        industries: List[str],
        max_roles: int = MAX_ROLES_PER_INDUSTRY,
        timeout: int = ROLE_INFERENCE_TIMEOUT
    ) -> RoleRecommendation:
        """
        Infer roles with graceful degradation for minimal profile data.

        Args:
            profile_signals: Aggregated signals from resume and profile analysis
            industries: List of target industries to search for roles
            max_roles: Maximum number of roles to recommend per industry
            timeout: Timeout for role inference in seconds

        Returns:
            RoleRecommendation: Recommended roles with graceful degradation applied
        """
        # Check profile completeness
        profile_completeness = self._estimate_profile_completeness(profile_signals)

        # If profile data is minimal (less than 25% complete), use fallback method
        if profile_completeness < 0.25:
            self.logger.warning(f"Profile completeness is low ({profile_completeness:.2f}), using graceful degradation")
            return self._handle_minimal_profile_data(profile_signals, industries)

        # Check for conflicting signals across multiple domains
        has_conflicting_signals = self._detect_conflicting_signals_across_domains(profile_signals)

        if has_conflicting_signals:
            self.logger.warning("Detected conflicting signals across multiple domains, adjusting recommendations")
            # Use a special inference method that handles conflicts appropriately
            return self._infer_roles_with_conflict_handling(profile_signals, industries, max_roles, timeout)

        # Otherwise, use normal inference process
        return self.infer_roles(profile_signals, industries, max_roles, timeout)

    def _detect_conflicting_signals_across_domains(self, profile_signals: ProfileSignals) -> bool:
        """
        Detect conflicting signals across multiple domains in the profile.

        Args:
            profile_signals: Profile signals to analyze for conflicts

        Returns:
            bool: True if conflicting signals are detected, False otherwise
        """
        conflicts_detected = 0

        # Check for conflicting technology stacks (e.g., frontend vs backend focus)
        profile_data = profile_signals.profile_signals
        if isinstance(profile_data, dict):
            github_activity = profile_data.get('github_activity', {})
            linkedin_summary = profile_data.get('linkedin_summary', {})
        else:
            # If it's a Pydantic model, access the fields directly
            github_activity = getattr(profile_data, 'github_activity', {})
            linkedin_summary = getattr(profile_data, 'linkedin_summary', {})

        # Get skills from different sources
        aggregated_skills = set(s.lower() for s in profile_signals.aggregated_skills)

        # Define conflicting technology categories
        frontend_techs = {'javascript', 'react', 'vue', 'angular', 'html', 'css', 'sass', 'scss', 'typescript'}
        backend_techs = {'python', 'java', 'node.js', 'php', 'ruby', 'go', 'rust', 'database', 'sql', 'api', 'django', 'flask', 'spring'}
        data_science_techs = {'python', 'r', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn', 'jupyter', 'sql'}
        devops_techs = {'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci/cd', 'jenkins', 'terraform'}

        # Count skills in each category
        frontend_skills = aggregated_skills.intersection(frontend_techs)
        backend_skills = aggregated_skills.intersection(backend_techs)
        data_science_skills = aggregated_skills.intersection(data_science_techs)
        devops_skills = aggregated_skills.intersection(devops_techs)

        # Detect if there are strong signals in multiple conflicting areas (>2 skills in each)
        strong_areas = 0
        if len(frontend_skills) >= 3:
            strong_areas += 1
        if len(backend_skills) >= 3:
            strong_areas += 1
        if len(data_science_skills) >= 2:  # Less stringent for data science since it often overlaps
            strong_areas += 1
        if len(devops_skills) >= 2:  # Less stringent for devops as well
            strong_areas += 1

        # If there are strong signals in 2 or more different areas, consider it conflicting
        if strong_areas >= 2:
            conflicts_detected += 1
            self.logger.info(f"Detected {strong_areas} conflicting technology areas in profile")

        # Check for conflicting experience levels
        experience_summary = profile_signals.experience_summary
        if isinstance(experience_summary, dict):
            experience_years = experience_summary.get('total_years', 0)
            leadership_indicators = experience_summary.get('leadership_indicators', [])
        else:
            experience_years = getattr(experience_summary, 'total_years', 0)
            leadership_indicators = getattr(experience_summary, 'leadership_indicators', [])

        # If someone has many years of experience but few leadership indicators, there might be a mismatch
        if experience_years >= 5 and len(leadership_indicators) < 2:
            # This isn't necessarily conflicting but might indicate different career paths
            pass

        # Check for conflicting domain experience
        if isinstance(experience_summary, dict):
            experience_domains = experience_summary.get('domains', [])
        else:
            experience_domains = getattr(experience_summary, 'domains', [])

        if len(experience_domains) > 3:
            # Multiple domains might indicate versatility but also lack of focus
            conflicts_detected += 1
            self.logger.info(f"Profile spans {len(experience_domains)} different domains: {experience_domains}")

        # Check for conflicting role signals in project descriptions
        project_highlights = profile_signals.project_highlights
        role_signals = set()
        for project in project_highlights:
            if isinstance(project, dict):
                description = project.get('description', '').lower()
            else:
                description = getattr(project, 'description', '').lower()

            if 'management' in description or 'lead' in description:
                role_signals.add('management')
            if 'technical' in description or 'engineering' in description:
                role_signals.add('technical')
            if 'design' in description:
                role_signals.add('design')
            if 'research' in description:
                role_signals.add('research')

        if len(role_signals) > 2:
            conflicts_detected += 1
            self.logger.info(f"Detected {len(role_signals)} different role types: {role_signals}")

        return conflicts_detected > 0

    def _infer_roles_with_conflict_handling(
        self,
        profile_signals: ProfileSignals,
        industries: List[str],
        max_roles: int = MAX_ROLES_PER_INDUSTRY,
        timeout: int = ROLE_INFERENCE_TIMEOUT
    ) -> RoleRecommendation:
        """
        Infer roles specifically handling cases with conflicting signals across domains.

        Args:
            profile_signals: Profile signals with conflicting information
            industries: List of target industries to search for roles
            max_roles: Maximum number of roles to recommend per industry
            timeout: Timeout for role inference in seconds

        Returns:
            RoleRecommendation: Recommendations that acknowledge and address conflicts
        """
        self.logger.info("Generating recommendations with conflict-aware logic")

        # Use the normal inference process but with special handling
        base_recommendation = self.infer_roles(profile_signals, industries, max_roles, timeout)

        # Add conflict-aware adjustments to the recommendations
        adjusted_roles = []
        for role in base_recommendation.roles:
            # Add conflict-aware justification
            if 'conflict_explanation' not in role.justification:
                role.justification['conflict_explanation'] = (
                    "This profile shows skills across multiple domains. "
                    "These recommendations balance different skill sets. "
                    "Consider focusing on one primary area for stronger positioning."
                )

            # Adjust confidence factors to acknowledge conflicts
            role.confidence_factors.append("Multiple domain skills detected - recommendations balance different areas")

            # Add conflict-aware improvement suggestions
            role.improvement_suggestions.extend([
                "Consider emphasizing one primary skill area for stronger role alignment",
                "Focus on projects that align with your target role to reduce domain conflicts"
            ])

            adjusted_roles.append(role)

        # Create a new recommendation with adjusted roles
        conflict_aware_recommendation = RoleRecommendation(
            recommendation_id=f"conflict_aware_{base_recommendation.recommendation_id}",
            session_id=base_recommendation.session_id,
            roles=adjusted_roles,
            overall_confidence=base_recommendation.overall_confidence * 0.8,  # Slightly reduce confidence due to conflicts
            confidence_factors=base_recommendation.confidence_factors + [
                "Conflicting signals detected across domains",
                "Recommendations attempt to balance multiple skill areas"
            ],
            recommendation_timestamp=datetime.now(),
            industry=base_recommendation.industry
        )

        self.logger.info("Generated conflict-aware recommendations")
        return conflict_aware_recommendation

    async def infer_roles_with_timeout(
        self,
        profile_signals: ProfileSignals,
        industries: List[str],
        max_roles: int = MAX_ROLES_PER_INDUSTRY
    ) -> Optional[RoleRecommendation]:
        """
        Infer roles with a timeout to prevent long-running operations.
        """
        try:
            return await asyncio.wait_for(
                self.infer_roles(profile_signals, industries, max_roles),
                timeout=ROLE_INFERENCE_TIMEOUT
            )
        except asyncio.TimeoutError:
            self.logger.error(f"Role inference timed out after {ROLE_INFERENCE_TIMEOUT} seconds")
            return None
        except Exception as e:
            self.logger.error(f"Error during role inference: {e}")
            return None

    def infer_roles_sync_with_timeout(
        self,
        profile_signals: ProfileSignals,
        industries: List[str],
        max_roles: int = MAX_ROLES_PER_INDUSTRY
    ) -> Optional[RoleRecommendation]:
        """
        Synchronous wrapper for infer_roles with timeout.
        This is useful when called from synchronous contexts like Streamlit.
        """
        import threading
        import queue

        result_queue = queue.Queue()

        def run_inference():
            try:
                import asyncio
                import nest_asyncio
                nest_asyncio.apply()  # Allow nested event loops

                async def run_async_inference():
                    return await self.infer_roles(
                        profile_signals=profile_signals,
                        industries=industries,
                        max_roles=max_roles,
                        timeout=ROLE_INFERENCE_TIMEOUT
                    )

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(run_async_inference())
                result_queue.put(('success', result))
            except Exception as e:
                result_queue.put(('error', e))

        # Start the inference in a separate thread
        inference_thread = threading.Thread(target=run_inference)
        inference_thread.start()

        # Wait for the result with timeout
        try:
            result_type, result = result_queue.get(timeout=ROLE_INFERENCE_TIMEOUT + 5)  # Add 5 seconds buffer
            if result_type == 'error':
                raise result
            return result
        except queue.Empty:
            self.logger.error(f"Synchronous role inference timed out after {ROLE_INFERENCE_TIMEOUT} seconds")
            return None
        finally:
            # Ensure the thread completes
            inference_thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish


# Global role inferencer instance
role_inferencer = RoleInferencer()


def get_role_inferencer() -> RoleInferencer:
    """Get the global role inferencer instance"""
    return role_inferencer