"""Tests for the text extractor service"""
import pytest
from unittest.mock import Mock, patch, mock_open
import tempfile
import os
from src.services.text_extractor import TextExtractor


class TestTextExtractor:
    """Test cases for TextExtractor service"""

    def test_extract_text_from_pdf_success(self, sample_pdf_content):
        """Test successful text extraction from PDF"""
        # Create a temporary PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(sample_pdf_content)
            tmp_path = tmp.name

        try:
            extractor = TextExtractor()
            # Mock the fitz.open to return a mock document
            with patch('src.services.text_extractor.fitz') as mock_fitz:
                mock_doc = Mock()
                mock_page = Mock()
                mock_text_page = Mock()

                # Configure the mock to return our test content
                mock_text_page.extractText.return_value = "Test PDF content"
                mock_page.getTextPage.return_value = mock_text_page
                mock_doc.load_page.return_value = mock_page
                mock_doc.__len__.return_value = 1
                mock_fitz.open.return_value.__enter__.return_value = mock_doc

                result = extractor.extract_text_from_pdf(tmp_path)
                assert result == "Test PDF content"
        finally:
            os.unlink(tmp_path)

    def test_extract_text_from_docx_success(self, sample_docx_content):
        """Test successful text extraction from DOCX"""
        # Create a temporary DOCX file
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp.write(sample_docx_content)
            tmp_path = tmp.name

        try:
            extractor = TextExtractor()
            # Mock the docx functionality
            with patch('src.services.text_extractor.Document') as mock_document_class:
                mock_doc = Mock()
                mock_para1 = Mock()
                mock_para1.text = "Test paragraph 1"
                mock_para2 = Mock()
                mock_para2.text = "Test paragraph 2"
                mock_doc.paragraphs = [mock_para1, mock_para2]

                mock_document_class.return_value = mock_doc

                result = extractor.extract_text_from_docx(tmp_path)
                expected = "Test paragraph 1\nTest paragraph 2"
                assert result == expected
        finally:
            os.unlink(tmp_path)

    def test_extract_text_from_file_pdf(self, sample_pdf_content):
        """Test extract_text_from_file with PDF"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(sample_pdf_content)
            tmp_path = tmp.name

        try:
            extractor = TextExtractor()
            with patch.object(extractor, 'extract_text_from_pdf', return_value="PDF content"):
                result = extractor.extract_text_from_file(tmp_path)
                assert result == "PDF content"
        finally:
            os.unlink(tmp_path)

    def test_extract_text_from_file_docx(self, sample_docx_content):
        """Test extract_text_from_file with DOCX"""
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp.write(sample_docx_content)
            tmp_path = tmp.name

        try:
            extractor = TextExtractor()
            with patch.object(extractor, 'extract_text_from_docx', return_value="DOCX content"):
                result = extractor.extract_text_from_file(tmp_path)
                assert result == "DOCX content"
        finally:
            os.unlink(tmp_path)

    def test_extract_text_from_file_unsupported_type(self):
        """Test extract_text_from_file with unsupported file type"""
        extractor = TextExtractor()
        result = extractor.extract_text_from_file("test.txt")
        assert result == ""