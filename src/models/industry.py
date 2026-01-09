"""Industry selection model for job role recommender"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class IndustrySelection(BaseModel):
    """
    Represents a user's selection of target industries and specializations
    for role recommendation.
    """
    selection_id: str
    session_id: str
    industries: List[str]
    specializations: Optional[List[str]] = None
    selection_timestamp: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }