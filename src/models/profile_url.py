"""Profile URL entity for Resume Analyzer Core"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import uuid
import re
from src.utils.constants import (
    LINKEDIN_URL_PATTERN,
    GITHUB_URL_PATTERN,
    PORTFOLIO_URL_PATTERN,
    PROFILE_TYPE_LINKEDIN,
    PROFILE_TYPE_GITHUB,
    PROFILE_TYPE_PORTFOLIO
)


@dataclass
class ProfileURL:
    """Represents a user-provided profile URL and its validation status"""

    url_id: str
    url: str
    profile_type: str  # LINKEDIN, GITHUB, or PORTFOLIO
    is_valid: bool
    is_accessible: bool
    validation_timestamp: datetime
    session_id: str
    error_message: Optional[str] = None

    def __post_init__(self):
        """Validate the ProfileURL entity after initialization"""
        if not self.url_id:
            raise ValueError("url_id cannot be empty")

        if not self.url:
            raise ValueError("url cannot be empty")

        if self.profile_type not in [PROFILE_TYPE_LINKEDIN, PROFILE_TYPE_GITHUB, PROFILE_TYPE_PORTFOLIO]:
            raise ValueError(f"profile_type must be one of: {PROFILE_TYPE_LINKEDIN}, {PROFILE_TYPE_GITHUB}, {PROFILE_TYPE_PORTFOLIO}")

        if self.is_valid and not self.is_accessible:
            # It's valid but not accessible - this is acceptable
            pass
        elif self.is_valid and self.is_accessible:
            # Both valid and accessible - perfect
            pass
        elif not self.is_valid:
            # Not valid - this should be accompanied by an error message
            if self.is_accessible and not self.error_message:
                raise ValueError("If URL is accessible but not valid, an error message must be provided")

    @classmethod
    def create_new(
        cls,
        url: str,
        session_id: str,
        profile_type: Optional[str] = None,
        is_valid: bool = False,
        is_accessible: bool = False,
        error_message: Optional[str] = None
    ) -> 'ProfileURL':
        """
        Create a new ProfileURL entity with generated ID and timestamp.

        Args:
            url: The profile URL
            session_id: Session identifier for cleanup
            profile_type: Type of profile (will be auto-detected if None)
            is_valid: Whether URL format is valid
            is_accessible: Whether URL is accessible
            error_message: Error message if validation failed

        Returns:
            New ProfileURL instance
        """
        # Auto-detect profile type if not provided
        if profile_type is None:
            profile_type = cls.detect_profile_type(url)

        return cls(
            url_id=str(uuid.uuid4()),
            url=url,
            profile_type=profile_type,
            is_valid=is_valid,
            is_accessible=is_accessible,
            validation_timestamp=datetime.now(),
            session_id=session_id,
            error_message=error_message
        )

    @staticmethod
    def detect_profile_type(url: str) -> str:
        """
        Detect the profile type based on URL pattern.

        Args:
            url: The URL to analyze

        Returns:
            Profile type (LINKEDIN, GITHUB, or PORTFOLIO)
        """
        # Normalize URL by removing trailing slashes and query params
        normalized_url = url.lower().split('?')[0].rstrip('/')

        # Check for LinkedIn pattern
        if re.match(LINKEDIN_URL_PATTERN.replace(r'(www\.)?', r'(www\.)?'), normalized_url):
            return PROFILE_TYPE_LINKEDIN

        # Check for GitHub pattern
        if re.match(GITHUB_URL_PATTERN.replace(r'(www\.)?', r'(www\.)?'), normalized_url):
            return PROFILE_TYPE_GITHUB

        # If it's a valid HTTP/HTTPS URL, consider it a portfolio
        if re.match(PORTFOLIO_URL_PATTERN.replace(r'(www\.)?', r'(www\.)?'), url.lower()):
            return PROFILE_TYPE_PORTFOLIO

        # Default to portfolio if it looks like a valid URL
        if url.lower().startswith(('http://', 'https://')):
            return PROFILE_TYPE_PORTFOLIO

        # If none match, default to portfolio
        return PROFILE_TYPE_PORTFOLIO

    def is_linkedin_url(self) -> bool:
        """Check if this is a LinkedIn URL."""
        return self.profile_type == PROFILE_TYPE_LINKEDIN

    def is_github_url(self) -> bool:
        """Check if this is a GitHub URL."""
        return self.profile_type == PROFILE_TYPE_GITHUB

    def is_portfolio_url(self) -> bool:
        """Check if this is a portfolio URL."""
        return self.profile_type == PROFILE_TYPE_PORTFOLIO

    def validate_format(self) -> tuple[bool, Optional[str]]:
        """
        Validate the URL format based on profile type.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.url.lower().startswith(('http://', 'https://')):
            return False, "URL must start with http:// or https://"

        if self.is_linkedin_url():
            if not re.match(LINKEDIN_URL_PATTERN, self.url.lower()):
                return False, f"Invalid LinkedIn URL format. Expected pattern: {LINKEDIN_URL_PATTERN}"
        elif self.is_github_url():
            if not re.match(GITHUB_URL_PATTERN, self.url.lower()):
                return False, f"Invalid GitHub URL format. Expected pattern: {GITHUB_URL_PATTERN}"
        elif self.is_portfolio_url():
            if not re.match(PORTFOLIO_URL_PATTERN, self.url.lower()):
                return False, f"Invalid portfolio URL format. Must be a valid HTTP/HTTPS URL"
        else:
            return False, f"Unknown profile type: {self.profile_type}"

        return True, None

    def to_dict(self) -> dict:
        """
        Convert the ProfileURL to a dictionary representation.

        Returns:
            Dictionary representation of the ProfileURL
        """
        return {
            "url_id": self.url_id,
            "url": self.url,
            "profile_type": self.profile_type,
            "is_valid": self.is_valid,
            "is_accessible": self.is_accessible,
            "validation_timestamp": self.validation_timestamp.isoformat() if self.validation_timestamp else None,
            "session_id": self.session_id,
            "error_message": self.error_message
        }