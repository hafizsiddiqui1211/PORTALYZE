"""Weaknesses panel component for Resume Analyzer Core"""
import streamlit as st
from typing import List


def render_weaknesses(weaknesses: List[str], show_header: bool = True, max_weaknesses: int = None):
    """
    Render a red-themed panel displaying resume weaknesses.

    Args:
        weaknesses: List of weakness descriptions
        show_header: Whether to show the section header
        max_weaknesses: Maximum number of weaknesses to display (None for all)
    """
    if show_header:
        st.subheader("⚠️ Areas for Improvement")

    if not weaknesses:
        st.success("No significant weaknesses identified in the resume.")
        return

    # Limit the number of weaknesses if specified
    weaknesses_to_show = weaknesses[:max_weaknesses] if max_weaknesses else weaknesses

    # Display each weakness in a red-themed container
    for i, weakness in enumerate(weaknesses_to_show):
        # Create a styled container for each weakness
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 10px;
                    color: #721c24;
                ">
                    <strong>⚠️ {weakness}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_weaknesses_with_priority(weaknesses: List[str], priorities: List[str] = None):
    """
    Render weaknesses with priority levels.

    Args:
        weaknesses: List of weakness descriptions
        priorities: List of priority levels (e.g., 'High', 'Medium', 'Low') corresponding to each weakness
    """
    st.subheader("⚠️ Areas for Improvement")

    if not weaknesses:
        st.success("No significant weaknesses identified in the resume.")
        return

    if priorities and len(priorities) != len(weaknesses):
        st.warning("Priorities list length doesn't match weaknesses list length. Ignoring priorities.")
        priorities = None

    # Display each weakness with priority if available
    for i, weakness in enumerate(weaknesses):
        priority = priorities[i] if priorities else "Medium"

        # Set color based on priority
        if priority.lower() == 'high':
            color = "#dc3545"  # Red
            priority_text = "🔴 High Priority"
        elif priority.lower() == 'low':
            color = "#fd7e14"  # Orange
            priority_text = "🟡 Low Priority"
        else:
            color = "#ffc107"  # Yellow
            priority_text = "🟡 Medium Priority"

        # Create a styled container for each weakness
        st.markdown(
            f"""
            <div style="
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
                border-left: 5px solid {color};
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div><strong>⚠️ {weakness}</strong></div>
                    <div style="color: {color}; font-weight: bold;">{priority_text}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_weaknesses_by_category(weaknesses: List[str], categories: List[str] = None):
    """
    Render weaknesses grouped by category.

    Args:
        weaknesses: List of weakness descriptions
        categories: List of categories corresponding to each weakness
    """
    st.subheader("⚠️ Categorized Areas for Improvement")

    if not weaknesses:
        st.success("No significant weaknesses identified in the resume.")
        return

    if not categories or len(categories) != len(weaknesses):
        # If no categories provided or mismatch, display all weaknesses together
        st.warning("Categories not provided or don't match weaknesses count. Displaying all together.")
        render_weaknesses(weaknesses)
        return

    # Group weaknesses by category
    category_dict = {}
    for weakness, category in zip(weaknesses, categories):
        if category not in category_dict:
            category_dict[category] = []
        category_dict[category].append(weakness)

    # Display each category in a separate expander
    for category, cat_weaknesses in category_dict.items():
        with st.expander(f"**{category.title()} Issues**"):
            for weakness in cat_weaknesses:
                st.warning(f"⚠️ {weakness}")


def render_weaknesses_expandable(weaknesses: List[str], max_visible: int = 3):
    """
    Render weaknesses with expandable sections for longer lists.

    Args:
        weaknesses: List of weakness descriptions
        max_visible: Maximum number of weaknesses to show initially
    """
    st.subheader("⚠️ Areas for Improvement")

    if not weaknesses:
        st.success("No significant weaknesses identified in the resume.")
        return

    # Show the first few weaknesses directly
    for i in range(min(max_visible, len(weaknesses))):
        st.warning(f"⚠️ {weaknesses[i]}")

    # If there are more weaknesses, put them in an expander
    if len(weaknesses) > max_visible:
        with st.expander(f"Show {len(weaknesses) - max_visible} more areas for improvement"):
            for i in range(max_visible, len(weaknesses)):
                st.warning(f"⚠️ {weaknesses[i]}")

    # Add a summary at the bottom
    st.caption(f"Total areas for improvement identified: {len(weaknesses)}")


def get_weaknesses_insights(weaknesses: List[str]) -> dict:
    """
    Generate insights about the weaknesses.

    Args:
        weaknesses: List of weakness descriptions

    Returns:
        Dictionary containing insights about the weaknesses
    """
    insights = {
        "count": len(weaknesses),
        "has_keyword_issues": any("keyword" in w.lower() or "skills" in w.lower() for w in weaknesses),
        "has_formatting_issues": any("format" in w.lower() or "layout" in w.lower() for w in weaknesses),
        "has_content_issues": any("content" in w.lower() or "section" in w.lower() for w in weaknesses)
    }

    return insights


def render_weaknesses_with_suggestions(weaknesses: List[str], suggestions: List[str] = None):
    """
    Render weaknesses with corresponding improvement suggestions.

    Args:
        weaknesses: List of weakness descriptions
        suggestions: List of suggestions corresponding to each weakness
    """
    st.subheader("⚠️ Areas for Improvement & Suggestions")

    if not weaknesses:
        st.success("No significant weaknesses identified in the resume.")
        return

    if suggestions and len(suggestions) != len(weaknesses):
        st.warning("Suggestions list length doesn't match weaknesses list length. Showing weaknesses only.")
        render_weaknesses(weaknesses)
        return

    # Display each weakness with its corresponding suggestion
    for i, weakness in enumerate(weaknesses):
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 15px;
                ">
                    <div style="color: #721c24; font-weight: bold;">⚠️ {weakness}</div>
                    <div style="margin-top: 8px;">
                        <span style="color: #155724; font-weight: bold;">💡 Suggestion:</span>
                        {suggestions[i] if suggestions else 'Work on this area to improve your resume'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )