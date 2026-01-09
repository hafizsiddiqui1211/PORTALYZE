"""Tests for the URL validator service"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.url_validator import URLValidator
from src.models.profile_url import ProfileURL


class TestURLValidator:
    """Test cases for URLValidator service"""

    def test_detect_profile_type_linkedin(self):
        """Test profile type detection for LinkedIn URLs"""
        validator = URLValidator()

        linkedin_urls = [
            "https://www.linkedin.com/in/johndoe",
            "https://linkedin.com/in/janedoe",
            "http://www.linkedin.com/in/testuser",
            "https://www.linkedin.com/in/user123/"
        ]

        for url in linkedin_urls:
            assert validator.detect_profile_type(url) == "LINKEDIN"

    def test_detect_profile_type_github(self):
        """Test profile type detection for GitHub URLs"""
        validator = URLValidator()

        github_urls = [
            "https://www.github.com/johndoe",
            "https://github.com/janedoe",
            "http://www.github.com/testuser",
            "https://github.com/user123/",
            "https://github.com/username123"
        ]

        for url in github_urls:
            assert validator.detect_profile_type(url) == "GITHUB"

    def test_detect_profile_type_portfolio(self):
        """Test profile type detection for portfolio URLs"""
        validator = URLValidator()

        portfolio_urls = [
            "https://www.johndoe.com",
            "https://janedoe.io",
            "http://testuser.net",
            "https://portfolio.design",
            "https://mywebsite.org/path"
        ]

        for url in portfolio_urls:
            assert validator.detect_profile_type(url) == "PORTFOLIO"

    def test_detect_profile_type_invalid(self):
        """Test profile type detection for invalid URLs"""
        validator = URLValidator()

        invalid_urls = [
            "ftp://example.com",
            "not-a-url",
            "file:///etc/passwd"
        ]

        for url in invalid_urls:
            # For invalid URLs, it should default to PORTFOLIO
            assert validator.detect_profile_type(url) == "PORTFOLIO"

    def test_validate_linkedin_url_format_valid(self):
        """Test validation of valid LinkedIn URLs"""
        validator = URLValidator()

        valid_urls = [
            "https://www.linkedin.com/in/johndoe",
            "https://linkedin.com/in/janedoe",
            "http://www.linkedin.com/in/testuser123",
            "https://www.linkedin.com/in/user-name/",
            "https://linkedin.com/in/username123"
        ]

        for url in valid_urls:
            is_valid, error_msg = validator.validate_url_format(url)
            assert is_valid, f"URL {url} should be valid but got error: {error_msg}"
            assert error_msg is None

    def test_validate_linkedin_url_format_invalid(self):
        """Test validation of invalid LinkedIn URLs"""
        validator = URLValidator()

        invalid_urls = [
            "https://www.linkedin.com/",  # No username
            "https://www.linkedin.com/company/test",  # Wrong pattern
            "https://example.com/linkedin",  # Wrong domain
            "https://linkedin.com/profile",  # Wrong path
        ]

        for url in invalid_urls:
            is_valid, error_msg = validator.validate_url_format(url)
            assert not is_valid, f"URL {url} should be invalid"
            assert error_msg is not None

    def test_validate_github_url_format_valid(self):
        """Test validation of valid GitHub URLs"""
        validator = URLValidator()

        valid_urls = [
            "https://www.github.com/johndoe",
            "https://github.com/janedoe",
            "http://www.github.com/testuser",
            "https://github.com/user_name",
            "https://github.com/user-name",
            "https://github.com/username123"
        ]

        for url in valid_urls:
            is_valid, error_msg = validator.validate_url_format(url)
            assert is_valid, f"URL {url} should be valid but got error: {error_msg}"
            assert error_msg is None

    def test_validate_github_url_format_invalid(self):
        """Test validation of invalid GitHub URLs"""
        validator = URLValidator()

        invalid_urls = [
            "https://www.github.com/",  # No username
            "https://github.com/user/repo",  # Contains repo path
            "https://example.com/github",  # Wrong domain
            "https://github.com/user/path/extra",  # Too many path segments
        ]

        for url in invalid_urls:
            is_valid, error_msg = validator.validate_url_format(url)
            assert not is_valid, f"URL {url} should be invalid"
            assert error_msg is not None

    def test_validate_portfolio_url_format_valid(self):
        """Test validation of valid portfolio URLs"""
        validator = URLValidator()

        valid_urls = [
            "https://www.johndoe.com",
            "https://janedoe.io",
            "http://testuser.net",
            "https://portfolio.design",
            "https://mywebsite.org/path"
        ]

        for url in valid_urls:
            is_valid, error_msg = validator.validate_url_format(url)
            assert is_valid, f"URL {url} should be valid but got error: {error_msg}"
            assert error_msg is None

    def test_validate_portfolio_url_format_invalid(self):
        """Test validation of invalid portfolio URLs"""
        validator = URLValidator()

        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "https://",  # Incomplete URL
            "https://.com",  # No domain name
        ]

        for url in invalid_urls:
            is_valid, error_msg = validator.validate_url_format(url)
            assert not is_valid, f"URL {url} should be invalid"
            assert error_msg is not None

    @patch('src.services.url_validator.requests.get')
    def test_check_url_accessibility_valid(self, mock_get):
        """Test URL accessibility check for valid URLs"""
        validator = URLValidator()

        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        url = "https://www.linkedin.com/in/testuser"
        is_accessible = validator.check_url_accessibility(url)
        assert is_accessible is True

    @patch('src.services.url_validator.requests.get')
    def test_check_url_accessibility_invalid(self, mock_get):
        """Test URL accessibility check for invalid URLs"""
        validator = URLValidator()

        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        url = "https://www.linkedin.com/in/nonexistent"
        is_accessible = validator.check_url_accessibility(url)
        assert is_accessible is False

    @patch('src.services.url_validator.requests.get')
    def test_check_url_accessibility_request_error(self, mock_get):
        """Test URL accessibility check when request fails"""
        validator = URLValidator()

        # Mock request raising an exception
        mock_get.side_effect = Exception("Connection error")

        url = "https://www.linkedin.com/in/testuser"
        is_accessible = validator.check_url_accessibility(url)
        assert is_accessible is False

    def test_validate_url_success(self):
        """Test successful URL validation"""
        validator = URLValidator()

        with patch.object(validator, 'validate_url_format', return_value=(True, None)), \
             patch.object(validator, 'check_url_accessibility', return_value=True):

            url = "https://www.linkedin.com/in/testuser"
            profile_url = validator.validate_url(url, "test-session")

            assert profile_url is not None
            assert profile_url.url == url
            assert profile_url.is_valid is True
            assert profile_url.is_accessible is True
            assert profile_url.session_id == "test-session"

    def test_validate_url_format_invalid(self):
        """Test URL validation when format is invalid"""
        validator = URLValidator()

        with patch.object(validator, 'validate_url_format', return_value=(False, "Invalid format")), \
             patch.object(validator, 'check_url_accessibility', return_value=True):

            url = "invalid-url"
            profile_url = validator.validate_url(url, "test-session")

            assert profile_url is not None
            assert profile_url.url == url
            assert profile_url.is_valid is False
            assert profile_url.is_accessible is True  # Accessibility check still ran
            assert profile_url.error_message == "Invalid format"

    def test_validate_url_not_accessible(self):
        """Test URL validation when URL is not accessible"""
        validator = URLValidator()

        with patch.object(validator, 'validate_url_format', return_value=(True, None)), \
             patch.object(validator, 'check_url_accessibility', return_value=False):

            url = "https://www.linkedin.com/in/nonexistent"
            profile_url = validator.validate_url(url, "test-session")

            assert profile_url is not None
            assert profile_url.url == url
            assert profile_url.is_valid is True  # Format is valid
            assert profile_url.is_accessible is False
            assert profile_url.error_message is None

    def test_create_profile_url_entity(self):
        """Test creation of ProfileURL entity"""
        validator = URLValidator()

        url = "https://www.linkedin.com/in/testuser"
        profile_url = validator.create_profile_url_entity(url, "test-session")

        assert profile_url is not None
        assert profile_url.url == url
        assert profile_url.session_id == "test-session"
        assert profile_url.profile_type == "LINKEDIN"
        assert isinstance(profile_url.url_id, str) and len(profile_url.url_id) > 0

    def test_validate_multiple_urls(self):
        """Test validation of multiple URLs"""
        validator = URLValidator()

        urls = [
            "https://www.linkedin.com/in/user1",
            "https://github.com/user2",
            "https://portfolio.com/user3"
        ]

        with patch.object(validator, 'validate_url_format', return_value=(True, None)), \
             patch.object(validator, 'check_url_accessibility', return_value=True):

            results = validator.validate_multiple_urls(urls, "test-session")

            assert len(results) == 3
            for i, result in enumerate(results):
                assert result.url == urls[i]
                assert result.is_valid is True
                assert result.is_accessible is True

    def test_is_linkedin_url(self):
        """Test LinkedIn URL detection"""
        validator = URLValidator()

        assert validator.is_linkedin_url("https://www.linkedin.com/in/testuser") is True
        assert validator.is_linkedin_url("https://github.com/testuser") is False
        assert validator.is_linkedin_url("https://portfolio.com/testuser") is False

    def test_is_github_url(self):
        """Test GitHub URL detection"""
        validator = URLValidator()

        assert validator.is_github_url("https://github.com/testuser") is True
        assert validator.is_github_url("https://www.linkedin.com/in/testuser") is False
        assert validator.is_github_url("https://portfolio.com/testuser") is False

    def test_is_portfolio_url(self):
        """Test portfolio URL detection"""
        validator = URLValidator()

        assert validator.is_portfolio_url("https://portfolio.com/testuser") is True
        assert validator.is_portfolio_url("https://github.com/testuser") is False
        assert validator.is_portfolio_url("https://www.linkedin.com/in/testuser") is False

    def test_normalize_url(self):
        """Test URL normalization"""
        validator = URLValidator()

        # Test various URL formats
        test_cases = [
            ("HTTP://WWW.EXAMPLE.COM", "http://www.example.com"),
            ("https://example.com///path//to//resource", "https://example.com/path/to/resource"),
            ("https://example.com?param=value&other=thing", "https://example.com?param=value&other=thing"),
        ]

        for input_url, expected in test_cases:
            normalized = validator.normalize_url(input_url)
            assert normalized == expected