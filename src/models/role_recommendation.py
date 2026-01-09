"""Role recommendation model for job role recommender"""

from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class RecommendedRole(BaseModel):
    """A single recommended role with details"""
    role_id: str
    title: str
    industry: str
    seniority_level: str  # JUNIOR, MID, SENIOR
    fit_score: float  # 0.0 to 1.0
    justification: Dict[str, str]  # skill_alignment, project_relevance, etc.
    confidence_factors: List[str]
    skill_gaps: List[str]
    improvement_suggestions: List[str]


class RoleRecommendation(BaseModel):
    """
    Complete role recommendation response containing multiple roles
    and overall analysis.
    """
    recommendation_id: str
    session_id: str
    roles: List[RecommendedRole]
    overall_confidence: float  # 0.0 to 1.0
    confidence_factors: List[str]
    recommendation_timestamp: datetime
    industry: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }