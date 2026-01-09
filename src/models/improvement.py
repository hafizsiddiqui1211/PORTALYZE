"""Improvement Suggestion entity for Resume Analyzer Core"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import uuid
from src.utils.constants import SUPPORTED_PROFILE_TYPES


@dataclass
class ImprovementSuggestion:
    """Represents an improvement suggestion for a profile"""

    suggestion_id: str
    profile_analysis_id: str
    category: str  # CONTENT, FORMATTING, VISIBILITY, ALIGNMENT, TECHNICAL
    priority: str  # HIGH, MEDIUM, LOW
    suggestion_text: str
    rationale: str
    example: Optional[str] = None
    affected_section: Optional[str] = None
    created_timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Validate the ImprovementSuggestion entity after initialization"""
        if not self.suggestion_id:
            raise ValueError("suggestion_id cannot be empty")

        if not self.profile_analysis_id:
            raise ValueError("profile_analysis_id cannot be empty")

        # Validate category
        valid_categories = ["CONTENT", "FORMATTING", "VISIBILITY", "ALIGNMENT", "TECHNICAL"]
        if self.category not in valid_categories:
            raise ValueError(f"category must be one of: {', '.join(valid_categories)}")

        # Validate priority
        valid_priorities = ["HIGH", "MEDIUM", "LOW"]
        if self.priority not in valid_priorities:
            raise ValueError(f"priority must be one of: {', '.join(valid_priorities)}")

        # Validate suggestion text
        if not self.suggestion_text or not self.suggestion_text.strip():
            raise ValueError("suggestion_text cannot be empty")

        # Validate rationale
        if not self.rationale or not self.rationale.strip():
            raise ValueError("rationale cannot be empty")

    @classmethod
    def create_new(
        cls,
        profile_analysis_id: str,
        category: str,
        priority: str,
        suggestion_text: str,
        rationale: str,
        example: Optional[str] = None,
        affected_section: Optional[str] = None
    ) -> 'ImprovementSuggestion':
        """
        Create a new ImprovementSuggestion entity with generated ID and timestamp.

        Args:
            profile_analysis_id: Foreign key to ProfileAnalysis
            category: Category of suggestion (CONTENT, FORMATTING, VISIBILITY, etc.)
            priority: Priority level (HIGH, MEDIUM, LOW)
            suggestion_text: The actionable suggestion
            rationale: Why this suggestion matters
            example: Example of improvement (optional)
            affected_section: Which profile section this affects (optional)

        Returns:
            New ImprovementSuggestion instance
        """
        return cls(
            suggestion_id=str(uuid.uuid4()),
            profile_analysis_id=profile_analysis_id,
            category=category,
            priority=priority,
            suggestion_text=suggestion_text,
            rationale=rationale,
            example=example,
            affected_section=affected_section,
            created_timestamp=datetime.now()
        )

    def is_high_priority(self) -> bool:
        """Check if this is a high priority suggestion."""
        return self.priority == "HIGH"

    def is_medium_priority(self) -> bool:
        """Check if this is a medium priority suggestion."""
        return self.priority == "MEDIUM"

    def is_low_priority(self) -> bool:
        """Check if this is a low priority suggestion."""
        return self.priority == "LOW"

    def is_content_suggestion(self) -> bool:
        """Check if this is a content-related suggestion."""
        return self.category == "CONTENT"

    def is_formatting_suggestion(self) -> bool:
        """Check if this is a formatting-related suggestion."""
        return self.category == "FORMATTING"

    def is_visibility_suggestion(self) -> bool:
        """Check if this is a visibility-related suggestion."""
        return self.category == "VISIBILITY"

    def is_alignment_suggestion(self) -> bool:
        """Check if this is an alignment-related suggestion."""
        return self.category == "ALIGNMENT"

    def is_technical_suggestion(self) -> bool:
        """Check if this is a technical-related suggestion."""
        return self.category == "TECHNICAL"

    def to_dict(self) -> dict:
        """
        Convert the ImprovementSuggestion to a dictionary representation.

        Returns:
            Dictionary representation of the ImprovementSuggestion
        """
        return {
            "suggestion_id": self.suggestion_id,
            "profile_analysis_id": self.profile_analysis_id,
            "category": self.category,
            "priority": self.priority,
            "suggestion_text": self.suggestion_text,
            "rationale": self.rationale,
            "example": self.example,
            "affected_section": self.affected_section,
            "created_timestamp": self.created_timestamp.isoformat() if self.created_timestamp else None
        }

    def get_priority_score(self) -> int:
        """
        Get a numeric score for the priority level (higher number = higher priority).

        Returns:
            Priority score (HIGH=3, MEDIUM=2, LOW=1)
        """
        priority_scores = {
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }
        return priority_scores.get(self.priority, 0)

    def get_category_weight(self) -> float:
        """
        Get a weight for the category (for ranking purposes).

        Returns:
            Category weight
        """
        # Different categories might have different weights depending on context
        category_weights = {
            "CONTENT": 1.0,    # Core content improvements are most important
            "ALIGNMENT": 0.9,  # Resume-profile alignment is highly valuable
            "VISIBILITY": 0.8, # Making profile more discoverable
            "TECHNICAL": 0.7,  # Technical improvements
            "FORMATTING": 0.6  # Formatting improvements
        }
        return category_weights.get(self.category, 0.5)