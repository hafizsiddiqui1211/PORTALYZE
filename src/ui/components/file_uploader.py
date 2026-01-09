"""File uploader component for Resume Analyzer Core"""
import streamlit as st
from typing import Optional, Tuple
from pathlib import Path


def render_file_uploader(max_file_size_mb: int = 10) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Render a file uploader component for PDF and DOCX files.

    Args:
        max_file_size_mb: Maximum allowed file size in MB (default 10)

    Returns:
        Tuple of (file_content_bytes, original_filename) or (None, None) if no file uploaded
    """
    # Calculate max size in bytes
    max_file_size_bytes = max_file_size_mb * 1024 * 1024

    # Create the file uploader
    uploaded_file = st.file_uploader(
        label="Upload your resume",
        type=["pdf", "docx"],
        accept_multiple_files=False,
        help=f"Upload a PDF or DOCX file (max {max_file_size_mb}MB)"
    )

    if uploaded_file is not None:
        # Check file size
        file_size = len(uploaded_file.getvalue())
        if file_size > max_file_size_bytes:
            st.error(f"File size exceeds {max_file_size_mb}MB limit. Please upload a smaller file.")
            return None, None

        # Get file content and name
        file_content = uploaded_file.getvalue()
        original_filename = uploaded_file.name

        # Validate file type based on extension
        file_extension = Path(original_filename).suffix.lower()
        if file_extension not in ['.pdf', '.docx']:
            st.error(f"Unsupported file type: {file_extension}. Please upload a PDF or DOCX file.")
            return None, None

        return file_content, original_filename

    return None, None


def render_file_uploader_with_validation(max_file_size_mb: int = 10) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Render a file uploader with additional validation messages.

    Args:
        max_file_size_mb: Maximum allowed file size in MB (default 10)

    Returns:
        Tuple of (file_content_bytes, original_filename) or (None, None) if no valid file uploaded
    """
    st.subheader("Resume Upload")
    st.write("Upload your resume in PDF or DOCX format for ATS analysis")

    # File uploader
    uploaded_file = st.file_uploader(
        label="Choose a resume file",
        type=["pdf", "docx"],
        accept_multiple_files=False,
        help=f"Supported formats: PDF, DOCX. Maximum size: {max_file_size_mb}MB"
    )

    if uploaded_file is not None:
        # Show file info
        file_size = len(uploaded_file.getvalue())
        file_size_mb = file_size / (1024 * 1024)

        # Check file size
        if file_size > max_file_size_mb * 1024 * 1024:
            st.error(f"❌ File size ({file_size_mb:.2f}MB) exceeds limit ({max_file_size_mb}MB)")
            return None, None
        else:
            st.success(f"✅ File size: {file_size_mb:.2f}MB (within limit)")

        # Validate file type
        original_filename = uploaded_file.name
        file_extension = Path(original_filename).suffix.lower()

        if file_extension not in ['.pdf', '.docx']:
            st.error(f"❌ Unsupported file type: {file_extension}")
            return None, None
        else:
            st.success(f"✅ File type: {file_extension.upper()}")

        # Show file name
        st.info(f"📄 Selected file: {original_filename}")

        return uploaded_file.getvalue(), original_filename

    return None, None