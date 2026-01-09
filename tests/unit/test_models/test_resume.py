"""Tests for the Resume model"""
import pytest
from datetime import datetime
from src.models.resume import Resume


class TestResume:
    """Test cases for Resume entity"""

    def test_resume_creation_success(self):
        """Test successful creation of a Resume entity"""
        resume = Resume(
            resume_id="test-id",
            original_filename="test_resume.pdf",
            file_type="PDF",
            file_path="/tmp/test_resume.pdf",
            text_content="Test resume content",
            metadata={"author": "Test Author"},
            upload_timestamp=datetime.now(),
            session_id="test-session"
        )

        assert resume.resume_id == "test-id"
        assert resume.original_filename == "test_resume.pdf"
        assert resume.file_type == "PDF"
        assert resume.file_path == "/tmp/test_resume.pdf"
        assert resume.text_content == "Test resume content"
        assert resume.metadata == {"author": "Test Author"}
        assert resume.session_id == "test-session"

    def test_resume_creation_with_invalid_file_type(self):
        """Test Resume creation fails with invalid file type"""
        with pytest.raises(ValueError, match="file_type must be PDF or DOCX"):
            Resume(
                resume_id="test-id",
                original_filename="test_resume.txt",
                file_type="TXT",  # Invalid type
                file_path="/tmp/test_resume.txt",
                text_content="Test resume content",
                metadata={"author": "Test Author"},
                upload_timestamp=datetime.now(),
                session_id="test-session"
            )

    def test_resume_creation_with_empty_file_path(self):
        """Test Resume creation fails with empty file path"""
        with pytest.raises(ValueError, match="file_path and text_content must not be empty"):
            Resume(
                resume_id="test-id",
                original_filename="test_resume.pdf",
                file_type="PDF",
                file_path="",  # Empty path
                text_content="Test resume content",
                metadata={"author": "Test Author"},
                upload_timestamp=datetime.now(),
                session_id="test-session"
            )

    def test_resume_creation_with_empty_text_content(self):
        """Test Resume creation fails with empty text content"""
        with pytest.raises(ValueError, match="file_path and text_content must not be empty"):
            Resume(
                resume_id="test-id",
                original_filename="test_resume.pdf",
                file_type="PDF",
                file_path="/tmp/test_resume.pdf",
                text_content="",  # Empty content
                metadata={"author": "Test Author"},
                upload_timestamp=datetime.now(),
                session_id="test-session"
            )

    def test_resume_create_new_method(self):
        """Test the create_new class method"""
        resume = Resume.create_new(
            original_filename="test_resume.pdf",
            file_type="PDF",
            file_path="/tmp/test_resume.pdf",
            text_content="Test resume content",
            session_id="test-session"
        )

        # Should have generated a valid UUID
        assert resume.resume_id is not None
        assert resume.resume_id != ""
        assert resume.original_filename == "test_resume.pdf"
        assert resume.file_type == "PDF"
        assert resume.file_path == "/tmp/test_resume.pdf"
        assert resume.text_content == "Test resume content"
        assert resume.session_id == "test-session"
        assert resume.upload_timestamp is not None

    def test_resume_create_new_method_docx(self):
        """Test the create_new class method with DOCX"""
        resume = Resume.create_new(
            original_filename="test_resume.docx",
            file_type="DOCX",
            file_path="/tmp/test_resume.docx",
            text_content="Test resume content",
            session_id="test-session"
        )

        assert resume.file_type == "DOCX"
        assert resume.original_filename == "test_resume.docx"