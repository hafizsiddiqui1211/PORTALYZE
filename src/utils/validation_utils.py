"""Validation utilities for Resume Analyzer Core"""
import os
import re
from typing import Tuple, Optional, Dict, Any, List
from urllib.parse import urlparse
import validators
from src.utils.constants import (
    LINKEDIN_URL_PATTERN,
    GITHUB_URL_PATTERN,
    PORTFOLIO_URL_PATTERN,
    SUPPORTED_PROFILE_TYPES
)


def validate_url_format(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the format of a URL.

    Args:
        url: The URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url:
        return False, "URL cannot be empty"

    # Check if it's a valid URL format using validators
    if not validators.url(url):
        return False, "Invalid URL format"

    # Check if it's an HTTP or HTTPS URL
    if not url.lower().startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"

    # Parse the URL to get the domain
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
    except Exception:
        return False, "Invalid URL format"

    # Check if it matches any supported profile type pattern
    if is_linkedin_url(url):
        return True, None
    elif is_github_url(url):
        return True, None
    elif is_portfolio_url(url):
        return True, None
    else:
        return False, f"URL does not match any supported profile type. Supported: {', '.join(SUPPORTED_PROFILE_TYPES)}"


def is_linkedin_url(url: str) -> bool:
    """
    Check if a URL is a LinkedIn profile URL.

    Args:
        url: The URL to check

    Returns:
        True if it's a LinkedIn URL, False otherwise
    """
    return bool(re.match(LINKEDIN_URL_PATTERN, url.lower()))


def is_github_url(url: str) -> bool:
    """
    Check if a URL is a GitHub profile URL.

    Args:
        url: The URL to check

    Returns:
        True if it's a GitHub URL, False otherwise
    """
    return bool(re.match(GITHUB_URL_PATTERN, url.lower()))


def is_portfolio_url(url: str) -> bool:
    """
    Check if a URL is a portfolio website URL.

    Args:
        url: The URL to check

    Returns:
        True if it's a portfolio URL, False otherwise
    """
    return bool(re.match(PORTFOLIO_URL_PATTERN, url.lower()))


def detect_profile_type(url: str) -> str:
    """
    Detect the profile type based on the URL.

    Args:
        url: The URL to analyze

    Returns:
        Profile type (LINKEDIN, GITHUB, or PORTFOLIO)
    """
    if is_linkedin_url(url):
        return "LINKEDIN"
    elif is_github_url(url):
        return "GITHUB"
    else:
        return "PORTFOLIO"  # Default to portfolio for any other valid URL


def validate_profile_data_structure(profile_data: Dict[str, Any], profile_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the structure of profile data based on profile type.

    Args:
        profile_data: The profile data to validate
        profile_type: The type of profile (LINKEDIN, GITHUB, or PORTFOLIO)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(profile_data, dict):
        return False, "Profile data must be a dictionary"

    # Validate required fields based on profile type
    if profile_type == "LINKEDIN":
        required_fields = ["headline", "summary"]
        optional_fields = ["experience_highlights", "skills", "education", "recommendations"]
    elif profile_type == "GITHUB":
        required_fields = ["username", "repositories"]
        optional_fields = ["bio", "total_stars", "recent_activity", "top_languages"]
    elif profile_type == "PORTFOLIO":
        required_fields = ["site_title", "bio_about"]
        optional_fields = ["projects", "skills", "contact_visible", "pages_analyzed"]
    else:
        return False, f"Invalid profile type: {profile_type}"

    # Check for required fields
    missing_fields = []
    for field in required_fields:
        if field not in profile_data:
            missing_fields.append(field)

    if missing_fields:
        return False, f"Missing required fields for {profile_type}: {', '.join(missing_fields)}"

    return True, None


def validate_skills_list(skills: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate a list of skills.

    Args:
        skills: List of skills to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(skills, list):
        return False, "Skills must be provided as a list"

    for i, skill in enumerate(skills):
        if not isinstance(skill, str):
            return False, f"Skill at index {i} is not a string: {type(skill)}"

        if not skill.strip():
            return False, f"Skill at index {i} is empty or contains only whitespace"

    return True, None


def validate_experience_entries(experiences: List[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """
    Validate a list of experience entries.

    Args:
        experiences: List of experience entries to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(experiences, list):
        return False, "Experiences must be provided as a list"

    for i, exp in enumerate(experiences):
        if not isinstance(exp, dict):
            return False, f"Experience at index {i} is not a dictionary: {type(exp)}"

        required_fields = ["company", "title", "start_date"]
        missing_fields = []
        for field in required_fields:
            if field not in exp:
                missing_fields.append(field)

        if missing_fields:
            return False, f"Experience at index {i} missing required fields: {', '.join(missing_fields)}"

    return True, None


def validate_project_entries(projects: List[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """
    Validate a list of project entries.

    Args:
        projects: List of project entries to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(projects, list):
        return False, "Projects must be provided as a list"

    for i, project in enumerate(projects):
        if not isinstance(project, dict):
            return False, f"Project at index {i} is not a dictionary: {type(project)}"

        # Projects should have at least a name
        if "name" not in project or not project["name"].strip():
            return False, f"Project at index {i} must have a non-empty name"

    return True, None


def validate_normalized_content(normalized_content: Dict[str, Any], profile_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the normalized content structure for a specific profile type.

    Args:
        normalized_content: The normalized content to validate
        profile_type: The type of profile (LINKEDIN, GITHUB, or PORTFOLIO)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(normalized_content, dict):
        return False, "Normalized content must be a dictionary"

    # Validate based on profile type
    if profile_type == "LINKEDIN":
        # LinkedIn should have at least headline and summary
        if "headline" not in normalized_content or not normalized_content["headline"].strip():
            return False, "LinkedIn profile must have a non-empty headline"
        if "summary" not in normalized_content or not normalized_content["summary"].strip():
            return False, "LinkedIn profile must have a non-empty summary"

        # Validate skills if present
        if "skills" in normalized_content:
            is_valid, error_msg = validate_skills_list(normalized_content["skills"])
            if not is_valid:
                return False, f"LinkedIn skills validation error: {error_msg}"

        # Validate experience if present
        if "experience" in normalized_content:
            is_valid, error_msg = validate_experience_entries(normalized_content["experience"])
            if not is_valid:
                return False, f"LinkedIn experience validation error: {error_msg}"

    elif profile_type == "GITHUB":
        # GitHub should have at least username and repositories
        if "username" not in normalized_content or not normalized_content["username"].strip():
            return False, "GitHub profile must have a non-empty username"
        if "repositories" not in normalized_content or not isinstance(normalized_content["repositories"], list):
            return False, "GitHub profile must have a repositories list"

        # Validate repositories
        for i, repo in enumerate(normalized_content["repositories"]):
            if not isinstance(repo, dict):
                return False, f"Repository at index {i} is not a dictionary"
            if "name" not in repo or not repo["name"].strip():
                return False, f"Repository at index {i} must have a non-empty name"

        # Validate bio if present
        if "bio" in normalized_content and normalized_content["bio"]:
            if not isinstance(normalized_content["bio"], str):
                return False, "GitHub bio must be a string"

    elif profile_type == "PORTFOLIO":
        # Portfolio should have at least site_title and bio_about
        if "site_title" not in normalized_content or not normalized_content["site_title"].strip():
            return False, "Portfolio profile must have a non-empty site_title"
        if "bio_about" not in normalized_content or not normalized_content["bio_about"].strip():
            return False, "Portfolio profile must have a non-empty bio_about"

        # Validate projects if present
        if "projects" in normalized_content:
            is_valid, error_msg = validate_project_entries(normalized_content["projects"])
            if not is_valid:
                return False, f"Portfolio projects validation error: {error_msg}"

        # Validate skills if present
        if "skills" in normalized_content:
            is_valid, error_msg = validate_skills_list(normalized_content["skills"])
            if not is_valid:
                return False, f"Portfolio skills validation error: {error_msg}"

    else:
        return False, f"Invalid profile type: {profile_type}"

    return True, None


def sanitize_text_content(text: str) -> str:
    """
    Sanitize text content by removing potentially harmful content.

    Args:
        text: The text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove potential script tags
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)

    # Remove potential iframe tags
    sanitized = re.sub(r'<iframe[^>]*>.*?</iframe>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)

    # Remove potential javascript: hrefs
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)

    # Remove potential data: hrefs
    sanitized = re.sub(r'data:', '', sanitized, flags=re.IGNORECASE)

    # Remove potential vbscript: hrefs
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)

    # Remove control characters (except common whitespace)
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\t\n\r')

    return sanitized.strip()


def validate_file_size(file_path: str, max_size_bytes: int) -> Tuple[bool, Optional[str]]:
    """
    Validate that a file size is within the allowed limit.

    Args:
        file_path: Path to the file to check
        max_size_bytes: Maximum allowed file size in bytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if not os.path.exists(file_path):
            return False, f"File does not exist: {file_path}"

        file_size = os.path.getsize(file_path)
        if file_size > max_size_bytes:
            max_size_mb = max_size_bytes / (1024 * 1024)
            file_size_mb = file_size / (1024 * 1024)
            return False, f"File size {file_size_mb:.2f}MB exceeds maximum allowed size of {max_size_mb:.2f}MB"

        return True, None
    except OSError as e:
        return False, f"Error checking file size: {str(e)}"


def validate_session_id(session_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a session ID format.

    Args:
        session_id: The session ID to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not session_id:
        return False, "Session ID cannot be empty"

    if not isinstance(session_id, str):
        return False, "Session ID must be a string"

    # Basic validation: should be a reasonable length and contain only safe characters
    if len(session_id) < 8:
        return False, "Session ID is too short (minimum 8 characters)"

    if len(session_id) > 128:
        return False, "Session ID is too long (maximum 128 characters)"

    # Check for potentially dangerous characters
    if re.search(r'[<>"\'&]', session_id):
        return False, "Session ID contains invalid characters"

    return True, None


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Check if a string is a valid UUID.

    Args:
        uuid_string: String to check

    Returns:
        True if valid UUID, False otherwise
    """
    try:
        import uuid
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def validate_uuid(uuid_string: str, field_name: str = "UUID") -> Tuple[bool, Optional[str]]:
    """
    Validate that a string is a valid UUID.

    Args:
        uuid_string: String to validate
        field_name: Name of the field for error messages

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not uuid_string:
        return False, f"{field_name} cannot be empty"

    if not is_valid_uuid(uuid_string):
        return False, f"Invalid {field_name}: {uuid_string}"

    return True, None


def validate_percentage(value: float, field_name: str = "Percentage") -> Tuple[bool, Optional[str]]:
    """
    Validate that a value is a valid percentage (0-100).

    Args:
        value: Value to validate
        field_name: Name of the field for error messages

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(value, (int, float)):
        return False, f"{field_name} must be a number"

    if not 0 <= value <= 100:
        return False, f"{field_name} must be between 0 and 100, got {value}"

    return True, None


def validate_list_elements(lst: List[Any], element_validator: callable, field_name: str = "List") -> Tuple[bool, Optional[str]]:
    """
    Validate all elements in a list using a provided validator function.

    Args:
        lst: List to validate
        element_validator: Function to validate each element (should return Tuple[bool, Optional[str]])
        field_name: Name of the field for error messages

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(lst, list):
        return False, f"{field_name} must be a list"

    for i, element in enumerate(lst):
        is_valid, error_msg = element_validator(element)
        if not is_valid:
            return False, f"{field_name}[{i}] validation failed: {error_msg}"

    return True, None


def is_safe_path(file_path: str, base_directory: str) -> bool:
    """
    Check if a file path is safe (doesn't attempt to escape the base directory).

    Args:
        file_path: Path to check
        base_directory: Base directory that paths should be contained within

    Returns:
        True if path is safe, False otherwise
    """
    try:
        # Resolve both paths to absolute paths
        abs_path = os.path.abspath(file_path)
        abs_base = os.path.abspath(base_directory)

        # Check if the file path starts with the base directory path
        return abs_path.startswith(abs_base)
    except Exception:
        # If there's an error resolving the paths, consider it unsafe
        return False


def validate_safe_path(file_path: str, base_directory: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a file path is safe and contained within the base directory.

    Args:
        file_path: Path to validate
        base_directory: Base directory that paths should be contained within

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_path:
        return False, "File path cannot be empty"

    if not base_directory:
        return False, "Base directory cannot be empty"

    # Normalize the paths to prevent path traversal
    normalized_path = os.path.normpath(file_path)
    normalized_base = os.path.normpath(base_directory)

    if not _is_safe_path(normalized_path, normalized_base):
        return False, f"Path '{file_path}' attempts to access files outside of allowed directory '{base_directory}'"

    return True, None


def _is_safe_path(file_path: str, base_directory: str) -> bool:
    """
    Check if a file path is safe and contained within the base directory.

    Args:
        file_path: Path to check
        base_directory: Base directory that paths should be contained within

    Returns:
        True if path is safe, False otherwise
    """
    try:
        # Convert to absolute paths
        abs_file_path = os.path.abspath(file_path)
        abs_base_directory = os.path.abspath(base_directory)

        # Check if the file path starts with the base directory path
        return abs_file_path.startswith(abs_base_directory)
    except Exception:
        # If there's an error resolving the paths, consider it unsafe
        return False


def prevent_directory_traversal(file_path: str) -> bool:
    """
    Check if a file path contains directory traversal attempts.

    Args:
        file_path: Path to check for traversal attempts

    Returns:
        True if path is safe, False if it contains traversal attempts
    """
    # Check for directory traversal patterns
    if '..' in file_path.replace('\\', '/').split('/'):
        return False

    # Normalize the path to resolve any relative paths
    normalized_path = os.path.normpath(file_path)

    # After normalization, check if the path goes up in the directory structure
    if normalized_path.startswith('..' + os.sep) or '/..' in normalized_path or '\\..':
        return False

    return True


def validate_file_path_security(file_path: str, allowed_extensions: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate file path for security issues including directory traversal and allowed extensions.

    Args:
        file_path: Path to validate
        allowed_extensions: Optional list of allowed file extensions (e.g., ['.pdf', '.docx'])

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_path:
        return False, "File path cannot be empty"

    # Prevent directory traversal
    if not prevent_directory_traversal(file_path):
        return False, "File path contains directory traversal attempt"

    # Validate file extension if allowed extensions are specified
    if allowed_extensions:
        import os.path
        _, ext = os.path.splitext(file_path.lower())
        if ext not in allowed_extensions:
            return False, f"File extension '{ext}' not allowed. Allowed: {', '.join(allowed_extensions)}"

    # Additional checks to prevent other path-based attacks
    # Check for null bytes
    if '\x00' in file_path:
        return False, "File path contains null byte character"

    # Check for potential command injection patterns
    dangerous_patterns = [';', '|', '&', '`', '$(', '${', '<', '>']
    for pattern in dangerous_patterns:
        if pattern in file_path:
            return False, f"File path contains potentially dangerous character sequence: {pattern}"

    return True, None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent security issues.

    Args:
        filename: Filename to sanitize

    Returns:
        Sanitized filename
    """
    if not filename:
        return ""

    # Remove potentially dangerous characters/sequences
    # Replace path separators to prevent directory traversal
    sanitized = filename.replace('/', '_').replace('\\', '_')

    # Remove null bytes
    sanitized = sanitized.replace('\x00', '')

    # Remove potentially dangerous sequences
    sanitized = sanitized.replace('..', 'dotdot')

    # Limit filename length to prevent buffer overflow issues
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:255-len(ext)] + ext

    return sanitized


def validate_url_security(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate URL for security issues like SSRF (Server-Side Request Forgery) prevention.

    Args:
        url: URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url:
        return False, "URL cannot be empty"

    # Basic URL format validation
    if not validators.url(url):
        return False, "Invalid URL format"

    # Parse the URL
    parsed = urlparse(url)

    # Check for potentially dangerous schemes
    allowed_schemes = ['http', 'https']
    if parsed.scheme not in allowed_schemes:
        return False, f"URL scheme '{parsed.scheme}' not allowed. Allowed: {', '.join(allowed_schemes)}"

    # Check for internal IP addresses to prevent SSRF
    hostname = parsed.hostname
    if hostname:
        # Check for internal/reserved IP addresses
        import ipaddress
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_reserved:
                return False, f"URL hostname '{hostname}' resolves to internal/reserved IP address"
        except ValueError:
            # Hostname is not an IP address, continue with string checks
            internal_hostnames = ['localhost', 'local', 'internal', 'intranet']
            if any(internal in hostname.lower() for internal in internal_hostnames):
                return False, f"URL hostname '{hostname}' appears to be internal"

            # Check for internal IP address patterns in hostname
            internal_patterns = [r'127\.', r'10\.', r'172\.(1[6-9]|2[0-9]|3[01])\.', r'192\.168\.']
            for pattern in internal_patterns:
                if re.search(pattern, hostname):
                    return False, f"URL hostname '{hostname}' appears to contain internal IP pattern"

    return True, None


def validate_content_security(content: str, max_length: int = 1000000) -> Tuple[bool, Optional[str]]:
    """
    Validate content for security issues like injection attacks.

    Args:
        content: Content to validate
        max_length: Maximum allowed content length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if content is None:
        return False, "Content cannot be None"

    # Check content length
    if len(content) > max_length:
        return False, f"Content length {len(content)} exceeds maximum allowed length of {max_length}"

    # Check for potentially dangerous patterns
    dangerous_patterns = [
        (r'<script[^>]*>.*?</script>', 'potential script tag injection'),
        (r'javascript:', 'potential JavaScript URL injection'),
        (r'vbscript:', 'potential VBScript injection'),
        (r'on\w+\s*=', 'potential event handler injection'),
        (r'<iframe[^>]*>.*?</iframe>', 'potential iframe injection'),
        (r'<object[^>]*>.*?</object>', 'potential object injection'),
        (r'<embed[^>]*>.*?</embed>', 'potential embed injection'),
    ]

    for pattern, description in dangerous_patterns:
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            return False, f"Content contains {description}"

    return True, None