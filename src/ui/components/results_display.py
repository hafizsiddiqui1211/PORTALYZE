"""Results display components for Resume Analyzer Core"""
import streamlit as st
from typing import Dict, List, Optional
from src.models.profile_analysis import ProfileAnalysis
from src.models.profile_url import ProfileURL


def render_analysis_results(profile_analysis: Optional[ProfileAnalysis], profile_url: Optional[ProfileURL] = None):
    """
    Render the analysis results for a profile.

    Args:
        profile_analysis: ProfileAnalysis entity containing the analysis results
        profile_url: Optional ProfileURL entity for additional context
    """
    if profile_analysis is None:
        st.warning("No analysis results available to display.")
        return

    st.header(f"📊 Analysis Results for {profile_analysis.profile_type} Profile")

    if profile_url:
        st.write(f"**URL:** {profile_url.url}")

    # Display overall scores
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Overall Score",
            value=f"{profile_analysis.overall_score:.1f}/100",
            delta=get_score_delta_text(profile_analysis.overall_score)
        )

    with col2:
        st.metric(
            label="Clarity Score",
            value=f"{profile_analysis.clarity_score:.1f}/100",
            delta=get_score_delta_text(profile_analysis.clarity_score)
        )

    with col3:
        st.metric(
            label="Impact Score",
            value=f"{profile_analysis.impact_score:.1f}/100",
            delta=get_score_delta_text(profile_analysis.impact_score)
        )

    # Display strengths
    if profile_analysis.strengths:
        with st.expander("✅ Strengths", expanded=True):
            for strength in profile_analysis.strengths:
                st.success(f"• {strength}")

    # Display weaknesses
    if profile_analysis.weaknesses:
        with st.expander("⚠️ Areas for Improvement", expanded=True):
            for weakness in profile_analysis.weaknesses:
                st.warning(f"• {weakness}")

    # Display suggestions
    if profile_analysis.suggestions:
        with st.expander("💡 Improvement Suggestions", expanded=True):
            for suggestion in profile_analysis.suggestions:
                render_suggestion_item(suggestion)

    # Display detailed feedback
    if profile_analysis.detailed_feedback:
        with st.expander("📝 Detailed Feedback", expanded=False):
            st.write(profile_analysis.detailed_feedback)


