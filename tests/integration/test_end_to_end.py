"""End-to-end integration tests for Resume Analyzer Core"""
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Import all the necessary modules
from src.services.file_processor import FileProcessor
from src.services.text_extractor import TextExtractor
from src.services.ats_analyzer import ATSAnalyzer
from src.services.ai_service import AIService
from src.services.keyword_analyzer import KeywordAnalyzer
from src.services.pdf_generator import PDFGenerator
from src.models.resume import Resume
from src.models.analysis import AnalysisResult
from src.models.suggestions import KeywordSuggestion


class TestEndToEndWorkflow:
    """Test the complete resume analysis workflow"""

    def test_complete_resume_analysis_workflow(self, sample_pdf_content):
        """Test the complete workflow: upload -> extract -> analyze -> suggest -> report"""
        # Create temporary files for testing
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
            tmp_pdf.write(sample_pdf_content)
            tmp_pdf_path = tmp_pdf.name

        try:
            # Step 1: File processing
            file_processor = FileProcessor()
            resume, error = file_processor.process_upload(sample_pdf_content, "test_resume.pdf")
            assert error is None
            assert resume is not None
            assert resume.file_type == "PDF"

            # Step 2: Text extraction
            text_extractor = TextExtractor()
            extracted_text = text_extractor.extract_text_from_file(resume.file_path)
            # Even with a minimal PDF, we should get some text or at least no error
            assert isinstance(extracted_text, str)

            # Step 3: ATS Analysis
            ats_analyzer = ATSAnalyzer()
            ats_score = ats_analyzer.calculate_ats_score(extracted_text or "Software Engineer with experience")
            assert isinstance(ats_score, float)
            assert 0 <= ats_score <= 100

            # Step 4: AI Analysis
            ai_service = AIService(api_key="test-key")  # Using test key to avoid real API calls
            ai_analysis = ai_service.analyze_resume(extracted_text or "Software Engineer with experience", ats_score)
            assert "strengths" in ai_analysis
            assert "weaknesses" in ai_analysis
            assert "section_feedback" in ai_analysis
            assert "overall_feedback" in ai_analysis
            assert "confidence_level" in ai_analysis

            # Step 5: Create AnalysisResult
            analysis_result = AnalysisResult.create_new(
                resume_id=resume.resume_id,
                ats_score=ats_score,
                strengths=ai_analysis["strengths"],
                weaknesses=ai_analysis["weaknesses"],
                section_feedback=ai_analysis["section_feedback"],
                overall_feedback=ai_analysis["overall_feedback"],
                confidence_level=ai_analysis["confidence_level"]
            )
            assert analysis_result is not None

            # Step 6: Generate keyword suggestions
            keyword_suggestions = ai_service.generate_keyword_suggestions(
                extracted_text or "Software Engineer with experience",
                analysis_result
            )
            assert isinstance(keyword_suggestions, list)

            # Step 7: Verify keyword suggestions are properly formed
            if keyword_suggestions:
                for suggestion in keyword_suggestions:
                    assert hasattr(suggestion, 'keyword')
                    assert hasattr(suggestion, 'relevance_score')
                    assert hasattr(suggestion, 'category')
                    assert hasattr(suggestion, 'justification')
                    assert 0 <= suggestion.relevance_score <= 1

            # Step 8: Generate PDF report
            pdf_generator = PDFGenerator()
            pdf_path = pdf_generator.generate_analysis_report(analysis_result, keyword_suggestions)
            assert os.path.exists(pdf_path)
            assert pdf_path.endswith('.pdf')

            # Clean up generated PDF
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        finally:
            # Clean up temporary file
            if os.path.exists(tmp_pdf_path):
                os.remove(tmp_pdf_path)

    def test_complete_workflow_with_docx_file(self, sample_docx_content):
        """Test the complete workflow with a DOCX file"""
        # Create temporary files for testing
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_docx:
            tmp_docx.write(sample_docx_content)
            tmp_docx_path = tmp_docx.name

        try:
            # Step 1: File processing
            file_processor = FileProcessor()
            resume, error = file_processor.process_upload(sample_docx_content, "test_resume.docx")
            assert error is None
            assert resume is not None
            assert resume.file_type == "DOCX"

            # Step 2: Text extraction
            text_extractor = TextExtractor()
            extracted_text = text_extractor.extract_text_from_file(resume.file_path)
            # The sample docx should contain "Test content"
            assert "Test content" in extracted_text

            # Step 3: ATS Analysis
            ats_analyzer = ATSAnalyzer()
            ats_score = ats_analyzer.calculate_ats_score(extracted_text)
            assert isinstance(ats_score, float)
            assert 0 <= ats_score <= 100

            # Step 4: AI Analysis
            ai_service = AIService(api_key="test-key")
            ai_analysis = ai_service.analyze_resume(extracted_text, ats_score)
            assert "strengths" in ai_analysis
            assert "weaknesses" in ai_analysis

            # Step 5: Create AnalysisResult
            analysis_result = AnalysisResult.create_new(
                resume_id=resume.resume_id,
                ats_score=ats_score,
                strengths=ai_analysis["strengths"],
                weaknesses=ai_analysis["weaknesses"],
                section_feedback=ai_analysis["section_feedback"],
                overall_feedback=ai_analysis["overall_feedback"],
                confidence_level=ai_analysis["confidence_level"]
            )
            assert analysis_result is not None

            # Step 6: Generate keyword suggestions
            keyword_suggestions = ai_service.generate_keyword_suggestions(
                extracted_text,
                analysis_result
            )
            assert isinstance(keyword_suggestions, list)

            # Step 7: Generate summary PDF report
            pdf_generator = PDFGenerator()
            pdf_path = pdf_generator.generate_summary_report(analysis_result, keyword_suggestions)
            assert os.path.exists(pdf_path)
            assert pdf_path.endswith('.pdf')

            # Clean up generated PDF
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        finally:
            # Clean up temporary file
            if os.path.exists(tmp_docx_path):
                os.remove(tmp_docx_path)

    def test_error_handling_in_complete_workflow(self):
        """Test that errors are properly handled in the workflow"""
        # Test with empty content
        file_processor = FileProcessor()
        resume, error = file_processor.process_upload(b"", "empty_file.pdf")
        # This might succeed since we're just creating a temp file, but extraction should fail later

        text_extractor = TextExtractor()
        # Try to extract from an empty/non-existent file - should handle gracefully
        extracted_text = text_extractor.extract_text_from_file("non_existent_file.pdf")
        assert extracted_text == ""  # Should return empty string on failure

        # ATS analyzer should handle empty text gracefully
        ats_analyzer = ATSAnalyzer()
        ats_score = ats_analyzer.calculate_ats_score("")
        assert ats_score == 0.0  # Should return 0 for empty text

    def test_keyword_analyzer_integration(self):
        """Test the keyword analyzer service integration"""
        keyword_analyzer = KeywordAnalyzer()

        # Test with sample resume text
        resume_text = """
        Software Engineer with 3 years of experience in Python, JavaScript, and React.
        Experience with AWS, Docker, and CI/CD pipelines.
        Bachelor's degree in Computer Science.
        """

        # Get role-specific keywords
        role_keywords = keyword_analyzer.get_role_specific_keywords("Software Engineer")
        assert len(role_keywords) > 0

        # Get relevant keywords from resume
        relevant_keywords = keyword_analyzer.get_relevant_keywords(resume_text, "Software Engineer")
        assert len(relevant_keywords) > 0
        # Should contain some of the keywords mentioned in the text
        assert any(keyword in resume_text for keyword in relevant_keywords)

        # Generate keyword suggestions
        suggestions = keyword_analyzer.generate_keyword_suggestions(resume_text, "Software Engineer")
        assert isinstance(suggestions, list)

        # Check that suggestions have the right structure
        for suggestion in suggestions:
            assert isinstance(suggestion, KeywordSuggestion)
            assert hasattr(suggestion, 'keyword')
            assert hasattr(suggestion, 'relevance_score')
            assert 0 <= suggestion.relevance_score <= 1

    def test_pdf_generation_with_realistic_data(self):
        """Test PDF generation with realistic analysis data"""
        # Create realistic analysis data
        analysis_result = AnalysisResult.create_new(
            resume_id="test-resume-123",
            ats_score=75.5,
            strengths=[
                "Strong technical skills in Python",
                "Good experience with web development",
                "Solid understanding of software architecture"
            ],
            weaknesses=[
                "Limited experience with cloud technologies",
                "Could benefit from more project leadership examples"
            ],
            section_feedback={
                "experience": "Good experience section with clear responsibilities",
                "skills": "Technical skills well presented",
                "education": "Education properly formatted"
            },
            overall_feedback="Overall strong resume with good technical foundation. Consider adding more cloud experience.",
            confidence_level=0.85
        )

        # Create keyword suggestions
        keyword_suggestions = [
            KeywordSuggestion.create_new(
                analysis_id=analysis_result.analysis_id,
                keyword="AWS",
                relevance_score=0.8,
                category="Technical",
                justification="Cloud experience is highly valued in software engineering roles",
                role_alignment="Software Engineer"
            ),
            KeywordSuggestion.create_new(
                analysis_id=analysis_result.analysis_id,
                keyword="Docker",
                relevance_score=0.75,
                category="Tool",
                justification="Containerization skills are increasingly important",
                role_alignment="Software Engineer"
            )
        ]

        # Generate PDFs
        pdf_generator = PDFGenerator()

        # Test full report
        full_pdf_path = pdf_generator.generate_analysis_report(analysis_result, keyword_suggestions)
        assert os.path.exists(full_pdf_path)
        assert os.path.getsize(full_pdf_path) > 0  # File should have content

        # Test summary report
        summary_pdf_path = pdf_generator.generate_summary_report(analysis_result, keyword_suggestions)
        assert os.path.exists(summary_pdf_path)
        assert os.path.getsize(summary_pdf_path) > 0  # File should have content

        # Clean up
        os.remove(full_pdf_path)
        os.remove(summary_pdf_path)

    def test_performance_requirements(self, sample_docx_content):
        """Test that the workflow meets performance requirements"""
        import time

        # Record start time
        start_time = time.time()

        # Run a simplified version of the workflow
        file_processor = FileProcessor()
        resume, error = file_processor.process_upload(sample_docx_content, "perf_test.docx")
        assert error is None

        text_extractor = TextExtractor()
        extracted_text = text_extractor.extract_text_from_file(resume.file_path)
        assert extracted_text

        ats_analyzer = ATSAnalyzer()
        ats_score = ats_analyzer.calculate_ats_score(extracted_text)

        ai_service = AIService(api_key="test-key")
        ai_analysis = ai_service.analyze_resume(extracted_text, ats_score)

        analysis_result = AnalysisResult.create_new(
            resume_id=resume.resume_id,
            ats_score=ats_score,
            strengths=ai_analysis["strengths"],
            weaknesses=ai_analysis["weaknesses"],
            section_feedback=ai_analysis["section_feedback"],
            overall_feedback=ai_analysis["overall_feedback"],
            confidence_level=ai_analysis["confidence_level"]
        )

        keyword_suggestions = ai_service.generate_keyword_suggestions(extracted_text, analysis_result)

        # Check that the workflow completed within reasonable time (e.g., 15 seconds)
        elapsed_time = time.time() - start_time
        assert elapsed_time < 15.0, f"Workflow took too long: {elapsed_time:.2f}s"

        # Clean up the temporary resume file
        file_processor.cleanup_temp_file(resume.file_path)