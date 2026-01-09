"""Dashboard UI for Resume Analyzer Core"""
import streamlit as st
from typing import Optional
from src.models.analysis import AnalysisResult
from src.models.suggestions import KeywordSuggestion


def render_dashboard(analysis_result: Optional[AnalysisResult] = None,
                    keyword_suggestions: Optional[list] = None,
                    role_recommendations: Optional[list] = None,
                    profile_analyses: Optional[dict] = None,
                    show_sidebar: bool = True):
    """
    Render the main dashboard with all analysis components.

    Args:
        analysis_result: The analysis result to display
        keyword_suggestions: List of keyword suggestions to display
        role_recommendations: List of role recommendations to display
        profile_analyses: Dictionary of profile analyses (LinkedIn, GitHub, Portfolio)
        show_sidebar: Whether to show the sidebar with additional information
    """
    # Set up the main layout
    st.title("📄 Smart Resume Analyzer Dashboard")

    if show_sidebar:
        _render_sidebar()

    # Create navigation tabs for different phases
    nav_tabs = ["Resume Analysis", "Profile Analysis", "Role Recommendations", "Combined View"]
    nav_tab_handles = st.tabs(nav_tabs)

    # Resume Analysis Tab
    with nav_tab_handles[0]:
        if analysis_result is not None:
            _render_analysis_header(analysis_result)

            # Create tabs for different views within resume analysis
            tab_names = ["📊 Overview", "✅ Strengths & Weaknesses", "📋 Section Feedback", "🔑 Keyword Suggestions"]
            tabs = st.tabs(tab_names)

            with tabs[0]:
                _render_overview_tab(analysis_result, keyword_suggestions)

            with tabs[1]:
                _render_strengths_weaknesses_tab(analysis_result)

            with tabs[2]:
                _render_section_feedback_tab(analysis_result)

            with tabs[3]:
                _render_keyword_suggestions_tab(keyword_suggestions)

            # Add PDF download button in the main area
            _render_pdf_download(analysis_result, keyword_suggestions)
        else:
            st.info("Complete resume analysis to see results here.")

    # Profile Analysis Tab
    with nav_tab_handles[1]:
        if profile_analyses:
            _render_profile_analysis_tab(profile_analyses)
        else:
            st.info("Complete profile analysis to see results here.")

    # Role Recommendations Tab
    with nav_tab_handles[2]:
        if role_recommendations:
            _render_role_recommendations_tab(role_recommendations)
        else:
            st.info("Complete role recommendations analysis to see results here.")

    # Combined View Tab
    with nav_tab_handles[3]:
        _render_combined_view_tab(analysis_result, profile_analyses, role_recommendations)


def _render_profile_analysis_tab(profile_analyses: dict):
    """Render the profile analysis tab."""
    st.subheader("📊 Profile Analysis Results")

    if not profile_analyses:
        st.info("No profile analysis available.")
        return

    for profile_type, analysis in profile_analyses.items():
        with st.expander(f"{profile_type.title()} Analysis", expanded=True):
            if 'strengths' in analysis:
                st.write("**Strengths:**")
                for strength in analysis['strengths']:
                    st.write(f"- {strength}")

            if 'weaknesses' in analysis:
                st.write("**Weaknesses:**")
                for weakness in analysis['weaknesses']:
                    st.write(f"- {weakness}")

            if 'suggestions' in analysis:
                st.write("**Suggestions:**")
                for suggestion in analysis['suggestions']:
                    st.write(f"- {suggestion}")


def _render_combined_view_tab(analysis_result: Optional[AnalysisResult],
                             profile_analyses: Optional[dict],
                             role_recommendations: Optional[list]):
    """Render the combined view tab with all insights."""
    st.subheader("🔗 Combined Career Insights")

    col1, col2 = st.columns(2)

    with col1:
        if analysis_result:
            st.write("**Resume Insights:**")
            st.metric("ATS Score", f"{analysis_result.ats_score:.1f}")
            st.write(f"**Strengths:** {len(analysis_result.strengths)} identified")
            st.write(f"**Areas for Improvement:** {len(analysis_result.weaknesses)} identified")

    with col2:
        if profile_analyses:
            st.write("**Profile Insights:**")
            st.write(f"**Profiles Analyzed:** {len(profile_analyses)}")
            total_suggestions = 0
            for profile_type, analysis in profile_analyses.items():
                if 'suggestions' in analysis:
                    total_suggestions += len(analysis['suggestions'])
            st.write(f"**Profile Suggestions:** {total_suggestions} identified")

    if role_recommendations:
        st.write("**Role Recommendations:**")
        from src.ui.components.role_card import show_multiple_role_cards
        show_multiple_role_cards(role_recommendations[:3])  # Show top 3 recommendations

        if len(role_recommendations) > 3:
            st.write(f"Plus {len(role_recommendations) - 3} more recommendations available.")


