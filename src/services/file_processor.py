"""File processing service for Resume Analyzer Core"""
from typing import Tuple, Optional
import os
from pathlib import Path
from src.utils.validators import validate_file
from src.utils.security import create_encrypted_temp_file, validate_file_access, generate_session_id
from src.models.resume import Resume
from src.utils.constants import SUPPORTED_FILE_TYPES, FILE_SIZE_LIMIT_MB
from src.utils.logger import get_logger


class FileProcessor:
    """Handles file upload, validation, and temporary storage"""

    def __init__(self, max_file_size: int = 10 * 1024 * 1024):  # 10MB default
        self.max_file_size = max_file_size
        self.logger = get_logger("FileProcessor")

    def generate_session_id(self) -> str:
        """
        Generate a unique session ID for tracking temporary file access.
        """
        import uuid
        return str(uuid.uuid4())

    def process_upload(self, file_content: bytes, original_filename: str) -> Tuple[Optional[Resume], Optional[str]]:
        """
        Process an uploaded file, validate it, store it temporarily, and return a Resume entity.

        Args:
            file_content: Raw bytes of the uploaded file
            original_filename: Original name of the uploaded file

        Returns:
            Tuple of (Resume entity if successful, error message if failed)
        """
        # Generate a session ID for this upload
        session_id = self.generate_session_id()

        # Log the file upload
        file_size = len(file_content)
        self.logger.info(f"Processing file upload: {original_filename}, size: {file_size} bytes, session: {session_id}")

        # Determine file type from extension
        file_extension = Path(original_filename).suffix.lower()
        if file_extension not in ['.pdf', '.docx']:
            supported_types_str = ', '.join([f.upper() for f in SUPPORTED_FILE_TYPES])
            error_msg = f"Unsupported file type: {file_extension}. Supported types: {supported_types_str}"
            self.logger.warning(f"File upload failed - unsupported type: {original_filename}, session: {session_id}")
            return None, error_msg

        # Calculate file size before creating temporary file
        file_size = len(file_content)
        if file_size > self.max_file_size:
            size_mb = self.max_file_size / (1024 * 1024)
            error_msg = f"File size {file_size} bytes exceeds maximum allowed size of {size_mb}MB"
            self.logger.warning(f"File upload failed - too large: {original_filename}, size: {file_size} bytes, session: {session_id}")
            return None, error_msg

        # Create temporary file using Python's tempfile module as required for cloud compatibility
        try:
            import tempfile
            # Create a temporary file with the correct extension
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
                tmp.write(file_content)
                temp_file_path = tmp.name
            self.logger.debug(f"Created temporary file: {temp_file_path} for session: {session_id}")
        except Exception as e:
            error_msg = f"Failed to create temporary file: {str(e)}"
            self.logger.error(f"File upload failed - could not create temp file: {original_filename}, session: {session_id}, error: {str(e)}")
            return None, error_msg

        # Validate the file
        is_valid, error_msg = validate_file(temp_file_path, self.max_file_size)
        if not is_valid:
            self.logger.warning(f"File validation failed: {original_filename}, session: {session_id}, error: {error_msg}")
            # Clean up the temporary file if validation fails
            try:
                os.remove(temp_file_path)
                self.logger.debug(f"Cleaned up temporary file after validation failure: {temp_file_path}")
            except:
                pass  # Ignore cleanup errors
            return None, error_msg

        # Extract text content from the file before creating Resume entity
        try:
            from src.services.text_extractor import TextExtractor
            text_extractor = TextExtractor()
            extracted_text = text_extractor.extract_text_from_file(temp_file_path)

            # Check if text extraction was successful
            if not extracted_text.strip():
                error_msg = f"Could not extract text from the uploaded file: {original_filename}"
                self.logger.warning(f"Text extraction failed: {original_filename}, session: {session_id}")
                # Clean up the temporary file
                try:
                    os.remove(temp_file_path)
                    self.logger.debug(f"Cleaned up temporary file after text extraction failure: {temp_file_path}")
                except:
                    pass  # Ignore cleanup errors
                return None, error_msg

        except Exception as e:
            error_msg = f"Failed to extract text from file: {str(e)}"
            self.logger.error(f"Text extraction failed: {original_filename}, session: {session_id}, error: {str(e)}")
            # Clean up the temporary file
            try:
                os.remove(temp_file_path)
                self.logger.debug(f"Cleaned up temporary file after text extraction failure: {temp_file_path}")
            except:
                pass  # Ignore cleanup errors
            return None, error_msg

        # Create Resume entity with extracted text content
        try:
            resume = Resume.create_new(
                original_filename=original_filename,
                file_type=file_extension[1:].upper(),  # Remove the dot and convert to uppercase
                file_path=temp_file_path,
                text_content=extracted_text,
                session_id=session_id
            )
            self.logger.info(f"Successfully processed file upload: {original_filename}, resume_id: {resume.resume_id}, session: {session_id}")
            return resume, None
        except Exception as e:
            self.logger.error(f"Resume entity creation failed: {original_filename}, session: {session_id}, error: {str(e)}")
            # Clean up the temporary file if entity creation fails
            try:
                os.remove(temp_file_path)
                self.logger.debug(f"Cleaned up temporary file after entity creation failure: {temp_file_path}")
            except:
                pass  # Ignore cleanup errors
            return None, f"Failed to create Resume entity: {str(e)}"

    def validate_and_access_file(self, file_path: str, session_id: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a file can be accessed within the context of a session.

        Args:
            file_path: Path to the file to validate
            session_id: Session ID for access validation

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate file path to prevent directory traversal
        from src.utils.security import validate_file_path, validate_file_size
        if not validate_file_path(file_path):
            return False, "Invalid file path - potential directory traversal detected"

        # Check if file exists first
        if not os.path.exists(file_path):
            return False, "File does not exist"

        # Validate file type
        file_extension = Path(file_path).suffix.lower()
        if file_extension not in ['.pdf', '.docx']:
            return False, f"Invalid file type: {file_extension}. Only PDF and DOCX files are allowed."

        # Validate file size
        if not validate_file_size(file_path, self.max_file_size):
            size_mb = self.max_file_size / (1024 * 1024)
            return False, f"File size exceeds maximum allowed size of {size_mb}MB"

        # Validate access via security module
        is_valid = validate_file_access(file_path, session_id)
        if not is_valid:
            return False, "File access denied or file not in allowed location"

        return True, None

    def cleanup_temp_file(self, file_path: str) -> bool:
        """
        Clean up a temporary file.

        Args:
            file_path: Path to the temporary file to clean up

        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.logger.debug(f"Cleaned up temporary file: {file_path}")
                return True
            else:
                self.logger.warning(f"Attempted to clean up non-existent file: {file_path}")
                return False
        except Exception as e:
            self.logger.error(f"Error cleaning up temporary file {file_path}: {str(e)}")
            return False

    def get_file_size_mb(self, file_path: str) -> float:
        """
        Get the size of a file in MB.

        Args:
            file_path: Path to the file

        Returns:
            File size in MB
        """
        if not os.path.exists(file_path):
            return 0.0
        return os.path.getsize(file_path) / (1024 * 1024)