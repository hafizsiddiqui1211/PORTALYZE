"""File validation utilities for Resume Analyzer Core"""
import os
from pathlib import Path
from typing import Tuple, Optional


def validate_file_type(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that the file is of a supported type (PDF or DOCX).

    Args:
        file_path: Path to the file to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in ['.pdf', '.docx']:
        return False, f"Unsupported file type: {extension}. Supported types: .pdf, .docx"

    return True, None


def validate_file_size(file_path: str, max_size: int = 10 * 1024 * 1024) -> Tuple[bool, Optional[str]]:  # 10MB
    """
    Validate that the file size is within the allowed limit.

    Args:
        file_path: Path to the file to validate
        max_size: Maximum allowed file size in bytes (default 10MB)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.exists(file_path):
        return False, f"File does not exist: {file_path}"

    file_size = os.path.getsize(file_path)

    if file_size > max_size:
        size_mb = max_size / (1024 * 1024)
        return False, f"File size {file_size} bytes exceeds maximum allowed size of {size_mb}MB"

    return True, None


def validate_file_content(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that the file has readable content.

    Args:
        file_path: Path to the file to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(file_path, 'rb') as f:
            # Try to read the first few bytes to check if it's readable
            f.read(100)
        return True, None
    except Exception as e:
        return False, f"File is not readable: {str(e)}"


def validate_file(file_path: str, max_size: int = 10 * 1024 * 1024) -> Tuple[bool, Optional[str]]:
    """
    Validate a file for type, size, and readability.

    Args:
        file_path: Path to the file to validate
        max_size: Maximum allowed file size in bytes (default 10MB)

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate file type
    is_valid_type, error_type = validate_file_type(file_path)
    if not is_valid_type:
        return False, error_type

    # Validate file size
    is_valid_size, error_size = validate_file_size(file_path, max_size)
    if not is_valid_size:
        return False, error_size

    # Validate file content
    is_valid_content, error_content = validate_file_content(file_path)
    if not is_valid_content:
        return False, error_content

    return True, None