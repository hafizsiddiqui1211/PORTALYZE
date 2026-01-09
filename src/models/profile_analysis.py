"""Profile Analysis entity for Resume Analyzer Core"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import uuid
from src.models.improvement import ImprovementSuggestion
from src.utils.constants import SUPPORTED_PROFILE_TYPES


@dataclass
class ProfileAnalysis:
    """Represents the analysis results for a single profile"""

    profile_analysis_id: str
    profile_id: str
    profile_type: str  # LINKEDIN, GITHUB, or PORTFOLIO
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[ImprovementSuggestion]
    clarity_score: float  # 0-100
    impact_score: float   # 0-100
    analysis_timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Validate the ProfileAnalysis entity after initialization"""
        if not self.profile_analysis_id:
            raise ValueError("profile_analysis_id cannot be empty")

        if not self.profile_id:
            raise ValueError("profile_id cannot be empty")

        if self.profile_type not in SUPPORTED_PROFILE_TYPES:
            raise ValueError(f"profile_type must be one of: {', '.join(SUPPORTED_PROFILE_TYPES)}")

        if not isinstance(self.strengths, list):
            raise ValueError("strengths must be a list")

        if not isinstance(self.weaknesses, list):
            raise ValueError("weaknesses must be a list")

        if not isinstance(self.suggestions, list):
            raise ValueError("suggestions must be a list")

        if not 0 <= self.clarity_score <= 100:
            raise ValueError("clarity_score must be between 0 and 100")

        if not 0 <= self.impact_score <= 100:
            raise ValueError("impact_score must be between 0 and 100")

        # Validate all suggestions have the correct profile_analysis_id
        for suggestion in self.suggestions:
            if suggestion.profile_analysis_id != self.profile_analysis_id:
                raise ValueError(f"Suggestion {suggestion.suggestion_id} has incorrect profile_analysis_id")

    @classmethod
    def create_new(
        cls,
        profile_id: str,
        profile_type: str,
        strengths: Optional[List[str]] = None,
        weaknesses: Optional[List[str]] = None,
        suggestions: Optional[List[ImprovementSuggestion]] = None,
        clarity_score: float = 0.0,
        impact_score: float = 0.0
    ) -> 'ProfileAnalysis':
        """
        Create a new ProfileAnalysis entity with generated ID and timestamp.

        Args:
            profile_id: Foreign key to ProfileData
            profile_type: Type of profile (LINKEDIN, GITHUB, or PORTFOLIO)
            strengths: List of identified strengths
            weaknesses: List of identified weaknesses
            suggestions: List of improvement suggestions
            clarity_score: Profile clarity rating (0-100)
            impact_score: Profile impact rating (0-100)

        Returns:
            New ProfileAnalysis instance
        """
        if strengths is None:
            strengths = []

        if weaknesses is None:
            weaknesses = []

        if suggestions is None:
            suggestions = []

        return cls(
            profile_analysis_id=str(uuid.uuid4()),
            profile_id=profile_id,
            profile_type=profile_type,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            clarity_score=clarity_score,
            impact_score=impact_score,
            analysis_timestamp=datetime.now()
        )

    def is_linkedin_analysis(self) -> bool:
        """Check if this is a LinkedIn profile analysis."""
        return self.profile_type == "LINKEDIN"

    def is_github_analysis(self) -> bool:
        """Check if this is a GitHub profile analysis."""
        return self.profile_type == "GITHUB"

    def is_portfolio_analysis(self) -> bool:
        """Check if this is a portfolio profile analysis."""
        return self.profile_type == "PORTFOLIO"

    def get_high_priority_suggestions(self) -> List[ImprovementSuggestion]:
        """Get all high priority suggestions."""
        return [s for s in self.suggestions if s.is_high_priority()]

    def get_medium_priority_suggestions(self) -> List[ImprovementSuggestion]:
        """Get all medium priority suggestions."""
        return [s for s in self.suggestions if s.is_medium_priority()]

    def get_low_priority_suggestions(self) -> List[ImprovementSuggestion]:
        """Get all low priority suggestions."""
        return [s for s in self.suggestions if s.is_low_priority()]

    def get_content_suggestions(self) -> List[ImprovementSuggestion]:
        """Get all content-related suggestions."""
        return [s for s in self.suggestions if s.is_content_suggestion()]

    def get_formatting_suggestions(self) -> List[ImprovementSuggestion]:
        """Get all formatting-related suggestions."""
        return [s for s in self.suggestions if s.is_formatting_suggestion()]

    def get_visibility_suggestions(self) -> List[ImprovementSuggestion]:
        """Get all visibility-related suggestions."""
        return [s for s in self.suggestions if s.is_visibility_suggestion()]

    def get_alignment_suggestions(self) -> List[ImprovementSuggestion]:
        """Get all alignment-related suggestions."""
        return [s for s in self.suggestions if s.is_alignment_suggestion()]

    def get_technical_suggestions(self) -> List[ImprovementSuggestion]:
        """Get all technical-related suggestions."""
        return [s for s in self.suggestions if s.is_technical_suggestion()]

    def get_total_suggestions_count(self) -> int:
        """Get the total number of suggestions."""
        return len(self.suggestions)

    def get_suggestions_by_priority(self) -> dict:
        """Get a count of suggestions by priority level."""
        return {
            "HIGH": len(self.get_high_priority_suggestions()),
            "MEDIUM": len(self.get_medium_priority_suggestions()),
            "LOW": len(self.get_low_priority_suggestions())
        }

    def get_suggestions_by_category(self) -> dict:
        """Get a count of suggestions by category."""
        return {
            "CONTENT": len(self.get_content_suggestions()),
            "FORMATTING": len(self.get_formatting_suggestions()),
            "VISIBILITY": len(self.get_visibility_suggestions()),
            "ALIGNMENT": len(self.get_alignment_suggestions()),
            "TECHNICAL": len(self.get_technical_suggestions())
        }

    def get_overall_score(self) -> float:
        """
        Calculate an overall score based on clarity and impact.

        Returns:
            Average of clarity and impact scores
        """
        return (self.clarity_score + self.impact_score) / 2.0

    def get_profile_quality_level(self) -> str:
        """
        Determine the profile quality level based on scores.

        Returns:
            Quality level: "EXCELLENT", "GOOD", "FAIR", or "POOR"
        """
        overall_score = self.get_overall_score()

        if overall_score >= 80:
            return "EXCELLENT"
        elif overall_score >= 60:
            return "GOOD"
        elif overall_score >= 40:
            return "FAIR"
        else:
            return "POOR"

    def has_significant_weaknesses(self) -> bool:
        """
        Check if the profile has significant weaknesses that need attention.

        Returns:
            True if there are significant weaknesses, False otherwise
        """
        # Consider it significant if there are more than 3 weaknesses or if the impact score is low
        return len(self.weaknesses) > 3 or self.impact_score < 50

    def has_notable_strengths(self) -> bool:
        """
        Check if the profile has notable strengths.

        Returns:
            True if there are notable strengths, False otherwise
        """
        # Consider it notable if there are more than 2 strengths or if the clarity score is high
        return len(self.strengths) > 2 or self.clarity_score > 70

    def get_actionable_insights(self) -> List[str]:
        """
        Get a list of actionable insights from the analysis.

        Returns:
            List of actionable insights
        """
        insights = []

        if self.has_notable_strengths():
            insights.append(f"Profile has {len(self.strengths)} notable strengths")

        if self.has_significant_weaknesses():
            insights.append(f"Profile has {len(self.weaknesses)} areas needing improvement")

        if self.get_high_priority_suggestions():
            insights.append(f"Consider addressing {len(self.get_high_priority_suggestions())} high-priority suggestions")

        return insights

    def to_dict(self) -> dict:
        """
        Convert the ProfileAnalysis to a dictionary representation.

        Returns:
            Dictionary representation of the ProfileAnalysis
        """
        return {
            "profile_analysis_id": self.profile_analysis_id,
            "profile_id": self.profile_id,
            "profile_type": self.profile_type,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "suggestions": [s.to_dict() for s in self.suggestions],
            "clarity_score": self.clarity_score,
            "impact_score": self.impact_score,
            "analysis_timestamp": self.analysis_timestamp.isoformat() if self.analysis_timestamp else None
        }