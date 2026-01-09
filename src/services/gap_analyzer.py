"""Gap analysis service for job role recommender"""

import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime

from ..models.gap_analysis import GapAnalysis, SkillGap
from ..models.profile_signals import ProfileSignals
from ..utils.constants import (
    SUPPORTED_INDUSTRIES,
    CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, CONFIDENCE_LOW
)


class GapAnalyzer:
    """Analyzes skill gaps between user profile and target role requirements"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_gaps(
        self,
        profile_signals: ProfileSignals,
        target_role_requirements: Dict[str, Any]
    ) -> GapAnalysis:
        """
        Analyze gaps between user profile and target role requirements.

        Args:
            profile_signals: User's profile signals
            target_role_requirements: Requirements for the target role

        Returns:
            GapAnalysis: Analysis of skill gaps and improvement suggestions
        """
        session_id = profile_signals.signals_id
        role_id = target_role_requirements.get('role_id', 'unknown_role')

        # Identify missing skills
        missing_skills = self._identify_missing_skills(
            profile_signals,
            target_role_requirements
        )

        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(
            missing_skills,
            target_role_requirements
        )

        # Identify priority areas
        priority_areas = self._identify_priority_areas(
            missing_skills,
            target_role_requirements
        )

        # Create skill gap objects
        skill_gaps = []
        for skill_name, importance_level, current_level, target_level in missing_skills:
            # Ensure importance level is properly assigned
            final_importance_level = self._assign_importance_level(
                skill_name,
                importance_level,
                target_role_requirements
            )

            skill_gap = SkillGap(
                skill_name=skill_name,
                importance_level=final_importance_level,
                current_level=current_level,
                target_level=target_level,
                improvement_suggestions=self._get_skill_specific_suggestions(
                    skill_name, target_role_requirements
                ),
                priority=self._calculate_skill_priority(
                    final_importance_level, current_level, target_level
                )
            )
            skill_gaps.append(skill_gap)

        # Create GapAnalysis object
        gap_analysis = GapAnalysis(
            gap_id=f"gap_{session_id}_{role_id}",
            role_id=role_id,
            session_id=session_id,
            missing_skills=skill_gaps,
            improvement_suggestions=improvement_suggestions,
            priority_areas=priority_areas,
            analysis_timestamp=datetime.now()
        )

        return gap_analysis

    def _identify_missing_skills(
        self,
        profile_signals: ProfileSignals,
        target_role_requirements: Dict[str, Any]
    ) -> List[Tuple[str, str, float, float]]:
        """
        Identify skills that the user lacks for the target role.

        Returns:
            List of tuples: (skill_name, importance_level, current_level, target_level)
        """
        # Get user's skills from profile signals
        user_skills = set(s.lower() for s in profile_signals.aggregated_skills)

        # Get required and preferred skills from role requirements
        required_skills = target_role_requirements.get('required_skills', [])
        preferred_skills = target_role_requirements.get('preferred_skills', [])
        technologies = target_role_requirements.get('technologies', [])

        # Combine all role skills with different importance levels
        all_role_skills = []
        for skill in required_skills:
            all_role_skills.append((skill.lower(), 'CRITICAL', 0.0, 1.0))  # Default current level 0.0 for missing
        for skill in preferred_skills:
            all_role_skills.append((skill.lower(), 'IMPORTANT', 0.0, 0.7))
        for tech in technologies:
            all_role_skills.append((tech.lower(), 'NICE_TO_HAVE', 0.0, 0.5))

        # Identify missing skills
        missing_skills = []
        for skill_name, importance, current_level, target_level in all_role_skills:
            if skill_name not in user_skills:
                missing_skills.append((skill_name.title(), importance, current_level, target_level))

        # Sort by importance and priority
        missing_skills.sort(key=lambda x: self._importance_to_priority(x[1]), reverse=True)

        return missing_skills

    def _importance_to_priority(self, importance_level: str) -> int:
        """Convert importance level to numeric priority."""
        importance_map = {
            'CRITICAL': 3,
            'IMPORTANT': 2,
            'NICE_TO_HAVE': 1
        }
        return importance_map.get(importance_level, 0)

    def _generate_improvement_suggestions(
        self,
        missing_skills: List[Tuple[str, str, float, float]],
        target_role_requirements: Dict[str, Any]
    ) -> List[str]:
        """Generate general improvement suggestions based on missing skills."""
        suggestions = []

        # Count by importance level
        critical_count = sum(1 for skill in missing_skills if skill[1] == 'CRITICAL')
        important_count = sum(1 for skill in missing_skills if skill[1] == 'IMPORTANT')
        nice_to_have_count = sum(1 for skill in missing_skills if skill[1] == 'NICE_TO_HAVE')

        if critical_count > 0:
            suggestions.append(f"Focus on acquiring {critical_count} critical skills required for this role")

        if important_count > 0:
            suggestions.append(f"Consider developing {important_count} important skills to strengthen your profile")

        if nice_to_have_count > 0:
            suggestions.append(f"Learning {nice_to_have_count} additional skills would be beneficial but not essential")

        # Add role-specific suggestions
        role_title = target_role_requirements.get('title', 'the role')
        industry = target_role_requirements.get('industry', 'the industry')

        if missing_skills:
            # Get the most important missing skill
            most_important_missing = next(
                (skill for skill in missing_skills if skill[1] == 'CRITICAL'),
                missing_skills[0] if missing_skills else None
            )

            if most_important_missing:
                suggestions.append(
                    f"Start with {most_important_missing[0]}, which is critical for {role_title} positions in {industry}"
                )

        # Add high-level improvement suggestions (without detailed curriculum)
        suggestions.extend(self._generate_high_level_improvements(
            missing_skills, target_role_requirements
        ))

        return suggestions

    def _generate_high_level_improvements(
        self,
        missing_skills: List[Tuple[str, str, float, float]],
        target_role_requirements: Dict[str, Any]
    ) -> List[str]:
        """
        Generate high-level improvement suggestions without detailed curriculum.

        Args:
            missing_skills: List of missing skills with importance levels
            target_role_requirements: Requirements for the target role

        Returns:
            List of high-level improvement suggestions
        """
        high_level_suggestions = []

        # Suggest learning paths based on skill categories
        critical_skills = [skill[0] for skill in missing_skills if skill[1] == 'CRITICAL']
        important_skills = [skill[0] for skill in missing_skills if skill[1] == 'IMPORTANT']

        if critical_skills:
            high_level_suggestions.append(
                f"Focus on mastering the core technologies: {', '.join(critical_skills[:3])}"
            )

        if important_skills:
            high_level_suggestions.append(
                f"Develop proficiency in: {', '.join(important_skills[:3])}"
            )

        # Suggest practical application
        if critical_skills or important_skills:
            high_level_suggestions.append(
                "Apply new skills by building relevant projects that demonstrate your capabilities"
            )

        # Suggest industry-specific approaches
        industry = target_role_requirements.get('industry', '').lower()
        if 'data' in industry or 'ml' in industry or 'ai' in industry:
            high_level_suggestions.append(
                "Work on data science or ML projects to build a portfolio showcasing your analytical skills"
            )
        elif 'software' in industry or 'engineering' in industry:
            high_level_suggestions.append(
                "Contribute to open-source projects or build a portfolio of software applications"
            )
        elif 'security' in industry:
            high_level_suggestions.append(
                "Practice security assessments and learn about compliance frameworks relevant to the industry"
            )

        # Suggest networking and visibility
        role_title = target_role_requirements.get('title', '').lower()
        if 'senior' in role_title or 'lead' in role_title:
            high_level_suggestions.append(
                "Focus on leadership skills by mentoring others, contributing to technical discussions, and sharing knowledge"
            )

        # Suggest certification or learning approach
        if len(critical_skills) > 2:
            high_level_suggestions.append(
                "Consider structured learning paths or certifications to systematically address skill gaps"
            )

        return high_level_suggestions

    def _identify_priority_areas(
        self,
        missing_skills: List[Tuple[str, str, float, float]],
        target_role_requirements: Dict[str, Any]
    ) -> List[str]:
        """Identify priority areas for improvement."""
        priority_areas = []

        # Group missing skills by importance
        critical_skills = [skill[0] for skill in missing_skills if skill[1] == 'CRITICAL']
        important_skills = [skill[0] for skill in missing_skills if skill[1] == 'IMPORTANT']
        nice_to_have_skills = [skill[0] for skill in missing_skills if skill[1] == 'NICE_TO_HAVE']

        if critical_skills:
            priority_areas.append(f"Critical skills to acquire: {', '.join(critical_skills[:3])}")  # Top 3

        if important_skills:
            priority_areas.append(f"Important skills to develop: {', '.join(important_skills[:3])}")  # Top 3

        # Add experience-based priority if applicable
        required_experience = target_role_requirements.get('required_experience', 0)
        # We'll need to pass profile_signals separately, so we'll skip this for now
        # since the method signature doesn't allow it

        # Identify priority based on skill gaps and their impact
        if critical_skills:
            priority_areas.append("Focus on critical skills first as they are required for the role")

        if important_skills and critical_skills:
            priority_areas.append("After critical skills, work on important skills to strengthen your profile")

        # Add domain-specific priority areas
        industry = target_role_requirements.get('industry', '').lower()
        if 'data' in industry or 'ml' in industry or 'ai' in industry:
            priority_areas.append("Focus on data manipulation and analysis skills first")
        elif 'software' in industry or 'engineering' in industry:
            priority_areas.append("Focus on core programming and system design skills first")
        elif 'security' in industry:
            priority_areas.append("Prioritize security best practices and compliance knowledge")

        # Add priority based on skill interdependencies
        priority_areas.extend(self._identify_skill_interdependencies(critical_skills, important_skills))

        return priority_areas

    def _identify_skill_interdependencies(
        self,
        critical_skills: List[str],
        important_skills: List[str]
    ) -> List[str]:
        """
        Identify priority based on skill interdependencies.

        Args:
            critical_skills: List of critical skills
            important_skills: List of important skills

        Returns:
            List of priority areas based on interdependencies
        """
        priority_areas = []

        # Define common skill dependencies
        dependencies = {
            'Docker': ['Linux', 'Networking'],
            'Kubernetes': ['Docker', 'Linux', 'Networking'],
            'React': ['JavaScript', 'HTML', 'CSS'],
            'Angular': ['JavaScript', 'TypeScript'],
            'TensorFlow': ['Python', 'Mathematics'],
            'PyTorch': ['Python', 'Mathematics'],
            'AWS': ['Linux', 'Networking'],
            'Azure': ['Networking', 'Security'],
            'GCP': ['Networking', 'Security'],
            'SQL': ['Database Design'],
            'NoSQL': ['Database Design'],
            'CI/CD': ['Git', 'Scripting'],
            'DevOps': ['Linux', 'Scripting', 'Networking'],
            'Machine Learning': ['Statistics', 'Python', 'Mathematics'],
            'Data Science': ['Statistics', 'Python', 'SQL']
        }

        # Check for dependencies that are missing
        all_missing_skills = set(critical_skills + important_skills)
        dependency_issues = []

        for skill in all_missing_skills:
            if skill in dependencies:
                needed_dependencies = dependencies[skill]
                missing_dependencies = [dep for dep in needed_dependencies if dep in all_missing_skills]
                if missing_dependencies:
                    dependency_issues.append(f"For {skill}, also need: {', '.join(missing_dependencies)}")

        if dependency_issues:
            priority_areas.extend(dependency_issues)

        return priority_areas

    def _get_user_experience(self, profile_signals: ProfileSignals) -> float:
        """Extract user's years of experience from profile signals."""
        experience_summary = profile_signals.experience_summary
        if isinstance(experience_summary, dict):
            return experience_summary.get('total_years', 0.0)
        else:
            # If it's a Pydantic model, access the field directly
            return getattr(experience_summary, 'total_years', 0.0)

    def _get_skill_specific_suggestions(
        self,
        skill_name: str,
        target_role_requirements: Dict[str, Any]
    ) -> List[str]:
        """Generate skill-specific improvement suggestions."""
        suggestions = []

        # Basic suggestion
        suggestions.append(f"Learn {skill_name} through online courses, tutorials, or hands-on projects")

        # Industry-specific suggestions could go here
        industry = target_role_requirements.get('industry', '').lower()
        if 'data' in industry or 'ml' in industry or 'ai' in industry:
            if 'python' in skill_name.lower():
                suggestions.append(f"Focus on Python libraries relevant to {industry} such as scikit-learn, pandas, or TensorFlow")
            elif 'sql' in skill_name.lower():
                suggestions.append(f"Practice SQL queries with analytical functions commonly used in {industry}")

        # Role-specific suggestions
        role_title = target_role_requirements.get('title', '').lower()
        if 'engineer' in role_title:
            if 'testing' in skill_name.lower():
                suggestions.append(f"Learn testing frameworks relevant to software engineering like pytest or JUnit")
            elif 'devops' in skill_name.lower():
                suggestions.append(f"Focus on CI/CD pipelines, containerization (Docker), and infrastructure as code (Terraform)")

        return suggestions

    def _calculate_skill_priority(
        self,
        importance_level: str,
        current_level: float,
        target_level: float
    ) -> int:
        """Calculate priority score for a skill gap."""
        # Base priority from importance level
        base_priority = self._importance_to_priority(importance_level)

        # Gap size factor (larger gaps may have higher priority to address)
        gap_size = target_level - current_level
        gap_factor = int(gap_size * 10)  # Scale gap to influence priority

        # Calculate final priority (higher number = higher priority)
        final_priority = base_priority * 10 + gap_factor

        return final_priority

    def _assign_importance_level(
        self,
        skill_name: str,
        base_importance_level: str,
        target_role_requirements: Dict[str, Any]
    ) -> str:
        """
        Assign importance level to a skill gap based on multiple factors.

        Args:
            skill_name: Name of the skill
            base_importance_level: Initial importance level
            target_role_requirements: Requirements for the target role

        Returns:
            str: Final importance level (CRITICAL, IMPORTANT, NICE_TO_HAVE)
        """
        # Start with the base importance level
        importance_level = base_importance_level

        # Adjust based on role requirements
        required_skills = target_role_requirements.get('required_skills', [])
        preferred_skills = target_role_requirements.get('preferred_skills', [])
        technologies = target_role_requirements.get('technologies', [])

        # Increase importance if it's a required skill
        if skill_name.lower() in [s.lower() for s in required_skills]:
            importance_level = 'CRITICAL'
        elif skill_name.lower() in [s.lower() for s in preferred_skills]:
            if importance_level != 'CRITICAL':  # Don't downgrade if already critical
                importance_level = 'IMPORTANT'
        elif skill_name.lower() in [t.lower() for t in technologies]:
            if importance_level == 'NICE_TO_HAVE':  # Only upgrade if currently low importance
                importance_level = 'IMPORTANT'

        # Additional heuristics for importance assignment
        skill_lower = skill_name.lower()

        # Critical skills based on industry or role
        industry = target_role_requirements.get('industry', '').lower()
        role_title = target_role_requirements.get('title', '').lower()

        # For certain industries, some skills become more critical
        if 'security' in industry or 'security' in role_title:
            security_skills = ['security', 'cybersecurity', 'encryption', 'authentication', 'authorization']
            if any(sec_skill in skill_lower for sec_skill in security_skills):
                importance_level = 'CRITICAL'

        if 'data' in industry or 'data' in role_title:
            data_skills = ['python', 'sql', 'r', 'statistics', 'machine learning', 'pandas', 'numpy']
            if any(data_skill in skill_lower for data_skill in data_skills):
                if importance_level != 'CRITICAL':
                    importance_level = 'IMPORTANT'

        # For leadership roles, certain skills become more important
        leadership_keywords = ['lead', 'senior', 'manager', 'architect', 'principal']
        if any(keyword in role_title for keyword in leadership_keywords):
            leadership_skills = ['leadership', 'communication', 'mentoring', 'architecture', 'design']
            if any(lead_skill in skill_lower for lead_skill in leadership_skills):
                if importance_level != 'CRITICAL':
                    importance_level = 'IMPORTANT'

        return importance_level

    def compare_profile_to_multiple_roles(
        self,
        profile_signals: ProfileSignals,
        role_requirements_list: List[Dict[str, Any]]
    ) -> List[GapAnalysis]:
        """
        Compare profile to multiple roles and return gap analyses for each.

        Args:
            profile_signals: User's profile signals
            role_requirements_list: List of role requirements to compare against

        Returns:
            List of GapAnalysis objects for each role
        """
        gap_analyses = []

        for role_requirements in role_requirements_list:
            try:
                gap_analysis = self.analyze_gaps(profile_signals, role_requirements)
                gap_analyses.append(gap_analysis)
            except Exception as e:
                self.logger.error(f"Error analyzing gaps for role {role_requirements.get('title', 'unknown')}: {e}")
                continue

        return gap_analyses

    def generate_gap_summary(
        self,
        gap_analysis: GapAnalysis
    ) -> Dict[str, Any]:
        """
        Generate a summary of the gap analysis.

        Args:
            gap_analysis: The gap analysis to summarize

        Returns:
            Dict with summary statistics
        """
        total_gaps = len(gap_analysis.missing_skills)
        critical_gaps = sum(1 for gap in gap_analysis.missing_skills if gap.importance_level == 'CRITICAL')
        important_gaps = sum(1 for gap in gap_analysis.missing_skills if gap.importance_level == 'IMPORTANT')
        nice_to_have_gaps = sum(1 for gap in gap_analysis.missing_skills if gap.importance_level == 'NICE_TO_HAVE')

        # Calculate average gap priority
        if total_gaps > 0:
            avg_priority = sum(gap.priority for gap in gap_analysis.missing_skills) / total_gaps
        else:
            avg_priority = 0

        return {
            'total_gaps': total_gaps,
            'critical_gaps': critical_gaps,
            'important_gaps': important_gaps,
            'nice_to_have_gaps': nice_to_have_gaps,
            'average_priority': avg_priority,
            'top_priority_skills': [
                gap.skill_name for gap in sorted(
                    gap_analysis.missing_skills,
                    key=lambda x: x.priority,
                    reverse=True
                )[:5]  # Top 5 priority gaps
            ]
        }


# Global gap analyzer instance
gap_analyzer = GapAnalyzer()


def get_gap_analyzer() -> GapAnalyzer:
    """Get the global gap analyzer instance"""
    return gap_analyzer