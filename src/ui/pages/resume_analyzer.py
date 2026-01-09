"""Resume Analyzer page for Resume Analyzer Core"""

import streamlit as st
from typing import Optional
from src.models.analysis import AnalysisResult
from src.services.file_processor import FileProcessor
from src.services.text_extractor import TextExtractor
from src.services.ats_analyzer import ATSAnalyzer
from src.services.ai_service import AIService
from src.ui.components.file_uploader import render_file_uploader_with_validation
from src.ui.dashboard import render_dashboard
from src.utils.constants import MAX_FILE_SIZE


def render_resume_analyzer_page(
    file_processor: FileProcessor,
    text_extractor: TextExtractor,
    ats_analyzer: ATSAnalyzer,
    ai_service: AIService,
):
    """Render the resume analyzer page."""
    st.title("📄 PORTALYZE")
    st.subheader(
        "Analyze your resume for ATS compatibility and get AI-powered feedback"
    )

    # Main content area
    if not st.session_state.resume_analyzed:
        # Upload section
        file_content, original_filename = render_file_uploader_with_validation(
            max_file_size_mb=MAX_FILE_SIZE // (1024 * 1024)  # Convert bytes to MB
        )

        if file_content and original_filename:
            with st.spinner("Processing your resume..."):
                try:
                    # Process the uploaded file - this now includes text extraction
                    resume, error = file_processor.process_upload(
                        file_content, original_filename
                    )
                    if error:
                        st.error(f"Error processing file: {error}")
                        return

                    # Use the text content that was already extracted during file processing
                    extracted_text = resume.text_content
                    if not extracted_text.strip():
                        st.error(
                            "Could not extract text from the uploaded file. Please check the file format."
                        )
                        return

                    # Calculate ATS score
                    ats_score = ats_analyzer.calculate_ats_score(extracted_text)

                    # Perform AI analysis
                    ai_analysis = ai_service.analyze_resume(extracted_text, ats_score)

                    # Create AnalysisResult
                    analysis_result = AnalysisResult.create_new(
                        resume_id=resume.resume_id,
                        ats_score=ats_score,
                        strengths=ai_analysis["strengths"],
                        weaknesses=ai_analysis["weaknesses"],
                        section_feedback=ai_analysis["section_feedback"],
                        overall_feedback=ai_analysis["overall_feedback"],
                        confidence_level=ai_analysis["confidence_level"],
                    )

                    # Generate keyword suggestions
                    keyword_suggestions = ai_service.generate_keyword_suggestions(
                        extracted_text, analysis_result
                    )

                    # Store results in session state
                    st.session_state.analysis_result = analysis_result
                    st.session_state.keyword_suggestions = keyword_suggestions
                    st.session_state.original_filename = original_filename
                    st.session_state.resume_analyzed = True

                    st.success("Resume analyzed successfully!")
                    st.rerun()

                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
                    return
    else:
        # Display dashboard with analysis results
        if st.session_state.analysis_result:
            render_dashboard(
                analysis_result=st.session_state.analysis_result,
                keyword_suggestions=st.session_state.keyword_suggestions,
                show_sidebar=False,  # Sidebar already shown in main
            )

            # Add a button to analyze another resume
            if st.button("🔄 Analyze Another Resume"):
                st.session_state.resume_analyzed = False
                st.session_state.analysis_result = None
                st.session_state.keyword_suggestions = []
                st.session_state.original_filename = ""
                st.rerun()

        else:
            st.error(
                "No analysis results available. Please go back and upload a resume."
            )
