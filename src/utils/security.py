"""Security utilities for Resume Analyzer Core"""
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import uuid
import json
from typing import Dict, List, Optional


def create_encrypted_temp_file(content: bytes, file_extension: str = "") -> str:
    """
    Create an encrypted temporary file for storing uploaded resume files.
    In a real implementation, this would use proper encryption.
    For this implementation, we're using obfuscated file names with a temporary directory.
    """
    # Create a temporary file with an obfuscated name
    temp_filename = f"temp_{uuid.uuid4().hex}{file_extension}"
    temp_path = os.path.join("data", "temp", temp_filename)

    with open(temp_path, 'wb') as f:
        f.write(content)

    return temp_path


def cleanup_old_temp_files(hours: int = 24):
    """
    Clean up temporary files older than specified hours (default 24 hours).
    """
    temp_dir = Path("data/temp")
    if not temp_dir.exists():
        return

    cutoff_time = datetime.now() - timedelta(hours=hours)

    for file_path in temp_dir.iterdir():
        if file_path.is_file():
            # Get file modification time
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mod_time < cutoff_time:
                try:
                    file_path.unlink()  # Delete the file
                except OSError:
                    pass  # Ignore errors when deleting files


def validate_file_access(file_path: str, session_id: str) -> bool:
    """
    Validate that a file can be accessed within the context of a session.
    This is a basic check to ensure the file exists and is in the expected location.
    """
    path = Path(file_path)

    # Ensure the file is in the temp directory
    temp_dir = Path("data/temp").resolve()
    file_dir = path.parent.resolve()

    if temp_dir != file_dir:
        return False

    # Check if file exists
    if not path.exists():
        return False

    # Additional security checks
    # 1. Check if the path is trying to escape the allowed directory (path traversal)
    try:
        path.resolve().relative_to(temp_dir)
    except ValueError:
        # Path is outside the allowed directory
        return False

    # 2. Check if the file is actually a file, not a directory
    if not path.is_file():
        return False

    # 3. Check file permissions (readable)
    if not os.access(path, os.R_OK):
        return False

    return True


def validate_file_path(file_path: str, allowed_base_dir: str = "data/temp") -> bool:
    """
    Validate a file path to prevent directory traversal attacks.

    Args:
        file_path: The file path to validate
        allowed_base_dir: The allowed base directory

    Returns:
        True if the path is valid and safe, False otherwise
    """
    try:
        # Convert to Path object
        path = Path(file_path)

        # Resolve the path to get the absolute path
        resolved_path = path.resolve()

        # Get the allowed base directory
        base_dir = Path(allowed_base_dir).resolve()

        # Check if the resolved path is within the allowed base directory
        resolved_path.relative_to(base_dir)
        return True
    except (ValueError, RuntimeError):
        # Path is outside the allowed directory or cannot be resolved
        return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent security issues.

    Args:
        filename: The original filename

    Returns:
        Sanitized filename
    """
    import re

    # Remove potentially dangerous characters
    # Keep only alphanumeric characters, dots, hyphens, and underscores
    sanitized = re.sub(r'[^\w\-_\.]', '_', filename)

    # Prevent directory traversal
    sanitized = sanitized.replace('../', '').replace('..\\', '')

    # Limit length to prevent potential issues
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:255-len(ext)] + ext

    return sanitized


def validate_file_size(file_path: str, max_size: int = 10 * 1024 * 1024) -> bool:
    """
    Validate that a file size is within allowed limits.

    Args:
        file_path: Path to the file to check
        max_size: Maximum allowed file size in bytes (default 10MB)

    Returns:
        True if file size is within limits, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            return False

        file_size = os.path.getsize(file_path)
        return file_size <= max_size
    except:
        return False


def generate_session_id() -> str:
    """
    Generate a unique session ID for tracking temporary file access.
    """
    return str(uuid.uuid4())


def hash_file_content(content: bytes) -> str:
    """
    Generate a hash of file content for integrity checking.
    """
    return hashlib.sha256(content).hexdigest()


def create_session_record(session_id: str, file_paths: List[str],
                        created_at: datetime = None) -> str:
    """
    Create a session record to track files associated with a session.

    Args:
        session_id: The session ID
        file_paths: List of file paths associated with the session
        created_at: Optional creation time (defaults to now)

    Returns:
        Path to the session record file
    """
    if created_at is None:
        created_at = datetime.now()

    session_record = {
        "session_id": session_id,
        "file_paths": file_paths,
        "created_at": created_at.isoformat(),
        "expires_at": (created_at + timedelta(hours=24)).isoformat()
    }

    session_dir = Path("data/temp/sessions")
    session_dir.mkdir(parents=True, exist_ok=True)

    session_file_path = session_dir / f"{session_id}.json"

    with open(session_file_path, 'w') as f:
        json.dump(session_record, f)

    return str(session_file_path)


def get_session_files(session_id: str) -> List[str]:
    """
    Get the list of files associated with a session.

    Args:
        session_id: The session ID

    Returns:
        List of file paths associated with the session
    """
    session_dir = Path("data/temp/sessions")
    session_file_path = session_dir / f"{session_id}.json"

    if not session_file_path.exists():
        return []

    try:
        with open(session_file_path, 'r') as f:
            session_record = json.load(f)
        return session_record.get("file_paths", [])
    except:
        return []


def cleanup_session_files(session_id: str) -> bool:
    """
    Clean up all files associated with a session.

    Args:
        session_id: The session ID

    Returns:
        True if successful, False otherwise
    """
    session_files = get_session_files(session_id)
    success = True

    for file_path in session_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            success = False

    # Remove the session record file
    session_dir = Path("data/temp/sessions")
    session_file_path = session_dir / f"{session_id}.json"

    try:
        if session_file_path.exists():
            os.remove(session_file_path)
    except:
        success = False

    return success


def cleanup_expired_sessions() -> int:
    """
    Clean up all expired sessions and their associated files.

    Returns:
        Number of sessions cleaned up
    """
    session_dir = Path("data/temp/sessions")
    if not session_dir.exists():
        return 0

    now = datetime.now()
    cleaned_count = 0

    for session_file in session_dir.glob("*.json"):
        try:
            with open(session_file, 'r') as f:
                session_record = json.load(f)

            expires_at_str = session_record.get("expires_at")
            if expires_at_str:
                expires_at = datetime.fromisoformat(expires_at_str)

                if now > expires_at:
                    session_id = session_record.get("session_id")
                    if session_id:
                        cleanup_session_files(session_id)
                        cleaned_count += 1
        except:
            # If there's an error reading the session file, try to delete it
            try:
                os.remove(session_file)
                cleaned_count += 1
            except:
                pass

    return cleaned_count


def cleanup_old_temp_files_with_sessions(hours: int = 24):
    """
    Enhanced cleanup that handles both direct temp files and session-based files.

    Args:
        hours: Number of hours after which files are considered old
    """
    # Cleanup direct temp files
    cleanup_old_temp_files(hours)

    # Cleanup expired sessions
    cleaned_sessions = cleanup_expired_sessions()

    print(f"Cleaned up {cleaned_sessions} expired sessions")