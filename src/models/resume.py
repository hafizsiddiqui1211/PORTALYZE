"""Resume entity for Resume Analyzer Core"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
import uuid


@dataclass
class Resume:
    """Represents a user-uploaded resume file and its extracted content"""

    resume_id: str
    original_filename: str
    file_type: str  # PDF or DOCX
    file_path: str  # Temporary encrypted storage path
    text_content: str  # Extracted text from the resume
    metadata: Dict[str, Any]  # Extracted metadata (creation date, author, etc.)
    upload_timestamp: datetime
    session_id: str

    def __post_init__(self):
        """Validate the Resume entity after initialization"""
        if self.file_type not in ["PDF", "DOCX"]:
            raise ValueError("file_type must be PDF or DOCX")

        if not self.file_path or not self.text_content:
            raise ValueError("file_path and text_content must not be empty")

    @classmethod
    def create_new(cls, original_filename: str, file_type: str, file_path: str,
                   text_content: str, session_id: str) -> 'Resume':
        """Create a new Resume entity with generated ID and timestamp"""
        return cls(
            resume_id=str(uuid.uuid4()),
            original_filename=original_filename,
            file_type=file_type,
            file_path=file_path,
            text_content=text_content,
            metadata={},
            upload_timestamp=datetime.now(),
            session_id=session_id
        )