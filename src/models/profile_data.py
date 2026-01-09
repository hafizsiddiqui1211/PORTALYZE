"""Profile Data entity for Resume Analyzer Core"""
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
from src.utils.constants import (
    PROFILE_TYPE_LINKEDIN,
    PROFILE_TYPE_GITHUB,
    PROFILE_TYPE_PORTFOLIO,
    SUPPORTED_PROFILE_TYPES
)


@dataclass
class ProfileData:
    """Represents the extracted and normalized profile data from a URL"""

    profile_id: str
    url_id: str
    profile_type: str  # LINKEDIN, GITHUB, or PORTFOLIO
    raw_content: str  # Raw extracted HTML/text content
    normalized_content: Dict[str, Any]  # Structured extracted data
    extraction_timestamp: datetime
    extraction_status: str  # SUCCESS, PARTIAL, FAILED
    limitations: List[str]  # Any parsing limitations encountered

    def __post_init__(self):
        """Validate the ProfileData entity after initialization"""
        if not self.profile_id:
            raise ValueError("profile_id cannot be empty")

        if not self.url_id:
            raise ValueError("url_id cannot be empty")

        if self.profile_type not in SUPPORTED_PROFILE_TYPES:
            raise ValueError(f"profile_type must be one of: {', '.join(SUPPORTED_PROFILE_TYPES)}")

        if self.extraction_status not in ["SUCCESS", "PARTIAL", "FAILED"]:
            raise ValueError("extraction_status must be SUCCESS, PARTIAL, or FAILED")

        if not isinstance(self.limitations, list):
            raise ValueError("limitations must be a list")

        # Validate normalized content structure based on profile type
        self._validate_normalized_content()

    def _validate_normalized_content(self):
        """Validate the structure of normalized content based on profile type."""
        if self.profile_type == PROFILE_TYPE_LINKEDIN:
            self._validate_linkedin_content()
        elif self.profile_type == PROFILE_TYPE_GITHUB:
            self._validate_github_content()
        elif self.profile_type == PROFILE_TYPE_PORTFOLIO:
            self._validate_portfolio_content()

    def _validate_linkedin_content(self):
        """Validate LinkedIn-specific normalized content structure."""
        required_fields = ["headline", "summary"]
        optional_fields = ["experience_highlights", "skills"]

        for field in required_fields:
            if field not in self.normalized_content:
                raise ValueError(f"LinkedIn profile must have '{field}' in normalized_content")

    def _validate_github_content(self):
        """Validate GitHub-specific normalized content structure."""
        required_fields = ["username", "repositories"]
        optional_fields = ["bio", "total_stars", "recent_activity", "top_languages"]

        for field in required_fields:
            if field not in self.normalized_content:
                raise ValueError(f"GitHub profile must have '{field}' in normalized_content")

    def _validate_portfolio_content(self):
        """Validate Portfolio-specific normalized content structure."""
        required_fields = ["site_title", "bio_about"]
        optional_fields = ["projects", "skills", "contact_visible", "pages_analyzed"]

        for field in required_fields:
            if field not in self.normalized_content:
                raise ValueError(f"Portfolio profile must have '{field}' in normalized_content")

    @classmethod
    def create_new(
        cls,
        url_id: str,
        profile_type: str,
        raw_content: str = "",
        normalized_content: Optional[Dict[str, Any]] = None,
        extraction_status: str = "PENDING",
        limitations: Optional[List[str]] = None
    ) -> 'ProfileData':
        """
        Create a new ProfileData entity with generated ID and timestamp.

        Args:
            url_id: Foreign key to ProfileURL
            profile_type: Type of profile (LINKEDIN, GITHUB, or PORTFOLIO)
            raw_content: Raw extracted HTML/text content
            normalized_content: Structured extracted data (will be initialized to empty dict if None)
            extraction_status: Status of extraction (SUCCESS, PARTIAL, FAILED)
            limitations: Parsing limitations encountered (will be initialized to empty list if None)

        Returns:
            New ProfileData instance
        """
        if normalized_content is None:
            normalized_content = {}

        if limitations is None:
            limitations = []

        return cls(
            profile_id=str(uuid.uuid4()),
            url_id=url_id,
            profile_type=profile_type,
            raw_content=raw_content,
            normalized_content=normalized_content,
            extraction_timestamp=datetime.now(),
            extraction_status=extraction_status,
            limitations=limitations
        )

    def is_linkedin_data(self) -> bool:
        """Check if this contains LinkedIn data."""
        return self.profile_type == PROFILE_TYPE_LINKEDIN

    def is_github_data(self) -> bool:
        """Check if this contains GitHub data."""
        return self.profile_type == PROFILE_TYPE_GITHUB

    def is_portfolio_data(self) -> bool:
        """Check if this contains portfolio data."""
        return self.profile_type == PROFILE_TYPE_PORTFOLIO

    def get_headline(self) -> Optional[str]:
        """Get the headline from the profile data."""
        if self.is_linkedin_data() and "headline" in self.normalized_content:
            return self.normalized_content["headline"]
        return None

    def get_summary(self) -> Optional[str]:
        """Get the summary from the profile data."""
        if self.is_linkedin_data() and "summary" in self.normalized_content:
            return self.normalized_content["summary"]
        return None

    def get_skills(self) -> List[str]:
        """Get the skills from the profile data."""
        if self.profile_type in [PROFILE_TYPE_LINKEDIN, PROFILE_TYPE_PORTFOLIO] and "skills" in self.normalized_content:
            return self.normalized_content["skills"]
        return []

    def get_projects(self) -> List[Dict[str, Any]]:
        """Get the projects from the profile data."""
        if self.is_portfolio_data() and "projects" in self.normalized_content:
            return self.normalized_content["projects"]
        return []

    def get_repositories(self) -> List[Dict[str, Any]]:
        """Get the repositories from the profile data."""
        if self.is_github_data() and "repositories" in self.normalized_content:
            return self.normalized_content["repositories"]
        return []

    def get_bio(self) -> Optional[str]:
        """Get the bio from the profile data."""
        if self.is_github_data() and "bio" in self.normalized_content:
            return self.normalized_content["bio"]
        elif self.is_portfolio_data() and "bio_about" in self.normalized_content:
            return self.normalized_content["bio_about"]
        return None

    def has_significant_content(self) -> bool:
        """Check if the profile data contains significant content for analysis."""
        # Check if we have substantial content in the normalized data
        content_keys = list(self.normalized_content.keys())

        if self.is_linkedin_data():
            # For LinkedIn, check for headline, summary, or experience
            return (
                bool(self.get_headline() and len(self.get_headline()) > 10) or
                bool(self.get_summary() and len(self.get_summary()) > 20) or
                ("experience_highlights" in self.normalized_content and len(self.normalized_content["experience_highlights"]) > 0)
            )
        elif self.is_github_data():
            # For GitHub, check for repositories or bio
            return (
                bool(self.get_repositories() and len(self.get_repositories()) > 0) or
                bool(self.get_bio() and len(self.get_bio()) > 10)
            )
        elif self.is_portfolio_data():
            # For portfolio, check for bio, projects, or skills
            return (
                bool(self.get_bio() and len(self.get_bio()) > 20) or
                bool(self.get_projects() and len(self.get_projects()) > 0) or
                bool(self.get_skills() and len(self.get_skills()) > 0)
            )

        return False

    def to_dict(self) -> dict:
        """
        Convert the ProfileData to a dictionary representation.

        Returns:
            Dictionary representation of the ProfileData
        """
        return {
            "profile_id": self.profile_id,
            "url_id": self.url_id,
            "profile_type": self.profile_type,
            "raw_content": self.raw_content,
            "normalized_content": self.normalized_content,
            "extraction_timestamp": self.extraction_timestamp.isoformat() if self.extraction_timestamp else None,
            "extraction_status": self.extraction_status,
            "limitations": self.limitations
        }