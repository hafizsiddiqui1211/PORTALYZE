"""URL validation service for Resume Analyzer Core"""
import re
import requests
from typing import Tuple, Optional, List
from urllib.parse import urlparse
from src.models.profile_url import ProfileURL
from src.utils.constants import (
    LINKEDIN_URL_PATTERN,
    GITHUB_URL_PATTERN,
    PORTFOLIO_URL_PATTERN,
    PROFILE_TYPE_LINKEDIN,
    PROFILE_TYPE_GITHUB,
    PROFILE_TYPE_PORTFOLIO,
    HTTP_TIMEOUT_DEFAULT
)
from src.utils.logger import get_logger


class URLValidator:
    """Validates profile URLs for format, accessibility, and profile type detection"""

    def __init__(self):
        self.logger = get_logger("URLValidator")

    def detect_profile_type(self, url: str) -> str:
        """
        Detect the profile type based on URL pattern.

        Args:
            url: The URL to analyze

        Returns:
            Profile type (LINKEDIN, GITHUB, or PORTFOLIO)
        """
        if not url:
            return PROFILE_TYPE_PORTFOLIO  # Default to portfolio for empty URLs

        # Normalize URL by removing trailing slashes and query params
        normalized_url = url.lower().split('?')[0].rstrip('/')

        # Check for LinkedIn pattern
        if re.match(LINKEDIN_URL_PATTERN, normalized_url):
            return PROFILE_TYPE_LINKEDIN

        # Check for GitHub pattern
        if re.match(GITHUB_URL_PATTERN, normalized_url):
            return PROFILE_TYPE_GITHUB

        # If it's a valid HTTP/HTTPS URL, consider it a portfolio
        if re.match(PORTFOLIO_URL_PATTERN, url.lower()):
            return PROFILE_TYPE_PORTFOLIO

        # Default to portfolio if it looks like a valid URL
        if url.lower().startswith(('http://', 'https://')):
            return PROFILE_TYPE_PORTFOLIO

        # If none match, default to portfolio
        return PROFILE_TYPE_PORTFOLIO

    def validate_url_format(self, url: str) -> Tuple[bool, Optional[str]]:
        """
        Validate URL format based on profile type.

        Args:
            url: The URL to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url:
            return False, "URL cannot be empty"

        if not url.lower().startswith(('http://', 'https://')):
            return False, "URL must start with http:// or https://"

        # Detect profile type
        profile_type = self.detect_profile_type(url)

        # Validate based on profile type
        if profile_type == PROFILE_TYPE_LINKEDIN:
            return self._validate_linkedin_url(url)
        elif profile_type == PROFILE_TYPE_GITHUB:
            return self._validate_github_url(url)
        elif profile_type == PROFILE_TYPE_PORTFOLIO:
            return self._validate_portfolio_url(url)
        else:
            return False, f"Unknown profile type: {profile_type}"

    def _validate_linkedin_url(self, url: str) -> Tuple[bool, Optional[str]]:
        """Validate LinkedIn URL format."""
        if not re.match(LINKEDIN_URL_PATTERN, url.lower()):
            return False, f"Invalid LinkedIn URL format. Expected pattern: {LINKEDIN_URL_PATTERN}"
        return True, None

    def _validate_github_url(self, url: str) -> Tuple[bool, Optional[str]]:
        """Validate GitHub URL format."""
        if not re.match(GITHUB_URL_PATTERN, url.lower()):
            return False, f"Invalid GitHub URL format. Expected pattern: {GITHUB_URL_PATTERN}"
        return True, None

    def _validate_portfolio_url(self, url: str) -> Tuple[bool, Optional[str]]:
        """Validate portfolio URL format."""
        if not re.match(PORTFOLIO_URL_PATTERN, url.lower()):
            return False, f"Invalid portfolio URL format. Must be a valid HTTP/HTTPS URL"
        return True, None

    def check_url_accessibility(self, url: str, timeout: int = HTTP_TIMEOUT_DEFAULT) -> bool:
        """
        Check if a URL is accessible.

        Args:
            url: The URL to check
            timeout: Request timeout in seconds

        Returns:
            True if accessible, False otherwise
        """
        try:
            self.logger.debug(f"Checking URL accessibility: {url}")

            # Check if it's a LinkedIn URL - they often block HEAD requests
            is_linkedin_url = 'linkedin.com' in url.lower()

            if is_linkedin_url:
                # For LinkedIn URLs, use GET request with minimal headers to avoid blocking
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                }

                # Make a GET request with minimal data transfer
                response = requests.get(url, timeout=timeout, allow_redirects=True,
                                      headers=headers, stream=True)
            else:
                # Make a HEAD request first to check if the URL is accessible
                response = requests.head(url, timeout=timeout, allow_redirects=True)

            # Consider it accessible if status code is less than 400
            is_accessible = response.status_code < 400

            if is_accessible:
                self.logger.info(f"URL is accessible: {url} (status: {response.status_code})")
            else:
                self.logger.warning(f"URL is not accessible: {url} (status: {response.status_code})")

            return is_accessible

        except requests.exceptions.RequestException as e:
            self.logger.warning(f"URL accessibility check failed for {url}: {str(e)}")
            # For LinkedIn, if the check fails, we'll still consider it potentially valid
            # since the format is correct and users might have valid profiles
            if 'linkedin.com' in url.lower():
                self.logger.info(f"LinkedIn URL format is valid, considering as potentially accessible: {url}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during URL accessibility check for {url}: {str(e)}")
            return False

    def validate_url(self, url: str, session_id: str) -> Optional[ProfileURL]:
        """
        Validate a profile URL by checking format and accessibility.

        Args:
            url: The URL to validate
            session_id: Session ID for the validation

        Returns:
            ProfileURL entity with validation results, or None if validation fails
        """
        self.logger.info(f"Validating URL: {url} for session: {session_id}")

        # Validate URL format
        is_valid, error_message = self.validate_url_format(url)

        # Check URL accessibility
        is_accessible = self.check_url_accessibility(url)

        # Create ProfileURL entity
        profile_url = ProfileURL.create_new(
            url=url,
            session_id=session_id,
            profile_type=self.detect_profile_type(url),
            is_valid=is_valid,
            is_accessible=is_accessible,
            error_message=error_message
        )

        self.logger.info(f"URL validation completed - Valid: {is_valid}, Accessible: {is_accessible} for URL: {url}")

        return profile_url

    def validate_multiple_urls(self, urls: List[str], session_id: str) -> List[ProfileURL]:
        """
        Validate multiple URLs.

        Args:
            urls: List of URLs to validate
            session_id: Session ID for the validation

        Returns:
            List of ProfileURL entities with validation results
        """
        results = []
        for url in urls:
            profile_url = self.validate_url(url, session_id)
            if profile_url:
                results.append(profile_url)

        return results

    def is_linkedin_url(self, url: str) -> bool:
        """
        Check if a URL is a LinkedIn URL.

        Args:
            url: The URL to check

        Returns:
            True if it's a LinkedIn URL, False otherwise
        """
        return self.detect_profile_type(url) == PROFILE_TYPE_LINKEDIN

    def is_github_url(self, url: str) -> bool:
        """
        Check if a URL is a GitHub URL.

        Args:
            url: The URL to check

        Returns:
            True if it's a GitHub URL, False otherwise
        """
        return self.detect_profile_type(url) == PROFILE_TYPE_GITHUB

    def is_portfolio_url(self, url: str) -> bool:
        """
        Check if a URL is a portfolio URL.

        Args:
            url: The URL to check

        Returns:
            True if it's a portfolio URL, False otherwise
        """
        return self.detect_profile_type(url) == PROFILE_TYPE_PORTFOLIO

    def normalize_url(self, url: str) -> str:
        """
        Normalize a URL by standardizing its format.

        Args:
            url: The URL to normalize

        Returns:
            Normalized URL
        """
        # Convert to lowercase
        normalized = url.lower()

        # Remove duplicate slashes
        normalized = re.sub(r'/{2,}', '/', normalized)

        # Remove trailing slash if not root
        if normalized.count('/') > 2:  # More than scheme://domain/
            normalized = normalized.rstrip('/')

        return normalized

    def create_profile_url_entity(self, url: str, session_id: str) -> ProfileURL:
        """
        Create a ProfileURL entity with initial validation.

        Args:
            url: The URL to create entity for
            session_id: Session ID for the entity

        Returns:
            ProfileURL entity
        """
        return ProfileURL.create_new(
            url=url,
            session_id=session_id,
            profile_type=self.detect_profile_type(url)
        )