def render_suggestion_item(suggestion: Dict):
    """
    Render an individual suggestion item with appropriate styling.

    Args:
        suggestion: Dictionary containing suggestion details
    """
    # Determine icon and color based on priority
    priority = suggestion.get('priority', 'MEDIUM').upper()

    if priority == 'HIGH':
        icon = "🔴"
        color = "#dc3545"  # Red
    elif priority == 'LOW':
        icon = "🟡"
        color = "#ffc107"  # Yellow
    else:  # MEDIUM
        icon = "🟡"
        color = "#fd7e14"  # Orange

    st.markdown(
        f"""
        <div style="
            background-color: #f8f9fa;
            border-left: 4px solid {color};
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 0 4px 4px 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <strong>{icon} {suggestion.get('title', 'Suggestion')}</strong><br>
                    <small>{suggestion.get('description', '')}</small>
                </div>
                <div style="text-align: right; color: {color}; font-weight: bold; min-width: 60px;">
                    {priority}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_profile_comparison(analyses: List[ProfileAnalysis]):
    """
    Render a comparison view of multiple profile analyses.

    Args:
        analyses: List of ProfileAnalysis entities to compare
    """
    if not analyses or len(analyses) < 2:
        st.info("Add more profile analyses to enable comparison view.")
        return

    st.header("⚖️ Profile Comparison")

    # Create comparison table
    comparison_data = []
    for analysis in analyses:
        comparison_data.append({
            'Profile Type': analysis.profile_type,
            'Overall Score': f"{analysis.overall_score:.1f}",
            'Clarity Score': f"{analysis.clarity_score:.1f}",
            'Impact Score': f"{analysis.impact_score:.1f}",
            'Strengths Count': len(analysis.strengths),
            'Weaknesses Count': len(analysis.weaknesses)
        })

    import pandas as pd
    df = pd.DataFrame(comparison_data)
    st.table(df)

    # Visual comparison
    st.subheader("Visual Score Comparison")
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(10, 6))

    profile_types = [analysis.profile_type for analysis in analyses]
    overall_scores = [analysis.overall_score for analysis in analyses]
    clarity_scores = [analysis.clarity_score for analysis in analyses]
    impact_scores = [analysis.impact_score for analysis in analyses]

    x = np.arange(len(profile_types))
    width = 0.25

    ax.bar(x - width, overall_scores, width, label='Overall Score', alpha=0.8)
    ax.bar(x, clarity_scores, width, label='Clarity Score', alpha=0.8)
    ax.bar(x + width, impact_scores, width, label='Impact Score', alpha=0.8)

    ax.set_xlabel('Profile Type')
    ax.set_ylabel('Score')
    ax.set_title('Profile Analysis Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(profile_types)
    ax.legend()

    # Add value labels on bars
    for i, (os, cs, is_) in enumerate(zip(overall_scores, clarity_scores, impact_scores)):
        ax.text(i - width, os + 1, f'{os:.1f}', ha='center', va='bottom', fontsize=9)
        ax.text(i, cs + 1, f'{cs:.1f}', ha='center', va='bottom', fontsize=9)
        ax.text(i + width, is_ + 1, f'{is_:.1f}', ha='center', va='bottom', fontsize=9)

    st.pyplot(fig)
    plt.clf()  # Clear figure to free memory


def render_detailed_feedback_sections(profile_analysis: ProfileAnalysis):
    """
    Render detailed feedback organized by sections.

    Args:
        profile_analysis: ProfileAnalysis entity with section feedback
    """
    if not hasattr(profile_analysis, 'section_feedback') or not profile_analysis.section_feedback:
        st.info("No section-specific feedback available.")
        return

    st.subheader("📋 Section-Specific Feedback")

    for section_name, feedback in profile_analysis.section_feedback.items():
        with st.expander(f"**{section_name.title()} Section**", expanded=False):
            if isinstance(feedback, dict):
                # If feedback is structured, display different aspects
                for aspect, detail in feedback.items():
                    st.write(f"**{aspect.replace('_', ' ').title()}:** {detail}")
            else:
                # If feedback is just text, display as is
                st.write(feedback)


def render_keyword_suggestions(suggestions: List[Dict]):
    """
    Render keyword suggestions for profile improvement.

    Args:
        suggestions: List of keyword suggestion dictionaries
    """
    if not suggestions:
        st.info("No keyword suggestions available.")
        return

    st.subheader("🔑 Keyword Suggestions")

    # Group suggestions by category if available
    categories = {}
    for suggestion in suggestions:
        category = suggestion.get('category', 'General')
        if category not in categories:
            categories[category] = []
        categories[category].append(suggestion)

    # Create tabs for each category
    if len(categories) > 1:
        category_tabs = st.tabs(list(categories.keys()))
        for i, (category, category_suggestions) in enumerate(categories.items()):
            with category_tabs[i]:
                st.write(f"#### {category} Keywords")
                for suggestion in category_suggestions:
                    render_keyword_suggestion_item(suggestion)
    else:
        # If only one category, display directly
        for suggestion in suggestions:
            render_keyword_suggestion_item(suggestion)


def render_keyword_suggestion_item(suggestion: Dict):
    """
    Render an individual keyword suggestion with details.

    Args:
        suggestion: Dictionary containing keyword suggestion details
    """
    keyword = suggestion.get('keyword', 'N/A')
    relevance = suggestion.get('relevance_score', 0)
    category = suggestion.get('category', 'General')
    justification = suggestion.get('justification', 'No justification provided')
    role_alignment = suggestion.get('role_alignment', 'Various roles')

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(
            f"""
            <div style="
                background-color: #e9ecef;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 10px;
            ">
                <div style="font-weight: bold; color: #495057;">{keyword}</div>
                <div style="font-size: 0.9em; color: #6c757d; margin: 5px 0;">
                    <strong>Justification:</strong> {justification}
                </div>
                <div style="font-size: 0.8em; color: #adb5bd;">
                    <strong>Role Alignment:</strong> {role_alignment}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # Display relevance score as a progress bar
        st.write(f"**Relevance:** {relevance*100:.0f}%")
        st.progress(relevance)


def get_score_delta_text(score: float) -> str:
    """
    Get appropriate delta text for a score.

    Args:
        score: The score value (0-100)

    Returns:
        Delta text string
    """
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    else:
        return "Needs Work"


def render_analysis_summary_card(profile_analysis: ProfileAnalysis):
    """
    Render a summary card for the analysis results.

    Args:
        profile_analysis: ProfileAnalysis entity to summarize
    """
    st.markdown(
        f"""
        <div style="
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: #495057;">{profile_analysis.profile_type} Profile Analysis</h3>
                    <p style="margin: 8px 0 0 0; color: #6c757d; font-size: 0.9em;">
                        Overall Score: <strong>{profile_analysis.overall_score:.1f}/100</strong>
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.5em; font-weight: bold; color: {get_score_color(profile_analysis.overall_score)};">
                        {profile_analysis.overall_score:.0f}
                    </div>
                    <div style="font-size: 0.8em; color: #6c757d;">
                        {get_score_level(profile_analysis.overall_score)}
                    </div>
                </div>
            </div>

            <div style="margin-top: 12px; display: flex; justify-content: space-around; text-align: center;">
                <div>
                    <div style="font-weight: bold; color: {get_score_color(profile_analysis.clarity_score)}">{profile_analysis.clarity_score:.0f}</div>
                    <div style="font-size: 0.8em; color: #6c757d;">Clarity</div>
                </div>
                <div>
                    <div style="font-weight: bold; color: {get_score_color(profile_analysis.impact_score)}">{profile_analysis.impact_score:.0f}</div>
                    <div style="font-size: 0.8em; color: #6c757d;">Impact</div>
                </div>
                <div>
                    <div style="font-weight: bold;">{len(profile_analysis.strengths)}</div>
                    <div style="font-size: 0.8em; color: #6c757d;">Strengths</div>
                </div>
                <div>
                    <div style="font-weight: bold;">{len(profile_analysis.weaknesses)}</div>
                    <div style="font-size: 0.8em; color: #6c757d;">Areas for Improvement</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_score_color(score: float) -> str:
    """
    Get appropriate color for a score.

    Args:
        score: The score value (0-100)

    Returns:
        Hex color string
    """
    if score >= 80:
        return "#28a745"  # Green
    elif score >= 60:
        return "#ffc107"  # Yellow
    elif score >= 40:
        return "#fd7e14"  # Orange
    else:
        return "#dc3545"  # Red


def get_score_level(score: float) -> str:
    """
    Get textual level for a score.

    Args:
        score: The score value (0-100)

    Returns:
        Textual level string
    """
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Fair"
    else:
        return "Needs Improvement"


def render_strengths_weaknesses_side_by_side(profile_analysis: ProfileAnalysis):
    """
    Render strengths and weaknesses in side-by-side columns.

    Args:
        profile_analysis: ProfileAnalysis entity with strengths and weaknesses
    """
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Strengths")
        if profile_analysis.strengths:
            for strength in profile_analysis.strengths:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #d4edda;
                        border: 1px solid #c3e6cb;
                        border-radius: 4px;
                        padding: 8px;
                        margin-bottom: 8px;
                    ">
                        • {strength}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No specific strengths identified.")

    with col2:
        st.subheader("⚠️ Areas for Improvement")
        if profile_analysis.weaknesses:
            for weakness in profile_analysis.weaknesses:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f8d7da;
                        border: 1px solid #f5c6cb;
                        border-radius: 4px;
                        padding: 8px;
                        margin-bottom: 8px;
                    ">
                        • {weakness}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No specific weaknesses identified.")


def render_export_options(profile_analysis: ProfileAnalysis, profile_url: Optional[ProfileURL] = None):
    """
    Render options for exporting analysis results.

    Args:
        profile_analysis: ProfileAnalysis entity to export
        profile_url: Optional ProfileURL for context
    """
    st.subheader("💾 Export Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Export as PDF"):
            # Placeholder for PDF export functionality
            st.info("PDF export functionality would be implemented here")

    with col2:
        if st.button("Export as JSON"):
            # Prepare data for JSON export
            export_data = {
                "profile_type": profile_analysis.profile_type,
                "url": profile_url.url if profile_url else "N/A",
                "overall_score": profile_analysis.overall_score,
                "clarity_score": profile_analysis.clarity_score,
                "impact_score": profile_analysis.impact_score,
                "strengths": profile_analysis.strengths,
                "weaknesses": profile_analysis.weaknesses,
                "suggestions": profile_analysis.suggestions,
                "detailed_feedback": profile_analysis.detailed_feedback
            }

            import json
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"{profile_analysis.profile_type.lower()}_analysis.json",
                mime="application/json"
            )

    with col3:
        if st.button("Export as Text"):
            # Prepare text export
            text_content = f"""
Profile Analysis Results
======================

Profile Type: {profile_analysis.profile_type}
URL: {profile_url.url if profile_url else "N/A"}

Scores:
- Overall: {profile_analysis.overall_score}/100
- Clarity: {profile_analysis.clarity_score}/100
- Impact: {profile_analysis.impact_score}/100

Strengths:
{chr(10).join([f"- {s}" for s in profile_analysis.strengths]) if profile_analysis.strengths else "None identified"}

Areas for Improvement:
{chr(10).join([f"- {w}" for w in profile_analysis.weaknesses]) if profile_analysis.weaknesses else "None identified"}

Suggestions:
{chr(10).join([f"- {s.get('title', '')}: {s.get('description', '')}" for s in profile_analysis.suggestions]) if profile_analysis.suggestions else "None provided"}
            """

            st.download_button(
                label="Download Text",
                data=text_content.strip(),
                file_name=f"{profile_analysis.profile_type.lower()}_analysis.txt",
                mime="text/plain"
            )