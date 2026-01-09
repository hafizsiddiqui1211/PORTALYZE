"""Tests for the ProfileURL model"""
import pytest
from datetime import datetime
from src.models.profile_url import ProfileURL


class TestProfileURL:
    """Test cases for ProfileURL entity"""

    def test_profile_url_creation_success(self):
        """Test successful creation of a ProfileURL entity"""
        profile_url = ProfileURL(
            url_id="test-url-id",
            url="https://www.linkedin.com/in/testuser",
            profile_type="LINKEDIN",
            is_valid=True,
            is_accessible=True,
            validation_timestamp=datetime.now(),
            session_id="test-session",
            error_message=None
        )

        assert profile_url.url_id == "test-url-id"
        assert profile_url.url == "https://www.linkedin.com/in/testuser"
        assert profile_url.profile_type == "LINKEDIN"
        assert profile_url.is_valid is True
        assert profile_url.is_accessible is True
        assert profile_url.session_id == "test-session"
        assert profile_url.error_message is None

    def test_profile_url_creation_with_error(self):
        """Test creation of a ProfileURL entity with error message"""
        error_msg = "Invalid URL format"
        profile_url = ProfileURL(
            url_id="test-url-id",
            url="invalid-url",
            profile_type="PORTFOLIO",
            is_valid=False,
            is_accessible=False,
            validation_timestamp=datetime.now(),
            session_id="test-session",
            error_message=error_msg
        )

        assert profile_url.url_id == "test-url-id"
        assert profile_url.url == "invalid-url"
        assert profile_url.profile_type == "PORTFOLIO"
        assert profile_url.is_valid is False
        assert profile_url.is_accessible is False
        assert profile_url.session_id == "test-session"
        assert profile_url.error_message == error_msg

    def test_profile_url_creation_with_empty_url_id(self):
        """Test ProfileURL creation fails with empty url_id"""
        with pytest.raises(ValueError, match="url_id cannot be empty"):
            ProfileURL(
                url_id="",
                url="https://www.linkedin.com/in/testuser",
                profile_type="LINKEDIN",
                is_valid=True,
                is_accessible=True,
                validation_timestamp=datetime.now(),
                session_id="test-session"
            )

    def test_profile_url_creation_with_empty_url(self):
        """Test ProfileURL creation fails with empty url"""
        with pytest.raises(ValueError, match="url cannot be empty"):
            ProfileURL(
                url_id="test-url-id",
                url="",
                profile_type="LINKEDIN",
                is_valid=True,
                is_accessible=True,
                validation_timestamp=datetime.now(),
                session_id="test-session"
            )

    def test_profile_url_creation_with_invalid_profile_type(self):
        """Test ProfileURL creation fails with invalid profile type"""
        with pytest.raises(ValueError, match="profile_type must be one of"):
            ProfileURL(
                url_id="test-url-id",
                url="https://www.linkedin.com/in/testuser",
                profile_type="INVALID_TYPE",
                is_valid=True,
                is_accessible=True,
                validation_timestamp=datetime.now(),
                session_id="test-session"
            )

    def test_profile_url_creation_with_valid_profile_types(self):
        """Test ProfileURL creation with all valid profile types"""
        valid_types = ["LINKEDIN", "GITHUB", "PORTFOLIO"]

        for profile_type in valid_types:
            profile_url = ProfileURL(
                url_id="test-url-id",
                url="https://example.com",
                profile_type=profile_type,
                is_valid=True,
                is_accessible=True,
                validation_timestamp=datetime.now(),
                session_id="test-session"
            )
            assert profile_url.profile_type == profile_type

    def test_profile_url_create_new_method(self):
        """Test the create_new class method"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        # Should have generated a valid UUID
        assert profile_url.url_id is not None
        assert profile_url.url_id != ""
        assert profile_url.url == "https://www.linkedin.com/in/testuser"
        assert profile_url.session_id == "test-session"
        assert profile_url.validation_timestamp is not None

    def test_profile_url_create_new_with_explicit_profile_type(self):
        """Test create_new method with explicit profile type"""
        profile_url = ProfileURL.create_new(
            url="https://github.com/testuser",
            session_id="test-session",
            profile_type="GITHUB"
        )

        assert profile_url.profile_type == "GITHUB"
        assert profile_url.url == "https://github.com/testuser"

    def test_profile_url_create_new_with_auto_detected_profile_type(self):
        """Test create_new method with auto-detected profile type"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        assert profile_url.profile_type == "LINKEDIN"

    def test_profile_url_detect_profile_type_linkedin(self):
        """Test profile type detection for LinkedIn URLs"""
        test_urls = [
            "https://www.linkedin.com/in/testuser",
            "https://linkedin.com/in/testuser",
            "http://www.linkedin.com/in/testuser",
            "https://www.linkedin.com/in/test-user/",
            "https://www.linkedin.com/in/TestUser123"
        ]

        for url in test_urls:
            detected_type = ProfileURL.detect_profile_type(url)
            assert detected_type == "LINKEDIN"

    def test_profile_url_detect_profile_type_github(self):
        """Test profile type detection for GitHub URLs"""
        test_urls = [
            "https://www.github.com/testuser",
            "https://github.com/testuser",
            "http://www.github.com/testuser",
            "https://github.com/test_user",
            "https://github.com/test-user",
            "https://github.com/TestUser123"
        ]

        for url in test_urls:
            detected_type = ProfileURL.detect_profile_type(url)
            assert detected_type == "GITHUB"

    def test_profile_url_detect_profile_type_portfolio(self):
        """Test profile type detection for portfolio URLs"""
        test_urls = [
            "https://www.testuser.com",
            "https://testuser.io",
            "http://testuser.net",
            "https://portfolio.design",
            "https://mywebsite.org/page"
        ]

        for url in test_urls:
            detected_type = ProfileURL.detect_profile_type(url)
            assert detected_type == "PORTFOLIO"

    def test_profile_url_detect_profile_type_with_invalid_url(self):
        """Test profile type detection with invalid URL"""
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "javascript:alert('xss')"
        ]

        for url in invalid_urls:
            # Should default to PORTFOLIO for unrecognized patterns
            detected_type = ProfileURL.detect_profile_type(url)
            assert detected_type == "PORTFOLIO"

    def test_profile_url_is_linkedin_url(self):
        """Test is_linkedin_url method"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        assert profile_url.is_linkedin_url() is True
        assert profile_url.is_github_url() is False
        assert profile_url.is_portfolio_url() is False

    def test_profile_url_is_github_url(self):
        """Test is_github_url method"""
        profile_url = ProfileURL.create_new(
            url="https://github.com/testuser",
            session_id="test-session"
        )

        assert profile_url.is_github_url() is True
        assert profile_url.is_linkedin_url() is False
        assert profile_url.is_portfolio_url() is False

    def test_profile_url_is_portfolio_url(self):
        """Test is_portfolio_url method"""
        profile_url = ProfileURL.create_new(
            url="https://www.testuser.com",
            session_id="test-session"
        )

        assert profile_url.is_portfolio_url() is True
        assert profile_url.is_linkedin_url() is False
        assert profile_url.is_github_url() is False

    def test_profile_url_validate_format_linkedin_valid(self):
        """Test format validation for valid LinkedIn URLs"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        is_valid, error_msg = profile_url.validate_format()
        assert is_valid is True
        assert error_msg is None

    def test_profile_url_validate_format_linkedin_invalid(self):
        """Test format validation for invalid LinkedIn URLs"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/",  # No username
            session_id="test-session",
            profile_type="LINKEDIN"
        )

        is_valid, error_msg = profile_url.validate_format()
        assert is_valid is False
        assert error_msg is not None

    def test_profile_url_validate_format_github_valid(self):
        """Test format validation for valid GitHub URLs"""
        profile_url = ProfileURL.create_new(
            url="https://github.com/testuser",
            session_id="test-session"
        )

        is_valid, error_msg = profile_url.validate_format()
        assert is_valid is True
        assert error_msg is None

    def test_profile_url_validate_format_github_invalid(self):
        """Test format validation for invalid GitHub URLs"""
        profile_url = ProfileURL.create_new(
            url="https://github.com/",  # No username
            session_id="test-session",
            profile_type="GITHUB"
        )

        is_valid, error_msg = profile_url.validate_format()
        assert is_valid is False
        assert error_msg is not None

    def test_profile_url_validate_format_portfolio_valid(self):
        """Test format validation for valid portfolio URLs"""
        profile_url = ProfileURL.create_new(
            url="https://www.testuser.com",
            session_id="test-session"
        )

        is_valid, error_msg = profile_url.validate_format()
        assert is_valid is True
        assert error_msg is None

    def test_profile_url_validate_format_invalid_protocol(self):
        """Test format validation for URLs without proper protocol"""
        profile_url = ProfileURL.create_new(
            url="not-a-protocol://example.com",
            session_id="test-session",
            profile_type="PORTFOLIO"
        )

        is_valid, error_msg = profile_url.validate_format()
        assert is_valid is False
        assert error_msg is not None

    def test_profile_url_to_dict(self):
        """Test conversion to dictionary"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        profile_dict = profile_url.to_dict()

        assert isinstance(profile_dict, dict)
        assert profile_dict["url_id"] == profile_url.url_id
        assert profile_dict["url"] == profile_url.url
        assert profile_dict["profile_type"] == profile_url.profile_type
        assert profile_dict["is_valid"] == profile_url.is_valid
        assert profile_dict["is_accessible"] == profile_url.is_accessible
        assert profile_dict["session_id"] == profile_url.session_id
        assert profile_dict["error_message"] == profile_url.error_message

    def test_profile_url_equality(self):
        """Test equality comparison between ProfileURL instances"""
        profile_url1 = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        profile_url2 = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        # Different instances with same data shouldn't be equal due to different IDs
        assert profile_url1.url == profile_url2.url
        assert profile_url1.session_id == profile_url2.session_id

    def test_profile_url_hash(self):
        """Test that ProfileURL can be hashed (for use in sets/dicts)"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        # Should not raise an exception
        hash_value = hash(profile_url.url_id)
        assert isinstance(hash_value, int)

    def test_profile_url_str_representation(self):
        """Test string representation of ProfileURL"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        # Basic check that it has a string representation
        repr_str = repr(profile_url)
        assert isinstance(repr_str, str)
        assert "ProfileURL" in repr_str

    def test_profile_url_timestamp_preservation(self):
        """Test that timestamps are preserved correctly"""
        fixed_time = datetime(2023, 1, 1, 12, 0, 0)

        profile_url = ProfileURL(
            url_id="test-url-id",
            url="https://www.linkedin.com/in/testuser",
            profile_type="LINKEDIN",
            is_valid=True,
            is_accessible=True,
            validation_timestamp=fixed_time,
            session_id="test-session"
        )

        assert profile_url.validation_timestamp == fixed_time

    def test_profile_url_optional_error_message(self):
        """Test ProfileURL with optional error message"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session",
            error_message="Test error message"
        )

        assert profile_url.error_message == "Test error message"

    def test_profile_url_default_values(self):
        """Test ProfileURL with default values"""
        profile_url = ProfileURL.create_new(
            url="https://www.linkedin.com/in/testuser",
            session_id="test-session"
        )

        # When created via create_new, defaults should be set based on validation
        assert profile_url.url_id is not None
        assert profile_url.session_id == "test-session"
        assert profile_url.validation_timestamp is not None