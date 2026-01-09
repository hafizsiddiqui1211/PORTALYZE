"""Alignment Result entity for Resume Analyzer Core"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import uuid


@dataclass
class AlignmentResult:
    """Represents the alignment analysis between resume and profile data"""

    alignment_id: str
    overall_score: float  # 0-100 percentage
    skill_alignment: Dict[str, float]  # Skill-to-skill mapping with scores
    experience_alignment: Dict[str, float]  # Experience-to-experience mapping with scores
    project_alignment: Dict[str, float]  # Project-to-project mapping with scores
    discrepancies: List[str]  # Notable differences between resume and profiles
    recommendations: List[str]  # Alignment improvement suggestions
    analysis_timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Validate the AlignmentResult entity after initialization"""
        if not self.alignment_id:
            raise ValueError("alignment_id cannot be empty")

        if not 0 <= self.overall_score <= 100:
            raise ValueError("overall_score must be between 0 and 100")

        if not isinstance(self.skill_alignment, dict):
            raise ValueError("skill_alignment must be a dictionary")

        if not isinstance(self.experience_alignment, dict):
            raise ValueError("experience_alignment must be a dictionary")

        if not isinstance(self.project_alignment, dict):
            raise ValueError("project_alignment must be a dictionary")

        if not isinstance(self.discrepancies, list):
            raise ValueError("discrepancies must be a list")

        if not isinstance(self.recommendations, list):
            raise ValueError("recommendations must be a list")

        # Validate alignment scores
        for key, score in self.skill_alignment.items():
            if not 0 <= score <= 100:
                raise ValueError(f"Skill alignment score for {key} must be between 0 and 100")

        for key, score in self.experience_alignment.items():
            if not 0 <= score <= 100:
                raise ValueError(f"Experience alignment score for {key} must be between 0 and 100")

        for key, score in self.project_alignment.items():
            if not 0 <= score <= 100:
                raise ValueError(f"Project alignment score for {key} must be between 0 and 100")

    @classmethod
    def create_new(
        cls,
        overall_score: float,
        skill_alignment: Optional[Dict[str, float]] = None,
        experience_alignment: Optional[Dict[str, float]] = None,
        project_alignment: Optional[Dict[str, float]] = None,
        discrepancies: Optional[List[str]] = None,
        recommendations: Optional[List[str]] = None
    ) -> 'AlignmentResult':
        """
        Create a new AlignmentResult entity with generated ID and timestamp.

        Args:
            overall_score: Overall alignment percentage (0-100)
            skill_alignment: Skill-to-skill alignment scores
            experience_alignment: Experience-to-experience alignment scores
            project_alignment: Project-to-project alignment scores
            discrepancies: Notable differences between resume and profiles
            recommendations: Alignment improvement suggestions

        Returns:
            New AlignmentResult instance
        """
        if skill_alignment is None:
            skill_alignment = {}

        if experience_alignment is None:
            experience_alignment = {}

        if project_alignment is None:
            project_alignment = {}

        if discrepancies is None:
            discrepancies = []

        if recommendations is None:
            recommendations = []

        return cls(
            alignment_id=str(uuid.uuid4()),
            overall_score=overall_score,
            skill_alignment=skill_alignment,
            experience_alignment=experience_alignment,
            project_alignment=project_alignment,
            discrepancies=discrepancies,
            recommendations=recommendations,
            analysis_timestamp=datetime.now()
        )

    def get_skill_alignment_percentage(self) -> float:
        """
        Calculate the average skill alignment percentage.

        Returns:
            Average skill alignment score
        """
        if not self.skill_alignment:
            return 0.0

        total_score = sum(self.skill_alignment.values())
        return total_score / len(self.skill_alignment) if self.skill_alignment else 0.0

    def get_experience_alignment_percentage(self) -> float:
        """
        Calculate the average experience alignment percentage.

        Returns:
            Average experience alignment score
        """
        if not self.experience_alignment:
            return 0.0

        total_score = sum(self.experience_alignment.values())
        return total_score / len(self.experience_alignment) if self.experience_alignment else 0.0

    def get_project_alignment_percentage(self) -> float:
        """
        Calculate the average project alignment percentage.

        Returns:
            Average project alignment score
        """
        if not self.project_alignment:
            return 0.0

        total_score = sum(self.project_alignment.values())
        return total_score / len(self.project_alignment) if self.project_alignment else 0.0

    def get_alignment_quality_level(self) -> str:
        """
        Determine the alignment quality level based on overall score.

        Returns:
            Quality level: "EXCELLENT", "GOOD", "FAIR", or "POOR"
        """
        if self.overall_score >= 85:
            return "EXCELLENT"
        elif self.overall_score >= 70:
            return "GOOD"
        elif self.overall_score >= 50:
            return "FAIR"
        else:
            return "POOR"

    def has_significant_discrepancies(self) -> bool:
        """
        Check if there are significant discrepancies between resume and profiles.

        Returns:
            True if there are significant discrepancies, False otherwise
        """
        return len(self.discrepancies) > 3

    def has_actionable_recommendations(self) -> bool:
        """
        Check if there are actionable recommendations for alignment.

        Returns:
            True if there are recommendations, False otherwise
        """
        return len(self.recommendations) > 0

    def get_alignment_summary(self) -> Dict[str, float]:
        """
        Get a summary of alignment scores.

        Returns:
            Dictionary with alignment category scores
        """
        return {
            "overall": self.overall_score,
            "skills": self.get_skill_alignment_percentage(),
            "experience": self.get_experience_alignment_percentage(),
            "projects": self.get_project_alignment_percentage()
        }

    def get_strongest_alignment_category(self) -> str:
        """
        Determine which category has the strongest alignment.

        Returns:
            Category with the highest alignment score
        """
        alignment_scores = {
            "skills": self.get_skill_alignment_percentage(),
            "experience": self.get_experience_alignment_percentage(),
            "projects": self.get_project_alignment_percentage()
        }

        return max(alignment_scores, key=alignment_scores.get)

    def get_weakest_alignment_category(self) -> str:
        """
        Determine which category has the weakest alignment.

        Returns:
            Category with the lowest alignment score
        """
        alignment_scores = {
            "skills": self.get_skill_alignment_percentage(),
            "experience": self.get_experience_alignment_percentage(),
            "projects": self.get_project_alignment_percentage()
        }

        return min(alignment_scores, key=alignment_scores.get)

    def get_recommendation_by_category(self, category: str) -> List[str]:
        """
        Get recommendations related to a specific category.

        Args:
            category: Category to filter recommendations ("skills", "experience", "projects")

        Returns:
            List of recommendations related to the category
        """
        # This is a simplified implementation - in practice, recommendations might be tagged
        # with categories to allow for more precise filtering
        category_keywords = {
            "skills": ["skill", "technology", "capability", "competency"],
            "experience": ["experience", "role", "position", "job", "worked"],
            "projects": ["project", "repository", "contribution", "work"]
        }

        if category.lower() not in category_keywords:
            return []

        keywords = category_keywords[category.lower()]
        filtered_recommendations = []

        for recommendation in self.recommendations:
            if any(keyword.lower() in recommendation.lower() for keyword in keywords):
                filtered_recommendations.append(recommendation)

        return filtered_recommendations

    def get_discrepancy_by_category(self, category: str) -> List[str]:
        """
        Get discrepancies related to a specific category.

        Args:
            category: Category to filter discrepancies ("skills", "experience", "projects")

        Returns:
            List of discrepancies related to the category
        """
        # This is a simplified implementation - in practice, discrepancies might be tagged
        # with categories to allow for more precise filtering
        category_keywords = {
            "skills": ["skill", "technology", "capability", "competency"],
            "experience": ["experience", "role", "position", "job", "worked"],
            "projects": ["project", "repository", "contribution", "work"]
        }

        if category.lower() not in category_keywords:
            return []

        keywords = category_keywords[category.lower()]
        filtered_discrepancies = []

        for discrepancy in self.discrepancies:
            if any(keyword.lower() in discrepancy.lower() for keyword in keywords):
                filtered_discrepancies.append(discrepancy)

        return filtered_discrepancies

    def get_actionable_insights(self) -> List[str]:
        """
        Get a list of actionable insights from the alignment analysis.

        Returns:
            List of actionable insights
        """
        insights = []

        if self.has_significant_discrepancies():
            insights.append(f"Found {len(self.discrepancies)} discrepancies between resume and profiles")
        else:
            insights.append("Resume and profile information are well-aligned")

        if self.has_actionable_recommendations():
            insights.append(f"Consider {len(self.recommendations)} alignment improvement recommendations")

        insights.append(f"Overall alignment score: {self.overall_score}/100 ({self.get_alignment_quality_level()})")

        strongest = self.get_strongest_alignment_category()
        weakest = self.get_weakest_alignment_category()
        insights.append(f"Strongest alignment in: {strongest}, Weakest in: {weakest}")

        return insights

    def to_dict(self) -> dict:
        """
        Convert the AlignmentResult to a dictionary representation.

        Returns:
            Dictionary representation of the AlignmentResult
        """
        return {
            "alignment_id": self.alignment_id,
            "overall_score": self.overall_score,
            "skill_alignment": self.skill_alignment,
            "experience_alignment": self.experience_alignment,
            "project_alignment": self.project_alignment,
            "discrepancies": self.discrepancies,
            "recommendations": self.recommendations,
            "analysis_timestamp": self.analysis_timestamp.isoformat() if self.analysis_timestamp else None
        }