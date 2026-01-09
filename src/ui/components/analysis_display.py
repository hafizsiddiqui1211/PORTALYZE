"""Analysis display component for Resume Analyzer Core"""
import streamlit as st
from src.models.analysis import AnalysisResult
from src.models.suggestions import KeywordSuggestion
from typing import List


def render_analysis_results(analysis_result: AnalysisResult, keyword_suggestions: List[KeywordSuggestion]):
    """
    Render the analysis results in a user-friendly format.

    Args:
        analysis_result: The analysis result to display
        keyword_suggestions: List of keyword suggestions to display
    """
    # Display ATS Score prominently
    st.header("Analysis Results")

    # ATS Score display
    col1, col2, col3 = st.columns(3)
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
            label="ATS Compatibility Score",
            value=f"{ats_score:.1f}/100",
            delta=f"{score_text}",
            delta_color="normal" if ats_score >= 60 else "inverse"
        )

    # Confidence level
    with col2:
        confidence_pct = analysis_result.confidence_level * 100
        st.metric(
            label="Analysis Confidence",
            value=f"{confidence_pct:.0f}%",
            delta="High" if confidence_pct >= 80 else "Medium" if confidence_pct >= 60 else "Low"
        )

    # Number of suggestions
    with col3:
        st.metric(
            label="Keyword Suggestions",
            value=len(keyword_suggestions),
            delta="Helpful" if len(keyword_suggestions) > 0 else "None"
        )

    # Strengths section
    st.subheader("Strengths 💚")
    if analysis_result.strengths:
        for strength in analysis_result.strengths:
            st.success(f"✅ {strength}")
    else:
        st.info("No specific strengths identified.")

    # Weaknesses section
    st.subheader("Areas for Improvement 🟡")
    if analysis_result.weaknesses:
        for weakness in analysis_result.weaknesses:
            st.warning(f"⚠️ {weakness}")
    else:
        st.info("No specific weaknesses identified.")

    # Section feedback
    st.subheader("Section Feedback 📝")
    if analysis_result.section_feedback:
        for section_name, feedback in analysis_result.section_feedback.items():
            with st.expander(f"{section_name.title()} Section"):
                st.write(feedback)
    else:
        st.info("No section-specific feedback available.")

    # Overall feedback
    st.subheader("Overall Feedback")
    if analysis_result.overall_feedback:
        st.info(analysis_result.overall_feedback)
    else:
        st.info("No overall feedback available.")

    # Keyword suggestions
    if keyword_suggestions:
        st.subheader("Keyword Suggestions for Improvement 🔑")
        for suggestion in keyword_suggestions:
            with st.container():
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**{suggestion.keyword}** - {suggestion.justification}")
                with col2:
                    st.caption(f"Relevance: {suggestion.relevance_score:.2f}")
                    st.caption(f"Category: {suggestion.category}")


def render_analysis_summary(analysis_result: AnalysisResult):
    """
    Render a compact summary of the analysis results.

    Args:
        analysis_result: The analysis result to display
    """
    st.subheader("Analysis Summary")

    # Brief overview
    st.write(f"**ATS Score:** {analysis_result.ats_score:.1f}/100")
    st.write(f"**Confidence:** {analysis_result.confidence_level:.2f}")

    # Strengths preview
    if analysis_result.strengths:
        st.write("**Key Strengths:**")
        for strength in analysis_result.strengths[:3]:  # Show first 3 strengths
            st.write(f"- {strength}")

    # Weaknesses preview
    if analysis_result.weaknesses:
        st.write("**Areas to Improve:**")
        for weakness in analysis_result.weaknesses[:3]:  # Show first 3 weaknesses
            st.write(f"- {weakness}")


def render_strengths_weaknesses(analysis_result: AnalysisResult):
    """
    Render strengths and weaknesses in a side-by-side layout.

    Args:
        analysis_result: The analysis result to display
    """
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Strengths 💚")
        if analysis_result.strengths:
            for strength in analysis_result.strengths:
                st.success(f"✅ {strength}")
        else:
            st.info("No specific strengths identified.")

    with col2:
        st.subheader("Areas for Improvement 🟡")
        if analysis_result.weaknesses:
            for weakness in analysis_result.weaknesses:
                st.warning(f"⚠️ {weakness}")
        else:
            st.info("No specific weaknesses identified.")