def _render_role_recommendations_tab(role_recommendations: list):
    """Render the role recommendations tab."""
    if not role_recommendations:
        st.info("No role recommendations available. Complete profile analysis to get personalized role suggestions.")
        return

    from src.ui.components.role_card import show_multiple_role_cards

    st.subheader("🎯 Role Recommendations")
    st.write("Based on your profile, here are some roles that might be a good fit:")

    # Display role recommendations
    show_multiple_role_cards(role_recommendations)


def _render_pdf_download(analysis_result: AnalysisResult, keyword_suggestions: list):
    """Render the PDF download functionality."""
    import os
    from src.services.pdf_generator import PDFGenerator

    st.subheader("📥 Download Analysis Report")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Full Report PDF"):
            try:
                generator = PDFGenerator()
                # Generate the PDF report
                pdf_path = generator.generate_analysis_report(
                    analysis_result=analysis_result,
                    keyword_suggestions=keyword_suggestions or []
                )

                # Read the PDF file and offer for download
                with open(pdf_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()

                st.download_button(
                    label="📥 Download Full Report",
                    data=pdf_bytes,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )

                st.success(f"Full report generated: {pdf_path}")
            except Exception as e:
                st.error(f"Error generating full report: {str(e)}")

    with col2:
        if st.button("Generate Summary Report PDF"):
            try:
                generator = PDFGenerator()
                # Generate the summary PDF report
                pdf_path = generator.generate_summary_report(
                    analysis_result=analysis_result,
                    keyword_suggestions=keyword_suggestions or []
                )

                # Read the PDF file and offer for download
                with open(pdf_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()

                st.download_button(
                    label="📥 Download Summary Report",
                    data=pdf_bytes,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )

                st.success(f"Summary report generated: {pdf_path}")
            except Exception as e:
                st.error(f"Error generating summary report: {str(e)}")


def _render_sidebar():
    """Render the sidebar with additional information."""
    with st.sidebar:
        st.header("📋 About This Analysis")
        st.write("""
        This dashboard provides:
        - ATS compatibility scoring
        - Strengths and weaknesses identification
        - Section-by-section feedback
        - Keyword suggestions for improvement
        """)

        st.header("ℹ️ How to Use")
        st.write("""
        1. Review your ATS score
        2. Examine strengths to maintain
        3. Address weaknesses for improvement
        4. Use keyword suggestions to optimize
        """)

        st.header("🎯 Improvement Tips")
        st.write("""
        - Use keywords from job descriptions
        - Quantify your achievements
        - Ensure consistent formatting
        - Include relevant technical skills
        """)


def _render_empty_state():
    """Render the empty state when no analysis is available."""
    st.subheader("Welcome to Resume Analyzer!")
    st.write("Upload your resume to get started with ATS compatibility analysis.")

    st.info("""
    🔍 **What we analyze:**
    - ATS compatibility score (0-100)
    - Resume strengths and weaknesses
    - Section-by-section feedback
    - Keyword suggestions for improvement
    """)

    # Add some example metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ATS Score", "N/A", "Upload resume to analyze")
    with col2:
        st.metric("Strengths", "N/A", "Analyze to find")
    with col3:
        st.metric("Suggestions", "N/A", "Analyze to get")


def _render_analysis_header(analysis_result: AnalysisResult):
    """Render the analysis header with key metrics."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ats_score = analysis_result.ats_score
        if ats_score >= 80:
            score_color = "green"
            score_text = "Excellent"
        elif ats_score >= 60:
            score_color = "orange"
            score_text = "Good"
        elif ats_score >= 40:
            score_color = "yellow"
            score_text = "Fair"
        else:
            score_color = "red"
            score_text = "Needs Improvement"

        st.metric(
            label="ATS Score",
            value=f"{ats_score:.1f}",
            delta=f"{score_text}",
            delta_color="normal" if ats_score >= 60 else "inverse"
        )

    with col2:
        confidence_pct = analysis_result.confidence_level * 100
        st.metric(
            label="Confidence",
            value=f"{confidence_pct:.0f}%",
            delta="High" if confidence_pct >= 80 else "Medium" if confidence_pct >= 60 else "Low"
        )

    with col3:
        strengths_count = len(analysis_result.strengths)
        st.metric(
            label="Strengths",
            value=strengths_count,
            delta="Good" if strengths_count >= 3 else "Consider improving"
        )

    with col4:
        weaknesses_count = len(analysis_result.weaknesses)
        st.metric(
            label="Areas for Improvement",
            value=weaknesses_count,
            delta="Good" if weaknesses_count <= 3 else "Needs attention"
        )


def _render_overview_tab(analysis_result: AnalysisResult, keyword_suggestions: Optional[list]):
    """Render the overview tab."""
    from src.ui.components.score_display import render_ats_score
    from src.ui.components.analysis_display import render_analysis_summary

    # ATS Score visualization
    render_ats_score(analysis_result.ats_score)

    # Analysis summary
    render_analysis_summary(analysis_result)

    # Overall feedback
    st.subheader("📝 Overall Feedback")
    st.info(analysis_result.overall_feedback)


def _render_strengths_weaknesses_tab(analysis_result: AnalysisResult):
    """Render the strengths and weaknesses tab."""
    from src.ui.components.strengths_panel import render_strengths_expandable
    from src.ui.components.weaknesses_panel import render_weaknesses_expandable

    col1, col2 = st.columns(2)

    with col1:
        render_strengths_expandable(analysis_result.strengths)

    with col2:
        render_weaknesses_expandable(analysis_result.weaknesses)


def _render_section_feedback_tab(analysis_result: AnalysisResult):
    """Render the section feedback tab."""
    from src.ui.components.section_feedback import render_section_feedback

    render_section_feedback(analysis_result.section_feedback)


def _render_keyword_suggestions_tab(keyword_suggestions: Optional[list]):
    """Render the keyword suggestions tab."""
    if not keyword_suggestions:
        st.info("No keyword suggestions available.")
        return

    st.subheader("🔑 Keyword Suggestions for Improvement")

    # Group suggestions by category
    categories = {}
    for suggestion in keyword_suggestions:
        category = getattr(suggestion, 'category', 'General')
        if category not in categories:
            categories[category] = []
        categories[category].append(suggestion)

    # Create tabs for each category
    if len(categories) > 1:
        category_tabs = st.tabs(list(categories.keys()))
        for i, (category, suggestions) in enumerate(categories.items()):
            with category_tabs[i]:
                _render_keyword_category(suggestions)
    else:
        # If only one category or no categories, just render all suggestions
        _render_keyword_category(keyword_suggestions)


def _render_keyword_category(suggestions: list):
    """Render suggestions for a specific category."""
    # Use the new keyword suggestions component
    from src.ui.components.keyword_suggestions import render_keyword_suggestions
    render_keyword_suggestions(suggestions, show_header=False)


def render_simple_dashboard(analysis_result: AnalysisResult, keyword_suggestions: list):
    """
    Render a simplified dashboard without tabs.

    Args:
        analysis_result: The analysis result to display
        keyword_suggestions: List of keyword suggestions to display
    """
    st.title("📄 Resume Analysis Results")

    # Header with key metrics
    _render_analysis_header(analysis_result)

    # ATS Score
    from src.ui.components.score_display import render_ats_score
    render_ats_score(analysis_result.ats_score, show_details=False)

    # Strengths and Weaknesses side by side
    from src.ui.components.analysis_display import render_strengths_weaknesses
    render_strengths_weaknesses(analysis_result)

    # Section feedback
    from src.ui.components.section_feedback import render_section_feedback
    render_section_feedback(analysis_result.section_feedback)

    # Keyword suggestions
    _render_keyword_suggestions_tab(keyword_suggestions)