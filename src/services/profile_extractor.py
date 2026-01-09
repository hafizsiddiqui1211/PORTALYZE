"""Base Profile Extractor service for Resume Analyzer Core"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.models.profile_data import ProfileData


class ProfileExtractor(ABC):
    """Abstract base class defining the interface for profile data extraction"""

    @abstractmethod
    def extract(self, url: str, **kwargs) -> ProfileData:
        """
        Extract profile data from the given URL.

        Args:
            url: The profile URL to extract data from
            **kwargs: Additional extraction parameters

        Returns:
            ProfileData instance containing the extracted data
        """
        pass

    @abstractmethod
    async def extract_async(self, url: str, **kwargs) -> ProfileData:
        """
        Asynchronously extract profile data from the given URL.

        Args:
            url: The profile URL to extract data from
            **kwargs: Additional extraction parameters

        Returns:
            ProfileData instance containing the extracted data
        """
        pass

    @abstractmethod
    def validate_url(self, url: str) -> tuple[bool, Optional[str]]:
        """
        Validate if the URL is supported by this extractor.

        Args:
            url: The URL to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        pass

    @abstractmethod
    def get_supported_platforms(self) -> list[str]:
        """
        Get the list of supported platforms for this extractor.

        Returns:
            List of supported platform names
        """
        pass

    @abstractmethod
    def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw extracted data into a standardized format.

        Args:
            raw_data: Raw extracted data

        Returns:
            Normalized data in standardized format
        """
        pass

    def preprocess_content(self, content: str) -> str:
        """
        Preprocess the content before extraction (remove unwanted elements, etc.).

        Args:
            content: Raw content to preprocess

        Returns:
            Preprocessed content
        """
        # Default implementation - just return content as is
        # Subclasses can override this to perform preprocessing
        return content

    def postprocess_data(self, profile_data: ProfileData) -> ProfileData:
        """
        Post-process the extracted profile data (add computed fields, etc.).

        Args:
            profile_data: The extracted profile data

        Returns:
            Post-processed profile data
        """
        # Default implementation - just return data as is
        # Subclasses can override this to perform post-processing
        return profile_data

    def calculate_extraction_score(self, profile_data: ProfileData) -> tuple[float, float]:
        """
        Calculate clarity and impact scores for the extracted profile data.

        Args:
            profile_data: The extracted profile data

        Returns:
            Tuple of (clarity_score, impact_score)
        """
        # Default implementation - return neutral scores
        # Subclasses should override this with platform-specific scoring
        return 50.0, 50.0  # Neutral scores

    def get_extraction_limits(self) -> Dict[str, Any]:
        """
        Get the extraction limits and constraints for this extractor.

        Returns:
            Dictionary with extraction limits and constraints
        """
        return {
            "max_pages": 1,  # Maximum number of pages to extract
            "max_content_length": 10000,  # Maximum content length in characters
            "timeout": 30,  # Timeout in seconds
            "retry_attempts": 3,  # Number of retry attempts
            "concurrent_requests": 1  # Maximum concurrent requests
        }


class BaseProfileExtractor(ProfileExtractor):
    """Base implementation of ProfileExtractor with common functionality"""

    def __init__(self):
        self.platform_name = "Base"
        self.supported_domains = []
        self.logger = None  # Will be set by subclasses

    def validate_url(self, url: str) -> tuple[bool, Optional[str]]:
        """
        Validate if the URL is supported by this extractor.

        Args:
            url: The URL to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url:
            return False, "URL cannot be empty"

        if not url.startswith(("http://", "https://")):
            return False, "URL must start with http:// or https://"

        # Check if URL domain is supported
        for domain in self.supported_domains:
            if domain in url:
                return True, None

        return False, f"Domain not supported. Supported domains: {', '.join(self.supported_domains)}"

    def get_supported_platforms(self) -> list[str]:
        """
        Get the list of supported platforms for this extractor.

        Returns:
            List of supported platform names
        """
        return [self.platform_name]

    def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw extracted data into a standardized format.

        Args:
            raw_data: Raw extracted data

        Returns:
            Normalized data in standardized format
        """
        # Default normalization - return raw data as is
        # Subclasses should override this with platform-specific normalization
        return raw_data

    def extract(self, url: str, **kwargs) -> ProfileData:
        """
        Synchronous extraction method that must be implemented by subclasses.

        Args:
            url: The profile URL to extract data from
            **kwargs: Additional extraction parameters

        Returns:
            ProfileData instance containing the extracted data
        """
        raise NotImplementedError("Subclasses must implement the extract method")

    async def extract_async(self, url: str, **kwargs) -> ProfileData:
        """
        Asynchronous extraction method that must be implemented by subclasses.

        Args:
            url: The profile URL to extract data from
            **kwargs: Additional extraction parameters

        Returns:
            ProfileData instance containing the extracted data
        """
        raise NotImplementedError("Subclasses must implement the extract_async method")

    def get_extraction_limits(self) -> Dict[str, Any]:
        """
        Get the extraction limits and constraints for this extractor.

        Returns:
            Dictionary with extraction limits and constraints
        """
        # Default limits - can be overridden by subclasses
        return {
            "max_pages": 1,
            "max_content_length": 10000,
            "timeout": 30,
            "retry_attempts": 3,
            "concurrent_requests": 1
        }

    def calculate_extraction_score(self, profile_data: ProfileData) -> tuple[float, float]:
        """
        Calculate clarity and impact scores for the extracted profile data.

        Args:
            profile_data: The extracted profile data

        Returns:
            Tuple of (clarity_score, impact_score)
        """
        # Base implementation: calculate scores based on content richness
        content = profile_data.raw_content
        normalized = profile_data.normalized_content

        # Calculate clarity score based on content structure and completeness
        clarity_score = 50.0  # Base score

        # Bonus for having a bio/summary
        if normalized.get('bio') or normalized.get('summary') or normalized.get('bio_about'):
            clarity_score += 15.0

        # Bonus for having skills
        if normalized.get('skills') and len(normalized['skills']) > 0:
            clarity_score += 10.0

        # Bonus for having projects or experience
        if normalized.get('projects') and len(normalized['projects']) > 0:
            clarity_score += 10.0
        elif normalized.get('experience_highlights') and len(normalized['experience_highlights']) > 0:
            clarity_score += 10.0

        # Calculate impact score based on perceived influence
        impact_score = 50.0  # Base score

        # Bonus for GitHub-specific metrics
        if profile_data.is_github_data():
            total_stars = normalized.get('total_stars', 0)
            repo_count = len(normalized.get('repositories', []))

            if total_stars > 100:
                impact_score += min(20, total_stars / 10)  # Up to 20 points for stars
            if repo_count > 5:
                impact_score += min(15, repo_count)  # Up to 15 points for repos

        # Bonus for LinkedIn-specific metrics
        elif profile_data.is_linkedin_data():
            headline = normalized.get('headline', '')
            summary = normalized.get('summary', '')

            if headline and len(headline) > 10:
                impact_score += 10.0
            if summary and len(summary) > 50:
                impact_score += 15.0

        # Bonus for portfolio-specific metrics
        elif profile_data.is_portfolio_data():
            site_title = normalized.get('site_title', '')
            contact_visible = normalized.get('contact_visible', False)

            if site_title and len(site_title) > 5:
                impact_score += 10.0
            if contact_visible:
                impact_score += 10.0

        # Cap scores at 100
        clarity_score = min(100.0, clarity_score)
        impact_score = min(100.0, impact_score)

        return clarity_score, impact_score