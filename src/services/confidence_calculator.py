"""Confidence calculation service for job role recommender"""

import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime

from ..models.profile_signals import ProfileSignals
from ..utils.constants import CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, CONFIDENCE_LOW


class ConfidenceCalculator:
    """Calculates confidence levels for role recommendations based on data completeness"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def calculate_confidence(
        self,
        profile_signals: ProfileSignals,
        role_fit_score: float,
        additional_factors: Dict[str, Any] = None
    ) -> Tuple[float, str, List[str]]:
        """
        Calculate confidence level for a role recommendation.

        Args:
            profile_signals: User's profile signals
            role_fit_score: Initial fit score for the role
            additional_factors: Additional factors that may affect confidence

        Returns:
            Tuple of (confidence_score, confidence_level, confidence_factors)
        """
        if additional_factors is None:
            additional_factors = {}

        # Calculate base confidence from profile completeness
        profile_completeness_score = self._calculate_profile_completeness_score(profile_signals)

        # Calculate data quality score
        data_quality_score = self._calculate_data_quality_score(profile_signals)

        # Calculate consistency score
        consistency_score = self._calculate_consistency_score(profile_signals)

        # Weighted confidence calculation
        # Profile completeness: 40%, Data quality: 30%, Consistency: 20%, Role fit: 10%
        weighted_confidence = (
            profile_completeness_score * 0.4 +
            data_quality_score * 0.3 +
            consistency_score * 0.2 +
            role_fit_score * 0.1
        )

        # Adjust based on additional factors if provided
        if additional_factors:
            weighted_confidence = self._apply_additional_factors(
                weighted_confidence, additional_factors
            )

        # Determine confidence level
        confidence_level = self._determine_confidence_level(weighted_confidence)

        # Generate confidence factors
        confidence_factors = self._generate_confidence_factors(
            profile_signals,
            profile_completeness_score,
            data_quality_score,
            consistency_score,
            role_fit_score
        )

        return weighted_confidence, confidence_level, confidence_factors

    def _calculate_profile_completeness_score(self, profile_signals: ProfileSignals) -> float:
        """Calculate score based on how complete the profile data is."""
        completeness_score = 0.0
        total_components = 4  # resume_signals, profile_signals, aggregated_skills, project_highlights

        # Check resume signals
        if profile_signals.resume_signals:
            completeness_score += 0.25

        # Check profile signals
        if profile_signals.profile_signals:
            completeness_score += 0.25

        # Check aggregated skills
        if profile_signals.aggregated_skills:
            completeness_score += 0.25

        # Check project highlights
        if profile_signals.project_highlights:
            completeness_score += 0.25

        # Additional check: number of skills
        if len(profile_signals.aggregated_skills) >= 10:
            completeness_score += 0.1  # Bonus for comprehensive skill set
        elif len(profile_signals.aggregated_skills) >= 5:
            completeness_score += 0.05

        # Additional check: experience info
        experience_summary = profile_signals.experience_summary
        if isinstance(experience_summary, dict):
            total_years = experience_summary.get('total_years', 0.0)
        else:
            total_years = getattr(experience_summary, 'total_years', 0.0)

        if total_years > 0:
            completeness_score += 0.1  # Bonus for having experience info

        return min(completeness_score, 1.0)

    def _calculate_data_quality_score(self, profile_signals: ProfileSignals) -> float:
        """Calculate score based on data quality and reliability."""
        quality_score = 0.0

        # Check if we have data from multiple sources
        sources_count = 0

        # Check resume data
        resume_data = profile_signals.resume_signals
        if resume_data:
            sources_count += 1
            # Check for key resume elements
            if isinstance(resume_data, dict):
                if resume_data.get('skills') or resume_data.get('experience_years', 0) > 0:
                    quality_score += 0.15

        # Check profile data
        profile_data = profile_signals.profile_signals
        if profile_data:
            sources_count += 1
            if isinstance(profile_data, dict):
                github_activity = profile_data.get('github_activity', {})
                if github_activity.get('total_commits', 0) > 0:
                    quality_score += 0.15
                if github_activity.get('repositories', 0) > 0:
                    quality_score += 0.10

        # Bonus for multiple sources
        if sources_count >= 2:
            quality_score += 0.2
        elif sources_count == 1:
            quality_score += 0.1

        # Check for project highlights
        if profile_signals.project_highlights:
            quality_score += 0.15

        # Normalize to 0-1 range
        return min(quality_score, 1.0)

    def _calculate_consistency_score(self, profile_signals: ProfileSignals) -> float:
        """Calculate score based on consistency across different data sources."""
        consistency_score = 0.0

        # Get skills from different sources
        resume_skills = []
        profile_skills = []

        # Extract resume skills
        resume_data = profile_signals.resume_signals
        if isinstance(resume_data, dict) and 'skills' in resume_data:
            resume_skills = [s.lower() for s in resume_data['skills']]

        # Extract profile skills
        profile_data = profile_signals.profile_signals
        if isinstance(profile_data, dict):
            linkedin_summary = profile_data.get('linkedin_summary', {})
            profile_skills.extend([s.lower() for s in linkedin_summary.get('skills', [])])

            github_activity = profile_data.get('github_activity', {})
            profile_skills.extend([s.lower() for s in github_activity.get('top_languages', [])])

        # Calculate overlap between sources
        if resume_skills and profile_skills:
            resume_set = set(resume_skills)
            profile_set = set(profile_skills)
            intersection = resume_set.intersection(profile_set)
            union = resume_set.union(profile_set)

            if union:
                overlap_ratio = len(intersection) / len(union)
                consistency_score = overlap_ratio * 0.5  # Weight the consistency factor

        # Additional consistency check: experience alignment
        experience_summary = profile_signals.experience_summary
        if isinstance(experience_summary, dict):
            total_years = experience_summary.get('total_years', 0.0)
        else:
            total_years = getattr(experience_summary, 'total_years', 0.0)

        if total_years > 0:
            consistency_score += 0.2  # Good if experience is provided

        return min(consistency_score, 1.0)

    def _apply_additional_factors(
        self,
        base_confidence: float,
        additional_factors: Dict[str, Any]
    ) -> float:
        """Apply additional factors that may adjust the confidence score."""
        adjusted_confidence = base_confidence

        # Apply factor for role archetype availability
        if additional_factors.get('archetype_completeness', 1.0) < 0.5:
            adjusted_confidence *= 0.8  # Reduce confidence if archetype data is incomplete

        # Apply factor for data recency
        if additional_factors.get('data_recent', True) is False:
            adjusted_confidence *= 0.9  # Slightly reduce confidence for old data

        # Apply factor for signal strength
        signal_strength = additional_factors.get('signal_strength', 1.0)
        adjusted_confidence *= signal_strength

        return max(0.0, min(adjusted_confidence, 1.0))  # Clamp between 0 and 1

    def _determine_confidence_level(self, confidence_score: float) -> str:
        """Determine confidence level based on confidence score."""
        if confidence_score >= CONFIDENCE_HIGH:
            return "HIGH"
        elif confidence_score >= CONFIDENCE_MEDIUM:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_confidence_factors(
        self,
        profile_signals: ProfileSignals,
        profile_completeness_score: float,
        data_quality_score: float,
        consistency_score: float,
        role_fit_score: float
    ) -> List[str]:
        """Generate factors that contribute to the confidence level."""
        factors = []

        # Profile completeness factors
        if profile_completeness_score >= 0.8:
            factors.append("Profile data is comprehensive")
        elif profile_completeness_score >= 0.5:
            factors.append("Profile data is moderately complete")
        else:
            factors.append("Profile data is limited")

        # Data quality factors
        if data_quality_score >= 0.7:
            factors.append("Data from multiple reliable sources")
        elif data_quality_score >= 0.4:
            factors.append("Data from some reliable sources")
        else:
            factors.append("Limited data sources available")

        # Consistency factors
        if consistency_score >= 0.6:
            factors.append("Good consistency across data sources")
        elif consistency_score >= 0.3:
            factors.append("Moderate consistency across data sources")
        else:
            factors.append("Inconsistent information across sources")

        # Role fit factors
        if role_fit_score >= 0.7:
            factors.append("Strong alignment with role requirements")
        elif role_fit_score >= 0.4:
            factors.append("Moderate alignment with role requirements")
        else:
            factors.append("Limited alignment with role requirements")

        # Additional specific factors
        if len(profile_signals.aggregated_skills) >= 10:
            factors.append("Rich skill portfolio")
        elif len(profile_signals.aggregated_skills) < 5:
            factors.append("Limited skill information")

        if profile_signals.project_highlights:
            factors.append("Project experience provided")

        return factors

    def calculate_confidence_with_factors(
        self,
        profile_signals: ProfileSignals,
        role_fit_score: float,
        role_requirements: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate confidence with detailed breakdown of factors.

        Args:
            profile_signals: User's profile signals
            role_fit_score: Initial fit score for the role
            role_requirements: Requirements for the target role

        Returns:
            Dict with confidence score, level, factors, and detailed breakdown
        """
        confidence_score, confidence_level, confidence_factors = self.calculate_confidence(
            profile_signals, role_fit_score
        )

        # Calculate detailed breakdown
        profile_completeness = self._calculate_profile_completeness_score(profile_signals)
        data_quality = self._calculate_data_quality_score(profile_signals)
        consistency = self._calculate_consistency_score(profile_signals)

        return {
            'confidence_score': confidence_score,
            'confidence_level': confidence_level,
            'confidence_factors': confidence_factors,
            'breakdown': {
                'profile_completeness': profile_completeness,
                'data_quality': data_quality,
                'consistency': consistency,
                'role_fit': role_fit_score
            },
            'improvement_suggestions': self._generate_improvement_suggestions(
                profile_signals, profile_completeness, data_quality, consistency
            )
        }

    def _generate_improvement_suggestions(
        self,
        profile_signals: ProfileSignals,
        profile_completeness: float,
        data_quality: float,
        consistency: float
    ) -> List[str]:
        """Generate suggestions to improve confidence levels."""
        suggestions = []

        if profile_completeness < 0.6:
            suggestions.append("Add more comprehensive profile information")

        if data_quality < 0.5:
            suggestions.append("Include data from additional sources (e.g., GitHub, LinkedIn)")

        if consistency < 0.4:
            suggestions.append("Ensure consistency across different profile sources")

        if not profile_signals.project_highlights:
            suggestions.append("Add project highlights to demonstrate practical experience")

        if len(profile_signals.aggregated_skills) < 5:
            suggestions.append("Include more skills in your profile")

        return suggestions

    def explain_confidence_factors(
        self,
        profile_signals: ProfileSignals,
        role_fit_score: float
    ) -> Dict[str, Any]:
        """
        Explain what would improve confidence levels for the user.

        Args:
            profile_signals: User's profile signals
            role_fit_score: Initial fit score for the role

        Returns:
            Dict with confidence explanation and improvement suggestions
        """
        # Calculate current confidence
        current_confidence, _, _ = self.calculate_confidence(profile_signals, role_fit_score)

        # Calculate what each factor contributes
        profile_completeness = self._calculate_profile_completeness_score(profile_signals)
        data_quality = self._calculate_data_quality_score(profile_signals)
        consistency = self._calculate_consistency_score(profile_signals)

        # Generate specific explanations
        explanations = {
            'current_confidence': current_confidence,
            'factors_explanation': {},
            'improvement_paths': []
        }

        # Profile completeness explanation
        explanations['factors_explanation']['profile_completeness'] = {
            'score': profile_completeness,
            'explanation': self._explain_profile_completeness(profile_completeness, profile_signals)
        }

        # Data quality explanation
        explanations['factors_explanation']['data_quality'] = {
            'score': data_quality,
            'explanation': self._explain_data_quality(data_quality, profile_signals)
        }

        # Consistency explanation
        explanations['factors_explanation']['consistency'] = {
            'score': consistency,
            'explanation': self._explain_consistency(consistency, profile_signals)
        }

        # Generate improvement paths
        explanations['improvement_paths'] = self._generate_detailed_improvement_paths(
            profile_signals, profile_completeness, data_quality, consistency
        )

        return explanations

    def _explain_profile_completeness(
        self,
        score: float,
        profile_signals: ProfileSignals
    ) -> str:
        """Explain the profile completeness factor."""
        if score >= 0.8:
            return "Your profile is comprehensive with information from multiple sections."
        elif score >= 0.5:
            return "Your profile has moderate completeness but could benefit from additional information."
        else:
            return "Your profile has limited information. Adding more details would significantly improve recommendations."

    def _explain_data_quality(
        self,
        score: float,
        profile_signals: ProfileSignals
    ) -> str:
        """Explain the data quality factor."""
        if score >= 0.8:
            return "Data from multiple reliable sources provides high-quality signals."
        elif score >= 0.5:
            return "Data quality is moderate. More diverse sources would improve confidence."
        else:
            return "Limited data sources impact the quality of recommendations. Consider adding more profile data."

    def _explain_consistency(
        self,
        score: float,
        profile_signals: ProfileSignals
    ) -> str:
        """Explain the consistency factor."""
        if score >= 0.8:
            return "Information is consistent across different profile sources."
        elif score >= 0.5:
            return "Moderate consistency across profile sources. Aligning information would help."
        else:
            return "Inconsistent information across sources reduces confidence. Ensure profile data is aligned."

    def _generate_detailed_improvement_paths(
        self,
        profile_signals: ProfileSignals,
        profile_completeness: float,
        data_quality: float,
        consistency: float
    ) -> List[Dict[str, str]]:
        """
        Generate detailed improvement paths with specific actions.

        Returns:
            List of improvement paths with action and impact
        """
        improvement_paths = []

        # Profile completeness improvements
        if profile_completeness < 0.7:
            improvement_paths.append({
                'category': 'Profile Completeness',
                'action': 'Add more skills to your profile',
                'impact': 'High',
                'description': 'Adding 5-10 more relevant skills could improve confidence by 10-15%'
            })

            if not profile_signals.project_highlights:
                improvement_paths.append({
                    'category': 'Profile Completeness',
                    'action': 'Add project highlights',
                    'impact': 'High',
                    'description': 'Including 2-3 project examples would demonstrate practical experience'
                })

        # Data quality improvements
        if data_quality < 0.7:
            improvement_paths.append({
                'category': 'Data Quality',
                'action': 'Connect additional profile sources',
                'impact': 'High',
                'description': 'Linking GitHub, LinkedIn, or portfolio would provide additional signals'
            })

        # Consistency improvements
        if consistency < 0.6:
            improvement_paths.append({
                'category': 'Consistency',
                'action': 'Align skill information across profiles',
                'impact': 'Medium',
                'description': 'Ensure skills listed on resume match those on LinkedIn/GitHub'
            })

        # Experience information
        experience_summary = profile_signals.experience_summary
        if isinstance(experience_summary, dict):
            total_years = experience_summary.get('total_years', 0.0)
        else:
            total_years = getattr(experience_summary, 'total_years', 0.0)

        if total_years == 0:
            improvement_paths.append({
                'category': 'Profile Completeness',
                'action': 'Add years of experience',
                'impact': 'Medium',
                'description': 'Specifying your years of experience would improve profile completeness'
            })

        return improvement_paths


# Global confidence calculator instance
confidence_calculator = ConfidenceCalculator()


def get_confidence_calculator() -> ConfidenceCalculator:
    """Get the global confidence calculator instance"""
    return confidence_calculator