"""Seniority detection service for job role recommender"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.profile_signals import ProfileSignals
from ..utils.constants import SENIORITY_JUNIOR, SENIORITY_MID, SENIORITY_SENIOR


class SeniorityDetector:
    """Detects appropriate seniority level based on profile signals and experience"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def detect_seniority(
        self,
        profile_signals: ProfileSignals,
        target_role_title: str = ""
    ) -> str:
        """
        Detect the appropriate seniority level based on profile signals.

        Args:
            profile_signals: Aggregated profile signals to analyze
            target_role_title: Optional target role title to tailor detection

        Returns:
            str: Seniority level (JUNIOR, MID, or SENIOR)
        """
        # Calculate various factors that influence seniority
        raw_years_experience = self._extract_years_experience(profile_signals)
        years_experience = self._apply_experience_heuristics(raw_years_experience, target_role_title)
        leadership_indicators = self._count_leadership_indicators(profile_signals)
        github_activity_score = self._calculate_github_activity_score(profile_signals)
        project_complexity_score = self._calculate_project_complexity_score(profile_signals)
        technology_depth = self._calculate_technology_depth(profile_signals)

        # Calculate weighted seniority score
        seniority_score = self._calculate_seniority_score(
            years_experience,
            leadership_indicators,
            github_activity_score,
            project_complexity_score,
            technology_depth
        )

        # Map score to seniority level
        return self._map_score_to_seniority(seniority_score)

    def _extract_years_experience(self, profile_signals: ProfileSignals) -> float:
        """Extract years of experience from profile signals."""
        experience_summary = profile_signals.experience_summary
        if isinstance(experience_summary, dict):
            return experience_summary.get('total_years', 0.0)
        else:
            # If it's a Pydantic model, access the field directly
            return getattr(experience_summary, 'total_years', 0.0)

    def _apply_experience_heuristics(self, years_experience: float, role_title: str = "") -> float:
        """
        Apply experience-based heuristics to adjust seniority based on role expectations.

        Args:
            years_experience: Raw years of experience
            role_title: Target role title to apply specific heuristics

        Returns:
            Adjusted years of experience based on role-specific heuristics
        """
        adjusted_years = years_experience

        # Role-specific heuristics
        if role_title:
            role_lower = role_title.lower()

            # For senior roles, require more experience
            if 'senior' in role_lower or 'lead' in role_lower or 'principal' in role_lower or 'architect' in role_lower:
                # For senior roles, you typically need more experience
                if years_experience < 5:
                    # Reduce the effective experience for senior role expectations
                    adjusted_years = years_experience * 0.8
                elif years_experience >= 8:
                    # Reward extensive experience for senior roles
                    adjusted_years = years_experience * 1.1
            elif 'junior' in role_lower or 'entry' in role_lower or 'associate' in role_lower:
                # For junior roles, even moderate experience is valuable
                if years_experience >= 2 and years_experience < 5:
                    adjusted_years = years_experience * 1.2
            elif 'intern' in role_lower:
                # For intern roles, experience expectations are lower
                adjusted_years = min(years_experience, 2.0)

        # Industry-specific heuristics could go here
        # For example, in fast-moving fields like web development,
        # newer experience might be weighted more heavily

        # General heuristics
        if years_experience > 15:
            # For very experienced candidates, cap the advantage to prevent over-weighting
            adjusted_years = 12.0 + (years_experience - 15) * 0.5
        elif years_experience < 1:
            # For less than 1 year, adjust based on projects/education
            adjusted_years = years_experience * 0.5  # New grads typically need more development

        return min(adjusted_years, 20.0)  # Cap at 20 years to prevent extreme values

    def _count_leadership_indicators(self, profile_signals: ProfileSignals) -> int:
        """Count leadership indicators in profile signals."""
        experience_summary = profile_signals.experience_summary
        if isinstance(experience_summary, dict):
            leadership_indicators = experience_summary.get('leadership_indicators', [])
        else:
            # If it's a Pydantic model, access the field directly
            leadership_indicators = getattr(experience_summary, 'leadership_indicators', [])

        return len(leadership_indicators) if leadership_indicators else 0

    def _calculate_github_activity_score(self, profile_signals: ProfileSignals) -> float:
        """Calculate a score based on GitHub activity signals."""
        profile_data = profile_signals.profile_signals
        if isinstance(profile_data, dict):
            github_activity = profile_data.get('github_activity', {})
        else:
            # Access the field from the Pydantic model
            github_activity = getattr(profile_data, 'github_activity', {})

        # Calculate score based on various GitHub metrics
        total_commits = github_activity.get('total_commits', 0)
        repositories = github_activity.get('repositories', 0)
        stars_received = github_activity.get('stars_received', 0)
        contributions = github_activity.get('contributions', 0)
        top_languages = github_activity.get('top_languages', [])
        recent_activity = github_activity.get('recent_activity', False)

        # Calculate scores for different metrics
        commit_score = min(total_commits / 500.0, 1.0)  # 500 commits = full score
        repo_score = min(repositories / 10.0, 1.0)     # 10 repos = full score
        star_score = min(stars_received / 50.0, 1.0)   # 50 stars = full score
        contrib_score = min(contributions / 100.0, 1.0) # 100 contributions = full score
        language_diversity_score = min(len(top_languages) / 5.0, 1.0)  # 5 languages = full score
        recent_activity_score = 1.0 if recent_activity else 0.3  # Bonus for recent activity

        # Weighted average with additional factors for seniority detection
        activity_score = (
            commit_score * 0.25 +      # Commit history
            repo_score * 0.15 +        # Repository count
            star_score * 0.2 +         # Recognition
            contrib_score * 0.2 +      # Contribution patterns
            language_diversity_score * 0.1 +  # Technology breadth
            recent_activity_score * 0.1       # Activity recency
        )

        return activity_score

    def _analyze_github_contribution_patterns(self, profile_signals: ProfileSignals) -> Dict[str, float]:
        """
        Analyze GitHub contribution patterns for seniority indicators.

        Args:
            profile_signals: Profile signals containing GitHub data

        Returns:
            Dict with various contribution pattern scores
        """
        profile_data = profile_signals.profile_signals
        if isinstance(profile_data, dict):
            github_activity = profile_data.get('github_activity', {})
        else:
            github_activity = getattr(profile_data, 'github_activity', {})

        total_commits = github_activity.get('total_commits', 0)
        repositories = github_activity.get('repositories', 0)
        contributions = github_activity.get('contributions', 0)
        recent_activity = github_activity.get('recent_activity', False)

        # Analyze contribution consistency
        consistency_score = 0.0
        if total_commits > 0 and contributions > 0:
            # More contributions than commits might indicate issue participation, PR reviews, etc.
            if contributions > total_commits:
                consistency_score = min(contributions / (total_commits * 2), 1.0)
            else:
                consistency_score = min(total_commits / 100.0, 1.0)  # Regular contributors

        # Analyze repository diversity (working on multiple projects)
        repo_diversity_score = min(repositories / 5.0, 1.0) if repositories > 0 else 0.0

        # Analyze activity recency (recent activity is good for seniority)
        recent_activity_score = 1.0 if recent_activity else 0.5

        # Calculate leadership indicators from GitHub
        leadership_score = 0.0
        if repositories > 0:
            # If they have many repositories they likely started projects (leadership)
            leadership_score = min(repositories / 15.0, 0.5)  # Max 0.5 for leadership

        return {
            'consistency_score': consistency_score,
            'repo_diversity_score': repo_diversity_score,
            'recent_activity_score': recent_activity_score,
            'leadership_score': leadership_score
        }

    def _calculate_project_complexity_score(self, profile_signals: ProfileSignals) -> float:
        """Calculate a score based on project complexity."""
        project_highlights = profile_signals.project_highlights
        if not project_highlights:
            return 0.0

        total_score = 0.0
        for project in project_highlights:
            # Score based on number of technologies used
            technologies = project.get('technologies', [])
            tech_score = min(len(technologies) / 5.0, 1.0)  # Max 5 technologies = full score

            # Score based on project impact (if available)
            impact = project.get('impact', '')
            impact_score = 0.5  # Default medium impact
            if 'increased' in impact.lower() or 'improved' in impact.lower():
                impact_score = 0.8
            elif 'developed' in impact.lower() or 'created' in impact.lower():
                impact_score = 0.6

            total_score += (tech_score * 0.6 + impact_score * 0.4)

        # Average score across all projects
        avg_score = total_score / len(project_highlights) if project_highlights else 0.0
        return min(avg_score, 1.0)

    def _calculate_technology_depth(self, profile_signals: ProfileSignals) -> float:
        """Calculate a score based on technology depth and variety."""
        technology_stack = []
        experience_summary = profile_signals.experience_summary

        if isinstance(experience_summary, dict):
            technology_stack = experience_summary.get('technology_stack', [])
        else:
            technology_stack = getattr(experience_summary, 'technology_stack', [])

        # Score based on number of technologies (variety)
        variety_score = min(len(technology_stack) / 10.0, 1.0)  # Max 10 technologies = full variety score

        # In a real implementation, we might also consider depth in each technology
        # For now, we'll just use variety as a proxy for depth
        return variety_score

    def _calculate_seniority_score(
        self,
        years_experience: float,
        leadership_indicators: int,
        github_activity_score: float,
        project_complexity_score: float,
        technology_depth: float
    ) -> float:
        """Calculate overall seniority score from multiple factors."""
        # Weighted score calculation
        # Years of experience is the most important factor
        experience_weight = 0.4
        leadership_weight = 0.2
        github_weight = 0.15
        project_weight = 0.15
        technology_weight = 0.1

        # Normalize years of experience to 0-1 scale (0-15 years)
        exp_score = min(years_experience / 15.0, 1.0)

        # Normalize leadership indicators to 0-1 scale (0-5 indicators)
        leadership_score = min(leadership_indicators / 5.0, 1.0)

        # Calculate weighted score
        weighted_score = (
            exp_score * experience_weight +
            leadership_score * leadership_weight +
            github_activity_score * github_weight +
            project_complexity_score * project_weight +
            technology_depth * technology_weight
        )

        return weighted_score

    def _map_score_to_seniority(self, score: float) -> str:
        """Map the seniority score to a seniority level."""
        if score >= 0.7:
            return SENIORITY_SENIOR
        elif score >= 0.4:
            return SENIORITY_MID
        else:
            return SENIORITY_JUNIOR

    def detect_seniority_with_context(
        self,
        profile_signals: ProfileSignals,
        target_role_title: str = "",
        target_industry: str = ""
    ) -> Dict[str, Any]:
        """
        Detect seniority with additional context and reasoning.

        Args:
            profile_signals: Aggregated profile signals to analyze
            target_role_title: Optional target role title
            target_industry: Optional target industry

        Returns:
            Dict with seniority level and reasoning
        """
        years_experience = self._extract_years_experience(profile_signals)
        leadership_indicators = self._count_leadership_indicators(profile_signals)
        github_activity_score = self._calculate_github_activity_score(profile_signals)
        project_complexity_score = self._calculate_project_complexity_score(profile_signals)
        technology_depth = self._calculate_technology_depth(profile_signals)

        seniority_score = self._calculate_seniority_score(
            years_experience,
            leadership_indicators,
            github_activity_score,
            project_complexity_score,
            technology_depth
        )

        seniority_level = self._map_score_to_seniority(seniority_score)

        # Generate reasoning
        reasoning = self._generate_seniority_reasoning(
            seniority_level,
            years_experience,
            leadership_indicators,
            github_activity_score,
            project_complexity_score,
            technology_depth
        )

        return {
            'seniority_level': seniority_level,
            'confidence_score': seniority_score,
            'reasoning': reasoning,
            'breakdown': {
                'years_experience': years_experience,
                'leadership_indicators': leadership_indicators,
                'github_activity_score': github_activity_score,
                'project_complexity_score': project_complexity_score,
                'technology_depth': technology_depth
            }
        }

    def _generate_seniority_reasoning(
        self,
        seniority_level: str,
        years_experience: float,
        leadership_indicators: int,
        github_activity_score: float,
        project_complexity_score: float,
        technology_depth: float
    ) -> List[str]:
        """Generate human-readable reasoning for the seniority determination."""
        reasoning = []

        # Experience-based reasoning
        if years_experience >= 6:
            reasoning.append(f"High years of experience ({years_experience} years) supports senior-level role")
        elif years_experience >= 3:
            reasoning.append(f"Moderate years of experience ({years_experience} years) supports mid-level role")
        else:
            reasoning.append(f"Early career experience ({years_experience} years) supports junior-level role")

        # Leadership reasoning
        if leadership_indicators > 2:
            reasoning.append(f"Strong leadership indicators ({leadership_indicators}) support higher seniority")
        elif leadership_indicators > 0:
            reasoning.append(f"Leadership indicators present ({leadership_indicators}) support mid-level role")

        # GitHub activity reasoning
        if github_activity_score > 0.7:
            reasoning.append("Strong GitHub activity demonstrates experience and engagement")
        elif github_activity_score > 0.4:
            reasoning.append("Moderate GitHub activity shows some engagement")

        # Project complexity reasoning
        if project_complexity_score > 0.7:
            reasoning.append("Complex projects demonstrate advanced skills")
        elif project_complexity_score > 0.4:
            reasoning.append("Projects of moderate complexity show developing skills")

        # Technology depth reasoning
        if technology_depth > 0.7:
            reasoning.append("Deep technology stack demonstrates breadth of knowledge")
        elif technology_depth > 0.4:
            reasoning.append("Good technology variety shows diverse skills")

        return reasoning


# Global seniority detector instance
seniority_detector = SeniorityDetector()


def get_seniority_detector() -> SeniorityDetector:
    """Get the global seniority detector instance"""
    return seniority_detector