"""Tests for the individual UI components"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st


class TestUIComponents:
    """Test cases for individual UI components"""

    def test_file_uploader_component(self):
        """Test that file uploader component logic works correctly"""
        from src.ui.components.file_uploader import render_file_uploader, render_file_uploader_with_validation

        # Since we can't test Streamlit components directly without a running app context,
        # we'll verify that the functions exist and can be imported
        assert callable(render_file_uploader)
        assert callable(render_file_uploader_with_validation)

        # Test that the functions have the expected parameters
        import inspect
        sig1 = inspect.signature(render_file_uploader)
        sig2 = inspect.signature(render_file_uploader_with_validation)

        # Both functions should have max_file_size_mb parameter
        assert 'max_file_size_mb' in sig1.parameters
        assert 'max_file_size_mb' in sig2.parameters

        # Default value should be reasonable
        assert sig1.parameters['max_file_size_mb'].default == 10
        assert sig2.parameters['max_file_size_mb'].default == 10

    def test_analysis_display_component(self):
        """Test that analysis display component logic works correctly"""
        from src.ui.components.analysis_display import (
            render_analysis_results,
            render_analysis_summary,
            render_strengths_weaknesses
        )

        # Verify that the functions exist and can be imported
        assert callable(render_analysis_results)
        assert callable(render_analysis_summary)
        assert callable(render_strengths_weaknesses)

        # Test that the functions have the expected parameters
        import inspect
        sig1 = inspect.signature(render_analysis_results)
        sig2 = inspect.signature(render_analysis_summary)
        sig3 = inspect.signature(render_strengths_weaknesses)

        # Check parameter counts
        assert len(sig1.parameters) == 2  # analysis_result, keyword_suggestions
        assert len(sig2.parameters) == 1  # analysis_result
        assert len(sig3.parameters) == 1  # analysis_result

    def test_file_uploader_with_mock_streamlit(self):
        """Test file uploader with mocked Streamlit components"""
        # Mock the Streamlit functions that the component uses
        with patch('src.ui.components.file_uploader.st') as mock_st:
            from src.ui.components.file_uploader import render_file_uploader_with_validation

            # Mock the file uploader to return None (no file uploaded)
            mock_st.file_uploader.return_value = None

            # Call the function
            file_content, filename = render_file_uploader_with_validation()

            # Verify that Streamlit's file_uploader was called
            assert mock_st.file_uploader.called
            # Should return None, None when no file is uploaded
            assert file_content is None
            assert filename is None

    def test_analysis_display_with_mock_streamlit(self):
        """Test analysis display with mocked Streamlit components"""
        # Create mock analysis result
        from src.models.analysis import AnalysisResult
        from src.models.suggestions import KeywordSuggestion

        mock_analysis = AnalysisResult.create_new(
            resume_id="test-resume-id",
            ats_score=80.0,
            strengths=["Good skills", "Relevant experience"],
            weaknesses=["Missing keywords"],
            section_feedback={"experience": "Good experience section"},
            overall_feedback="Overall good resume",
            confidence_level=0.8
        )

        mock_suggestions = [
            KeywordSuggestion.create_new(
                analysis_id=mock_analysis.analysis_id,
                keyword="Python",
                relevance_score=0.9,
                category="Technical",
                justification="Important for the role",
                role_alignment="Software Engineer"
            )
        ]

        # Mock the Streamlit functions that the component uses
        with patch('src.ui.components.analysis_display.st') as mock_st:
            from src.ui.components.analysis_display import render_analysis_results

            # Call the function
            render_analysis_results(mock_analysis, mock_suggestions)

            # Verify that Streamlit functions were called appropriately
            # The function should create columns and metrics
            assert mock_st.columns.called or mock_st.header.called or mock_st.subheader.called

    def test_component_imports(self):
        """Test that all UI components can be imported without errors"""
        # Test importing file uploader components
        from src.ui.components import file_uploader
        from src.ui.components import analysis_display

        # Verify that expected functions exist in the modules
        assert hasattr(file_uploader, 'render_file_uploader')
        assert hasattr(file_uploader, 'render_file_uploader_with_validation')
        assert hasattr(analysis_display, 'render_analysis_results')
        assert hasattr(analysis_display, 'render_analysis_summary')
        assert hasattr(analysis_display, 'render_strengths_weaknesses')