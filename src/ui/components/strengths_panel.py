"""Strengths panel component for Resume Analyzer Core"""
import streamlit as st
from typing import List


def render_strengths(strengths: List[str], show_header: bool = True, max_strengths: int = None):
    """
    Render a green-themed panel displaying resume strengths.

    Args:
        strengths: List of strength descriptions
        show_header: Whether to show the section header
        max_strengths: Maximum number of strengths to display (None for all)
    """
    if show_header:
        st.subheader("✅ Strengths")

    if not strengths:
        st.info("No specific strengths identified in the resume.")
        return

    # Limit the number of strengths if specified
    strengths_to_show = strengths[:max_strengths] if max_strengths else strengths

    # Display each strength in a green-themed container
    for i, strength in enumerate(strengths_to_show):
        # Create a styled container for each strength
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 10px;
                    color: #155724;
                ">
                    <strong>✓ {strength}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_strengths_with_feedback(strengths: List[str], feedback: str = None):
    """
    Render strengths with additional overall feedback.

    Args:
        strengths: List of strength descriptions
        feedback: Additional feedback about the strengths
    """
    st.subheader("✅ Resume Strengths")

    if not strengths:
        st.info("No specific strengths identified in the resume.")
        return

    # Display each strength in a green-themed container
    for i, strength in enumerate(strengths):
        st.success(f"**{i+1}.** {strength}")

    # Add overall feedback if provided
    if feedback:
        st.markdown(f"**Overall Strengths Feedback:** {feedback}")


def render_strengths_summary(strengths: List[str], show_count: bool = True):
    """
    Render a compact summary of strengths.

    Args:
        strengths: List of strength descriptions
        show_count: Whether to show the count of strengths
    """
    if not strengths:
        st.info("No specific strengths identified in the resume.")
        return

    if show_count:
        st.write(f"**Number of Strengths Identified: {len(strengths)}**")

    # Create a horizontal layout for strengths
    cols = st.columns(min(3, len(strengths)))  # Max 3 columns

    for i, strength in enumerate(strengths):
        with cols[i % len(cols)]:
            st.markdown(
                f"""
                <div style="
                    background-color: #e8f5e8;
                    border-left: 4px solid #28a745;
                    padding: 8px;
                    margin-bottom: 8px;
                    border-radius: 3px;
                ">
                    <small>✓ {strength}</small>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_strengths_expandable(strengths: List[str], max_visible: int = 3):
    """
    Render strengths with expandable sections for longer lists.

    Args:
        strengths: List of strength descriptions
        max_visible: Maximum number of strengths to show initially
    """
    st.subheader("✅ Resume Strengths")

    if not strengths:
        st.info("No specific strengths identified in the resume.")
        return

    # Show the first few strengths directly
    for i in range(min(max_visible, len(strengths))):
        st.success(f"✓ {strengths[i]}")

    # If there are more strengths, put them in an expander
    if len(strengths) > max_visible:
        with st.expander(f"Show {len(strengths) - max_visible} more strengths"):
            for i in range(max_visible, len(strengths)):
                st.success(f"✓ {strengths[i]}")

    # Add a summary at the bottom
    st.caption(f"Total strengths identified: {len(strengths)}")


def get_strengths_insights(strengths: List[str]) -> dict:
    """
    Generate insights about the strengths.

    Args:
        strengths: List of strength descriptions

    Returns:
        Dictionary containing insights about the strengths
    """
    insights = {
        "count": len(strengths),
        "has_technical": any("technical" in s.lower() or "skill" in s.lower() for s in strengths),
        "has_experience": any("experience" in s.lower() or "work" in s.lower() for s in strengths),
        "has_achievements": any("achievement" in s.lower() or "accomplish" in s.lower() for s in strengths)
    }

    return insights