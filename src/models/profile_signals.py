"""Profile signals model for job role recommender"""

from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class ProfileSignals(BaseModel):
    """
    Aggregated signals from resume analysis, LinkedIn, GitHub, and portfolio
    used for role inference.
    """
    signals_id: str
    resume_signals: Dict
    profile_signals: Dict
    aggregated_skills: List[str]
    experience_summary: Dict
    project_highlights: List[Dict]


class ResumeSignals(BaseModel):
    """Signals extracted from resume analysis"""
    skills: List[str]
    experience_years: float
    job_titles: List[str]
    industries: List[str]
    education: List[Dict]
    certifications: List[str]


class ProfileSignalsData(BaseModel):
    """Signals extracted from online profiles"""
    github_activity: Dict
    linkedin_summary: Dict
    portfolio_projects: List[Dict]
    social_signals: Dict


class ExperienceSummary(BaseModel):
    """Summary of professional experience"""
    total_years: float
    domains: List[str]
    leadership_indicators: List[str]
    technology_stack: List[str]