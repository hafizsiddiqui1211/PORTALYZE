"""LinkedIn Profile Extractor Service for Resume Analyzer Core"""
import re
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
import httpx
from src.services.http_client import HttpClient, SyncHttpClient
from src.services.rate_limiter import RateLimiter
from src.utils.logger import get_logger
from src.utils.constants import HTTP_TIMEOUT_DEFAULT
from src.utils.validation_utils import validate_url_security, validate_content_security


class LinkedInExtractor:
    """Extracts public profile data from LinkedIn profiles"""

    def __init__(self, http_timeout: int = HTTP_TIMEOUT_DEFAULT):
        self.http_timeout = http_timeout
        self.logger = get_logger("LinkedInExtractor")
        self.http_client = SyncHttpClient(timeout=http_timeout)
        self.rate_limiter = RateLimiter()
        self.base_url = "https://www.linkedin.com/in/"

    def extract_profile(self, url: str) -> Dict[str, Any]:
        """
        Extract profile data from a LinkedIn URL.

        Args:
            url: LinkedIn profile URL

        Returns:
            Dictionary with normalized profile data
        """
        self.logger.info(f"Starting LinkedIn profile extraction from: {url}")

        # Validate URL security
        is_valid, error_msg = validate_url_security(url)
        if not is_valid:
            raise ValueError(f"Invalid LinkedIn URL: {error_msg}")

        # Validate that URL is a LinkedIn profile
        if not url.lower().startswith(self.base_url):
            raise ValueError(f"URL is not a LinkedIn profile: {url}")

        # Apply rate limiting
        self.rate_limiter.wait_if_needed()

        try:
            # Get the profile page
            response = self.http_client.get(url)

            # Check for common LinkedIn privacy/access responses
            if response.status_code == 404:
                raise ValueError(f"LinkedIn profile not found (404). The profile may be private or no longer exists: {url}")
            elif response.status_code == 999:  # LinkedIn's rate limiting status code
                raise ValueError(f"LinkedIn rate limiting detected. Please try again later: {url}")
            elif "captcha" in response.text.lower() or "security" in response.text.lower():
                raise ValueError(f"LinkedIn security check detected. Profile extraction blocked for: {url}")
            elif "unavailable" in response.text.lower() or "private" in response.text.lower():
                raise ValueError(f"LinkedIn profile is private or unavailable: {url}")

            response.raise_for_status()

            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check if the page indicates privacy restrictions
            page_text = soup.get_text().lower()
            if any(phrase in page_text for phrase in [
                "private profile", "private", "this profile is private",
                "access denied", "unavailable", "not available"
            ]):
                raise ValueError(f"LinkedIn profile is private or access is restricted: {url}")

            # Extract profile data
            profile_data = self._extract_normalized_content(soup, url)

            # Check if extraction returned minimal data (indicating privacy restrictions)
            if len(profile_data) <= 2:  # Only url and profile_type
                self.logger.warning(f"LinkedIn profile returned minimal data, likely due to privacy settings: {url}")

            self.logger.info(f"Successfully extracted LinkedIn profile data from: {url}")
            return profile_data

        except httpx.RequestError as e:
            self.logger.error(f"HTTP error during LinkedIn extraction: {str(e)}")
            error_msg = str(e).lower()
            if "404" in error_msg or "not found" in error_msg:
                raise ValueError(f"LinkedIn profile not found (404). The profile may be private or no longer exists: {url}")
            elif "403" in error_msg or "forbidden" in error_msg:
                raise ValueError(f"LinkedIn access forbidden. Profile may be private: {url}")
            elif "429" in error_msg or "rate limit" in error_msg:
                raise ValueError(f"LinkedIn rate limiting detected. Please try again later: {url}")
            raise
        except Exception as e:
            self.logger.error(f"Error during LinkedIn extraction: {str(e)}")
            raise

    def _extract_normalized_content(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """
        Extract and normalize content from LinkedIn profile HTML.

        Args:
            soup: BeautifulSoup object with profile HTML
            url: Original profile URL

        Returns:
            Dictionary with normalized profile data
        """
        normalized_content = {
            "url": url,
            "profile_type": "LINKEDIN",
            "headline": self._extract_headline(soup),
            "summary": self._extract_summary(soup),
            "experience_highlights": self._extract_experience(soup),
            "skills": self._extract_skills(soup),
            "education": self._extract_education(soup),
            "recommendations": self._extract_recommendations(soup),
            "location": self._extract_location(soup),
            "connections": self._extract_connections(soup),
            "profile_image": self._extract_profile_image(soup)
        }

        # Remove None values
        normalized_content = {k: v for k, v in normalized_content.items() if v is not None}

        # Validate content security
        for key, value in normalized_content.items():
            if isinstance(value, str):
                is_valid, error_msg = validate_content_security(value)
                if not is_valid:
                    self.logger.warning(f"Content security validation failed for {key}: {error_msg}")
                    normalized_content[key] = ""  # Sanitize by removing potentially dangerous content

        return normalized_content

    def _extract_headline(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract headline/title from LinkedIn profile."""
        try:
            # Try multiple selectors for headline
            selectors = [
                'h1.text-heading-xlarge',  # New LinkedIn layout
                'h1[data-test-id="headline"]',  # Alternative selector
                '.pv-top-card--list .pv-top-card--experience-list-item',  # Alternative
                'h1'  # Fallback
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text:
                        return text

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting headline: {str(e)}")
            return None

    def _extract_summary(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract summary/about section from LinkedIn profile."""
        try:
            # Try multiple selectors for summary
            selectors = [
                '.pv-about-section .inline-show-more-text span',  # New LinkedIn layout
                '.pv-about-section .lt-line-clamp__line',  # Alternative
                '.pv-about-section p',  # Fallback
                '[data-test-id="about-section"]'  # Alternative
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text:
                        # Remove "See more" and "See less" text
                        text = re.sub(r'\s*See more\s*|\s*See less\s*', '', text).strip()
                        return text

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting summary: {str(e)}")
            return None

    def _extract_experience(self, soup: BeautifulSoup) -> Optional[List[Dict[str, Any]]]:
        """Extract experience information from LinkedIn profile."""
        try:
            experiences = []
            # Try multiple selectors for experience
            selectors = [
                '.experience-section .pv-position-entity',  # New LinkedIn layout
                '.pv-profile-section.experience-section li',  # Alternative
                '[data-section="experience"] li'  # Alternative
            ]

            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        exp = {
                            "title": self._get_text_from_selector(element, '.pv-entity__summary-info h3, .t-16'),
                            "company": self._get_text_from_selector(element, '.pv-entity__company-summary-info .pv-entity__summary-title-text, .pv-entity__secondary-title'),
                            "dates": self._get_text_from_selector(element, '.pv-entity__date-range span:nth-of-type(2), .pv-entity__bullet-item-v2'),
                            "location": self._get_text_from_selector(element, '.pv-entity__location .pv-entity__bullet-item-v2, .pv-entity__bullet-item'),
                            "description": self._get_text_from_selector(element, '.pv-entity__description, .pv-entity__extra-details')
                        }

                        # Remove None values
                        exp = {k: v for k, v in exp.items() if v is not None and v.strip()}
                        if exp:  # Only add if there's at least one field
                            experiences.append(exp)

                    break  # Use the first selector that finds content

            return experiences if experiences else None
        except Exception as e:
            self.logger.warning(f"Error extracting experience: {str(e)}")
            return None

    def _extract_skills(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """Extract skills from LinkedIn profile."""
        try:
            skills = []
            # Try multiple selectors for skills
            selectors = [
                '.pv-skill-category-entity .pv-skill-category-entity__name-text',  # New LinkedIn layout
                '.pv-profile-section.skills-section li',  # Alternative
                '.pv-skill-entity__skill-name'  # Alternative
            ]

            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        skill_text = element.get_text().strip()
                        if skill_text:
                            skills.append(skill_text)
                    break  # Use the first selector that finds content

            return skills if skills else None
        except Exception as e:
            self.logger.warning(f"Error extracting skills: {str(e)}")
            return None

    def _extract_education(self, soup: BeautifulSoup) -> Optional[List[Dict[str, Any]]]:
        """Extract education information from LinkedIn profile."""
        try:
            education = []
            # Try multiple selectors for education
            selectors = [
                '.education-section .pv-profile-section li',  # New LinkedIn layout
                '.pv-education-entity'  # Alternative
            ]

            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        edu = {
                            "school": self._get_text_from_selector(element, '.pv-entity__school-name, .text-size-16'),
                            "degree": self._get_text_from_selector(element, '.pv-entity__degree-name .pv-entity__comma-item, .text-size-14'),
                            "field": self._get_text_from_selector(element, '.pv-entity__fos .pv-entity__comma-item'),
                            "dates": self._get_text_from_selector(element, '.pv-entity__dates span:nth-of-type(2)')
                        }

                        # Remove None values
                        edu = {k: v for k, v in edu.items() if v is not None and v.strip()}
                        if edu:  # Only add if there's at least one field
                            education.append(edu)

                    break  # Use the first selector that finds content

            return education if education else None
        except Exception as e:
            self.logger.warning(f"Error extracting education: {str(e)}")
            return None

    def _extract_recommendations(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """Extract recommendations from LinkedIn profile."""
        try:
            # Recommendations are often not publicly visible
            # This is a best-effort extraction
            recommendations = []
            # Try to find any recommendation-related elements
            elements = soup.select('.recommendation-card .pv-recommendation-entity__summary')
            for element in elements:
                rec_text = element.get_text().strip()
                if rec_text:
                    recommendations.append(rec_text)

            return recommendations if recommendations else None
        except Exception as e:
            self.logger.warning(f"Error extracting recommendations: {str(e)}")
            return None

    def _extract_location(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract location from LinkedIn profile."""
        try:
            selectors = [
                '.pv-top-card--list-bullet .t-black--light',  # New LinkedIn layout
                '.pv-top-card__location',  # Alternative
                '.location-posterity'  # Alternative
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text:
                        return text

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting location: {str(e)}")
            return None

    def _extract_connections(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract connection count from LinkedIn profile."""
        try:
            selectors = [
                '.pv-top-card--list .t-bold',  # New LinkedIn layout
                '.pv-top-card__connections'  # Alternative
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text and ('connection' in text.lower() or 'follower' in text.lower()):
                        return text

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting connections: {str(e)}")
            return None

    def _extract_profile_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract profile image URL from LinkedIn profile."""
        try:
            selectors = [
                '.pv-top-card__photo .pv-top-card__photo-wrapper img',
                '.profile-photo-edit__preview img',
                '.pv-member-photo img'
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element and element.get('src'):
                    return element.get('src')

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting profile image: {str(e)}")
            return None

    def _get_text_from_selector(self, element, selector: str) -> Optional[str]:
        """Helper method to get text from a sub-selector."""
        try:
            sub_element = element.select_one(selector)
            if sub_element:
                return sub_element.get_text().strip()
            return None
        except Exception:
            return None

    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract profile data from a LinkedIn URL (alias for extract_profile).

        Args:
            url: LinkedIn profile URL

        Returns:
            Dictionary with normalized profile data
        """
        return self.extract_profile(url)

    def validate_linkedin_url(self, url: str) -> bool:
        """
        Validate if a URL is a valid LinkedIn profile URL.

        Args:
            url: URL to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if URL matches LinkedIn pattern
            is_valid, _ = validate_url_security(url)
            if not is_valid:
                return False

            return url.lower().startswith(self.base_url)
        except Exception:
            return False