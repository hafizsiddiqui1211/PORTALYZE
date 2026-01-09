"""Section feedback component for Resume Analyzer Core"""
import streamlit as st
from typing import Dict, List, Optional


def render_section_feedback(section_feedback: Dict[str, str], show_header: bool = True):
    """
    Render expandable section-by-section feedback.

    Args:
        section_feedback: Dictionary with section names as keys and feedback as values
        show_header: Whether to show the section header
    """
    if show_header:
        st.subheader("📋 Section-by-Section Feedback")

    if not section_feedback:
        st.info("No section-specific feedback available.")
        return

    # Define standard sections in a preferred order
    standard_sections = ["summary", "experience", "skills", "education", "projects", "certifications", "awards"]

    # First, render standard sections in order
    for section in standard_sections:
        if section.lower() in section_feedback:
            _render_single_section(section, section_feedback[section.lower()])

    # Then render any remaining sections that aren't standard
    for section, feedback in section_feedback.items():
        if section.lower() not in standard_sections:
            _render_single_section(section, feedback)


def _render_single_section(section_name: str, feedback: str):
    """
    Render a single section's feedback in an expandable format.

    Args:
        section_name: Name of the resume section
        feedback: Feedback for the section
    """
    # Capitalize section name for display
    display_name = section_name.replace('_', ' ').replace('-', ' ').title()

    # Choose an appropriate icon based on section name
    icon = _get_section_icon(section_name.lower())

    with st.expander(f"{icon} {display_name} Section"):
        st.write(feedback)


def _get_section_icon(section_name: str) -> str:
    """
    Get an appropriate icon for a section.

    Args:
        section_name: Name of the section

    Returns:
        Emoji icon for the section
    """
    icon_map = {
        'summary': '📝',
        'objective': '🎯',
        'experience': '💼',
        'work': '💼',
        'employment': '💼',
        'skills': '🛠️',
        'technologies': '💻',
        'education': '🎓',
        'academic': '🎓',
        'projects': '🏗️',
        'portfolio': '🖼️',
        'certifications': '📜',
        'licenses': '📜',
        'awards': '🏆',
        'achievements': '🏆',
        'publications': '📚',
        'research': '🔬',
        'contact': '📞',
        'personal': '👤',
        'references': '👥'
    }

    return icon_map.get(section_name, '📄')  # Default icon if not found


def render_section_feedback_detailed(section_feedback: Dict[str, str],
                                   strengths_by_section: Optional[Dict[str, List[str]]] = None,
                                   weaknesses_by_section: Optional[Dict[str, List[str]]] = None):
    """
    Render detailed section feedback with strengths and weaknesses per section.

    Args:
        section_feedback: Dictionary with section names as keys and feedback as values
        strengths_by_section: Optional dictionary of strengths for each section
        weaknesses_by_section: Optional dictionary of weaknesses for each section
    """
    st.subheader("📋 Detailed Section Feedback")

    if not section_feedback:
        st.info("No section-specific feedback available.")
        return

    # Group all sections together
    all_sections = set(section_feedback.keys())
    if strengths_by_section:
        all_sections.update(strengths_by_section.keys())
    if weaknesses_by_section:
        all_sections.update(weaknesses_by_section.keys())

    # Define standard sections in a preferred order
    standard_sections = ["summary", "experience", "skills", "education", "projects", "certifications", "awards"]

    # First, render standard sections in order
    for section in standard_sections:
        if section.lower() in all_sections:
            _render_detailed_section(section, section_feedback, strengths_by_section, weaknesses_by_section)

    # Then render any remaining sections that aren't standard
    for section in all_sections:
        if section.lower() not in standard_sections:
            _render_detailed_section(section, section_feedback, strengths_by_section, weaknesses_by_section)


