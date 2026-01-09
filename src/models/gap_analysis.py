"""Gap analysis model for job role recommender"""

from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class SkillGap(BaseModel):
    """Represents a single skill gap identified for a role"""
    skill_name: str
    importance_level: str  # CRITICAL, IMPORTANT, NICE_TO_HAVE
    current_level: float  # 0.0 to 1.0
    target_level: float  # 0.0 to 1.0
    improvement_suggestions: List[str]
    priority: int  # 1 (highest) to n (lowest)


class GapAnalysis(BaseModel):
    """
    Complete gap analysis for a recommended role showing missing skills
    and improvement suggestions.
    """
    gap_id: str
    role_id: str
    session_id: str
    missing_skills: List[SkillGap]
    improvement_suggestions: List[str]
    priority_areas: List[str]  # Most important gaps to address first
    analysis_timestamp: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }