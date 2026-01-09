"""KeywordSuggestion entity for Resume Analyzer Core"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import uuid


@dataclass
class KeywordSuggestion:
    """Represents a suggested keyword for resume improvement"""

    suggestion_id: str
    analysis_id: str
    keyword: str
    relevance_score: float  # How relevant the keyword is (0-1)
    category: str  # Technical, SoftSkill, IndustrySpecific
    justification: str  # Why this keyword is suggested
    role_alignment: str  # Which roles this keyword aligns with
    created_timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Validate the KeywordSuggestion entity after initialization"""
        if not self.keyword.strip():
            raise ValueError("keyword must be non-empty")

        if not 0 <= self.relevance_score <= 1:
            raise ValueError("relevance_score must be between 0 and 1")

        valid_categories = {"Technical", "SoftSkill", "IndustrySpecific"}
        if self.category not in valid_categories:
            raise ValueError(f"category must be one of {valid_categories}")

        if not self.justification.strip():
            raise ValueError("justification must be non-empty")

    @classmethod
    def create_new(cls, analysis_id: str, keyword: str, relevance_score: float,
                   category: str, justification: str, role_alignment: str) -> 'KeywordSuggestion':
        """Create a new KeywordSuggestion entity with generated ID and timestamp"""
        return cls(
            suggestion_id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            keyword=keyword,
            relevance_score=relevance_score,
            category=category,
            justification=justification,
            role_alignment=role_alignment,
            created_timestamp=datetime.now()
        )