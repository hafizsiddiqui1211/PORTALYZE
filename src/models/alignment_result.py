"""Alignment Result entity for Resume Analyzer Core"""
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import uuid


@dataclass
class AlignmentResult:
    """Represents the alignment analysis between resume and profile data"""

    alignment_id: str
    overall_score: float  # 0-100 percentage
    skill_alignment: Dict[str, float]  # Skill alignment scores by platform
    experience_alignment: Dict[str, float]  # Experience alignment scores by platform
    project_alignment: Dict[str, float]  # Project alignment scores by platform
    discrepancies: List[str]  # Notable differences between resume and profiles
    recommendations: List[str]  # Alignment improvement suggestions
    analysis_timestamp: datetime

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

        # Validate alignment scores are between 0 and 100
        for platform, score in self.skill_alignment.items():
            if not 0 <= score <= 100:
                raise ValueError(f"Skill alignment score for {platform} must be between 0 and 100")

        for platform, score in self.experience_alignment.items():
            if not 0 <= score <= 100:
                raise ValueError(f"Experience alignment score for {platform} must be between 0 and 100")

        for platform, score in self.project_alignment.items():
            if not 0 <= score <= 100:
                raise ValueError(f"Project alignment score for {platform} must be between 0 and 100")

    @classmethod
    def create_new(
        cls,
        overall_score: float,
        skill_alignment: Dict[str, float],
        experience_alignment: Dict[str, float],
        project_alignment: Dict[str, float],
        discrepancies: List[str],
        recommendations: List[str]
    ) -> 'AlignmentResult':
        """
        Create a new AlignmentResult entity with generated ID and timestamp.

        Args:
            overall_score: Overall alignment score (0-100)
            skill_alignment: Skill alignment scores by platform
            experience_alignment: Experience alignment scores by platform
            project_alignment: Project alignment scores by platform
            discrepancies: List of notable differences between resume and profiles
            recommendations: List of alignment improvement suggestions

        Returns:
            New AlignmentResult instance
        """
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

    def get_highest_alignment_platform(self) -> str:
        """
        Get the platform with the highest overall alignment score.

        Returns:
            Platform name with highest alignment
        """
        # Calculate average alignment score for each platform
        platform_scores = {}

        for platform in set(self.skill_alignment.keys()) | set(self.experience_alignment.keys()) | set(self.project_alignment.keys()):
            skill_score = self.skill_alignment.get(platform, 0)
            experience_score = self.experience_alignment.get(platform, 0)
            project_score = self.project_alignment.get(platform, 0)

            # Average the three scores for this platform
            avg_score = (skill_score + experience_score + project_score) / 3
            platform_scores[platform] = avg_score

        if not platform_scores:
            return "No platforms analyzed"

        # Return the platform with the highest average score
        return max(platform_scores, key=platform_scores.get)

    def get_lowest_alignment_platform(self) -> str:
        """
        Get the platform with the lowest overall alignment score.

        Returns:
            Platform name with lowest alignment
        """
        # Calculate average alignment score for each platform
        platform_scores = {}

        for platform in set(self.skill_alignment.keys()) | set(self.experience_alignment.keys()) | set(self.project_alignment.keys()):
            skill_score = self.skill_alignment.get(platform, 0)
            experience_score = self.experience_alignment.get(platform, 0)
            project_score = self.project_alignment.get(platform, 0)

            # Average the three scores for this platform
            avg_score = (skill_score + experience_score + project_score) / 3
            platform_scores[platform] = avg_score

        if not platform_scores:
            return "No platforms analyzed"

        # Return the platform with the lowest average score
        return min(platform_scores, key=platform_scores.get)

    def get_skill_gaps(self) -> List[str]:
        """
        Get a list of platforms with significant skill alignment gaps (> 30 points difference).

        Returns:
            List of platform names with significant skill gaps
        """
        significant_gaps = []

        for platform, score in self.skill_alignment.items():
            # Consider a gap significant if the score is below 70%
            if score < 70:
                significant_gaps.append(platform)

        return significant_gaps

    def get_experience_gaps(self) -> List[str]:
        """
        Get a list of platforms with significant experience alignment gaps (> 30 points difference).

        Returns:
            List of platform names with significant experience gaps
        """
        significant_gaps = []

        for platform, score in self.experience_alignment.items():
            # Consider a gap significant if the score is below 70%
            if score < 70:
                significant_gaps.append(platform)

        return significant_gaps

    def get_project_gaps(self) -> List[str]:
        """
        Get a list of platforms with significant project alignment gaps (> 30 points difference).

        Returns:
            List of platform names with significant project gaps
        """
        significant_gaps = []

        for platform, score in self.project_alignment.items():
            # Consider a gap significant if the score is below 70%
            if score < 70:
                significant_gaps.append(platform)

        return significant_gaps

    def has_critical_discrepancies(self) -> bool:
        """
        Check if there are critical discrepancies that need immediate attention.

        Returns:
            True if critical discrepancies exist, False otherwise
        """
        # Look for discrepancies that mention critical information mismatches
        critical_keywords = [
            "experience", "role", "position", "company", "dates", "employment", "job"
        ]

        for discrepancy in self.discrepancies:
            if any(keyword in discrepancy.lower() for keyword in critical_keywords):
                return True

        return False

    def get_priority_recommendations(self) -> List[str]:
        """
        Get recommendations that should be prioritized based on severity.

        Returns:
            List of high-priority recommendations
        """
        priority_keywords = [
            "critical", "essential", "important", "must", "high priority",
            "urgently", "immediately", "significantly improve"
        ]

        priority_recs = []
        for recommendation in self.recommendations:
            if any(keyword in recommendation.lower() for keyword in priority_keywords):
                priority_recs.append(recommendation)

        # If no explicitly marked priority recommendations, return recommendations
        # related to critical sections
        if not priority_recs:
            for recommendation in self.recommendations:
                if any(keyword in recommendation.lower() for keyword in ["skills", "experience", "projects", "summary"]):
                    priority_recs.append(recommendation)

        return priority_recs

    def get_alignment_summary(self) -> Dict[str, float]:
        """
        Get a summary of alignment scores by category.

        Returns:
            Dictionary with average scores by category
        """
        return {
            "average_skill_alignment": self._get_average_score(self.skill_alignment),
            "average_experience_alignment": self._get_average_score(self.experience_alignment),
            "average_project_alignment": self._get_average_score(self.project_alignment)
        }

    def _get_average_score(self, score_dict: Dict[str, float]) -> float:
        """
        Calculate the average score from a dictionary of scores.

        Args:
            score_dict: Dictionary of platform-score pairs

        Returns:
            Average score
        """
        if not score_dict:
            return 0.0

        return sum(score_dict.values()) / len(score_dict)

    def get_alignment_quality_level(self) -> str:
        """
        Determine the overall alignment quality level.

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

    def get_platform_alignment_details(self, platform: str) -> Dict[str, float]:
        """
        Get detailed alignment scores for a specific platform.

        Args:
            platform: Platform name to get details for

        Returns:
            Dictionary with detailed scores for the platform
        """
        return {
            "skill_score": self.skill_alignment.get(platform, 0),
            "experience_score": self.experience_alignment.get(platform, 0),
            "project_score": self.project_alignment.get(platform, 0),
            "average_score": (
                self.skill_alignment.get(platform, 0) +
                self.experience_alignment.get(platform, 0) +
                self.project_alignment.get(platform, 0)
            ) / 3 if platform in self.skill_alignment or platform in self.experience_alignment or platform in self.project_alignment else 0
        }

    def get_total_discrepancies_count(self) -> int:
        """
        Get the total number of discrepancies identified.

        Returns:
            Number of discrepancies
        """
        return len(self.discrepancies)

    def get_total_recommendations_count(self) -> int:
        """
        Get the total number of recommendations provided.

        Returns:
            Number of recommendations
        """
        return len(self.recommendations)

    def to_dict(self) -> Dict:
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
            "analysis_timestamp": self.analysis_timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'AlignmentResult':
        """
        Create an AlignmentResult from a dictionary.

        Args:
            data: Dictionary containing alignment result data

        Returns:
            AlignmentResult instance
        """
        return cls(
            alignment_id=data["alignment_id"],
            overall_score=data["overall_score"],
            skill_alignment=data["skill_alignment"],
            experience_alignment=data["experience_alignment"],
            project_alignment=data["project_alignment"],
            discrepancies=data["discrepancies"],
            recommendations=data["recommendations"],
            analysis_timestamp=datetime.fromisoformat(data["analysis_timestamp"])
        )

    def get_actionable_insights(self) -> List[str]:
        """
        Get actionable insights from the alignment analysis.

        Returns:
            List of actionable insights
        """
        insights = []

        if self.has_critical_discrepancies():
            insights.append("⚠️ Critical discrepancies found between resume and profiles - address immediately")

        quality_level = self.get_alignment_quality_level()
        insights.append(f"📈 Overall alignment quality: {quality_level}")

        best_platform = self.get_highest_alignment_platform()
        worst_platform = self.get_lowest_alignment_platform()
        insights.append(f"🏆 Best aligned platform: {best_platform}")
        insights.append(f"📉 Lowest aligned platform: {worst_platform}")

        skill_gaps = self.get_skill_gaps()
        if skill_gaps:
            insights.append(f"🔍 Platforms with skill gaps: {', '.join(skill_gaps)}")

        priority_recs = self.get_priority_recommendations()
        if priority_recs:
            insights.append(f"⚡ {len(priority_recs)} high-priority recommendations available")

        return insights