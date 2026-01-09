"""AnalysisResult entity for Resume Analyzer Core"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


@dataclass
class AnalysisResult:
    """Represents the results of a resume analysis"""

    analysis_id: str
    resume_id: str
    ats_score: float  # ATS compatibility percentage (0-100)
    strengths: List[str]  # Identified strengths in the resume
    weaknesses: List[str]  # Identified weaknesses in the resume
    section_feedback: Dict[str, str]  # Feedback organized by resume sections
    overall_feedback: str  # Summary feedback
    confidence_level: float  # Confidence in the analysis (0-1)
    analysis_timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Validate the AnalysisResult entity after initialization"""
        if not 0 <= self.ats_score <= 100:
            raise ValueError("ats_score must be between 0 and 100")

        if not self.strengths or not self.weaknesses:
            raise ValueError("strengths and weaknesses arrays must have at least 1 item")

        required_sections = {'experience', 'skills', 'education'}
        if not required_sections.issubset(self.section_feedback.keys()):
            raise ValueError(f"section_feedback must include at least {required_sections} keys")

        if not 0 <= self.confidence_level <= 1:
            raise ValueError("confidence_level must be between 0 and 1")

    @classmethod
    def create_new(cls, resume_id: str, ats_score: float, strengths: List[str],
                   weaknesses: List[str], section_feedback: Dict[str, str],
                   overall_feedback: str, confidence_level: float) -> 'AnalysisResult':
        """Create a new AnalysisResult entity with generated ID and timestamp"""
        return cls(
            analysis_id=str(uuid.uuid4()),
            resume_id=resume_id,
            ats_score=ats_score,
            strengths=strengths,
            weaknesses=weaknesses,
            section_feedback=section_feedback,
            overall_feedback=overall_feedback,
            confidence_level=confidence_level,
            analysis_timestamp=datetime.now()
        )