def _render_detailed_section(section_name: str,
                           section_feedback: Dict[str, str],
                           strengths_by_section: Optional[Dict[str, List[str]]],
                           weaknesses_by_section: Optional[Dict[str, List[str]]]):
    """
    Render a single section's detailed feedback.

    Args:
        section_name: Name of the resume section
        section_feedback: Dictionary of section feedback
        strengths_by_section: Optional dictionary of strengths for each section
        weaknesses_by_section: Optional dictionary of weaknesses for each section
    """
    # Capitalize section name for display
    display_name = section_name.replace('_', ' ').replace('-', ' ').title()

    # Choose an appropriate icon based on section name
    icon = _get_section_icon(section_name.lower())

    with st.expander(f"{icon} {display_name} Section"):
        # Show general feedback
        if section_name.lower() in section_feedback:
            st.write("**General Feedback:**")
            st.info(section_feedback[section_name.lower()])

        # Show strengths for this section
        if strengths_by_section and section_name.lower() in strengths_by_section:
            strengths = strengths_by_section[section_name.lower()]
            if strengths:
                st.write("**Strengths:**")
                for strength in strengths:
                    st.success(f"✅ {strength}")

        # Show weaknesses for this section
        if weaknesses_by_section and section_name.lower() in weaknesses_by_section:
            weaknesses = weaknesses_by_section[section_name.lower()]
            if weaknesses:
                st.write("**Areas for Improvement:**")
                for weakness in weaknesses:
                    st.warning(f"⚠️ {weakness}")


def render_section_feedback_summary(section_feedback: Dict[str, str]):
    """
    Render a compact summary of section feedback.

    Args:
        section_feedback: Dictionary with section names as keys and feedback as values
    """
    st.subheader("📋 Section Feedback Summary")

    if not section_feedback:
        st.info("No section-specific feedback available.")
        return

    # Create columns for a compact view
    sections = list(section_feedback.keys())
    if len(sections) <= 3:
        cols = st.columns(len(sections))
    else:
        cols = st.columns(3)  # Max 3 columns

    for i, section in enumerate(sections):
        with cols[i % len(cols)]:
            display_name = section.replace('_', ' ').replace('-', ' ').title()
            icon = _get_section_icon(section.lower())

            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f8f9fa;
                        border: 1px solid #dee2e6;
                        border-radius: 5px;
                        padding: 10px;
                        margin-bottom: 10px;
                    ">
                        <div style="font-weight: bold; color: #495057;">
                            {icon} {display_name}
                        </div>
                        <div style="font-size: 0.9em; margin-top: 5px;">
                            {section_feedback[section][:100] + '...' if len(section_feedback[section]) > 100 else section_feedback[section]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def get_standard_sections() -> List[str]:
    """
    Get a list of standard resume sections.

    Returns:
        List of standard resume section names
    """
    return [
        "summary",
        "experience",
        "skills",
        "education",
        "projects",
        "certifications",
        "awards",
        "contact"
    ]


def render_section_feedback_by_importance(section_feedback: Dict[str, str],
                                        importance_scores: Optional[Dict[str, float]] = None):
    """
    Render section feedback ordered by importance.

    Args:
        section_feedback: Dictionary with section names as keys and feedback as values
        importance_scores: Optional dictionary with section names as keys and importance scores as values
    """
    st.subheader("📋 Section Feedback by Importance")

    if not section_feedback:
        st.info("No section-specific feedback available.")
        return

    # If importance scores are provided, sort sections by importance
    if importance_scores:
        sorted_sections = sorted(section_feedback.keys(),
                               key=lambda x: importance_scores.get(x.lower(), 0),
                               reverse=True)
    else:
        # Default order: prioritize key sections
        priority_order = ["experience", "skills", "education", "projects", "summary"]
        sorted_sections = []

        # Add priority sections first
        for section in priority_order:
            if section in section_feedback:
                sorted_sections.append(section)

        # Add remaining sections
        for section in section_feedback.keys():
            if section not in sorted_sections:
                sorted_sections.append(section)

    # Render sections in order of importance
    for section in sorted_sections:
        display_name = section.replace('_', ' ').replace('-', ' ').title()
        icon = _get_section_icon(section.lower())

        # Show importance score if available
        score_text = ""
        if importance_scores and section in importance_scores:
            score = importance_scores[section]
            # Use color based on importance
            color = "#dc3545" if score >= 0.8 else "#ffc107" if score >= 0.5 else "#6c757d"
            score_text = f" <span style='color: {color}; font-size: 0.8em;'>(Importance: {score:.2f})</span>"

        with st.expander(f"{icon} {display_name}{score_text}", unsafe_allow_html=True):
            st.write(section_feedback[section])