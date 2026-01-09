"""Keyword suggestions component for Resume Analyzer Core"""
import streamlit as st
from typing import List
from src.models.suggestions import KeywordSuggestion


def _get_color_for_relevance(relevance_score: float) -> tuple:
    """
    Get appropriate color and background color for a relevance score.

    Args:
        relevance_score: The relevance score (0-1)

    Returns:
        Tuple of (border_color, background_color)
    """
    if relevance_score >= 0.8:
        return "#28a745", "#d4edda"  # High relevance - green
    elif relevance_score >= 0.5:
        return "#ffc107", "#fff3cd"  # Medium relevance - yellow
    else:
        return "#dc3545", "#f8d7da"  # Low relevance - red


def render_keyword_suggestions(suggestions: List[KeywordSuggestion], show_header: bool = True):
    """
    Render keyword suggestions in card format.

    Args:
        suggestions: List of KeywordSuggestion entities to display
        show_header: Whether to show the section header
    """
    if show_header:
        st.subheader("🔑 Keyword Suggestions for Improvement")

    if not suggestions:
        st.info("No keyword suggestions available. Your resume may already be well-optimized!")
        return

    # Display each suggestion as a card
    for i, suggestion in enumerate(suggestions):
        _render_single_keyword_card(suggestion, i + 1)


def _render_single_keyword_card(suggestion: KeywordSuggestion, index: int):
    """
    Render a single keyword suggestion as a card using Streamlit's native components.

    Args:
        suggestion: The KeywordSuggestion to display
        index: The index of this suggestion for styling
    """
    # Determine color based on relevance score for styling
    border_color, bg_color = _get_color_for_relevance(suggestion.relevance_score)

    # Use Streamlit containers and columns for layout instead of raw HTML
    with st.container():
        # Create header with keyword and relevance score side by side
        header_col1, header_col2 = st.columns([4, 1])

        with header_col1:
            # Use markdown with color styling for the keyword
            st.markdown(f"<h4 style='color: {border_color}; margin-bottom: 0.5rem;'>{index}. {suggestion.keyword}</h4>", unsafe_allow_html=True)

        with header_col2:
            # Display relevance score in a colored badge
            st.markdown(
                f"<div style='text-align: center; background-color: {border_color}; color: white; padding: 0.25rem 0.5rem; border-radius: 12px; font-weight: bold; margin-left: auto; width: fit-content;'>"
                f"{suggestion.relevance_score:.2f}"
                f"</div>",
                unsafe_allow_html=True
            )

        # Display category with a badge-style appearance
        st.markdown(
            f"<div style='margin: 0.5rem 0; padding: 0.25rem 0;'>"
            f"<strong style='color: #495057;'>Category:</strong> "
            f"<span style='background-color: #e9ecef; padding: 0.125rem 0.375rem; border-radius: 0.25rem; margin-left: 0.5rem; font-size: 0.9em;'>"
            f"{suggestion.category}"
            f"</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Display role alignment
        st.markdown(
            f"<div style='margin: 0.5rem 0; padding: 0.25rem 0;'>"
            f"<strong style='color: #495057;'>Role Alignment:</strong> {suggestion.role_alignment}"
            f"</div>",
            unsafe_allow_html=True
        )

        # Display justification
        st.markdown(
            f"<div style='margin: 0.5rem 0; padding: 0.25rem 0;'>"
            f"<strong style='color: #495057;'>Justification:</strong> {suggestion.justification}"
            f"</div>",
            unsafe_allow_html=True
        )

        # Create an expander for implementation tips to keep the UI clean
        with st.expander("Implementation Tips"):
            tips = _get_implementation_tips_list(suggestion)
            for tip in tips:
                st.markdown(f"<span style='color: #28a745;'>•</span> {tip}", unsafe_allow_html=True)

        # Add a subtle divider at the bottom of the card
        st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)


def _get_implementation_tips_list(suggestion: KeywordSuggestion) -> List[str]:
    """
    Generate a list of implementation tips based on the keyword category.

    Args:
        suggestion: The KeywordSuggestion to get tips for

    Returns:
        List of implementation tips as strings
    """
    category = suggestion.category.lower()
    tips = []

    if "technical" in category or "programming" in category or "framework" in category:
        tips = [
            "Include this skill in your 'Technical Skills' section",
            "Mention specific projects where you've used this technology",
            "Highlight any certifications or training related to this skill"
        ]
    elif "tool" in category:
        tips = [
            "List this tool in your 'Technical Tools' or 'Software' section",
            "Describe how you've used this tool in your work experience",
            "Include specific examples of projects completed with this tool"
        ]
    elif "soft skill" in category.lower():
        tips = [
            "Demonstrate this skill through your work experience descriptions",
            "Include examples of how you've applied this skill in professional settings",
            "Use action verbs that reflect this soft skill in your bullet points"
        ]
    elif "industry" in category.lower():
        tips = [
            "Include industry-specific projects in your portfolio",
            "Mention relevant industry experience in your summary",
            "Use industry terminology in your resume to show familiarity"
        ]
    else:
        tips = [
            f"Consider adding '{suggestion.keyword}' to relevant sections of your resume",
            f"Think about how '{suggestion.keyword}' relates to your target role",
            "Look for opportunities to naturally incorporate this term in your experience descriptions"
        ]

    return tips




def render_keyword_suggestions_by_category(suggestions: List[KeywordSuggestion]):
    """
    Render keyword suggestions grouped by category.

    Args:
        suggestions: List of KeywordSuggestion entities to display
    """
    st.subheader("🔑 Keyword Suggestions by Category")

    if not suggestions:
        st.info("No keyword suggestions available.")
        return

    # Group suggestions by category
    categories = {}
    for suggestion in suggestions:
        category = suggestion.category
        if category not in categories:
            categories[category] = []
        categories[category].append(suggestion)

    # Create tabs for each category
    if len(categories) > 1:
        category_names = list(categories.keys())
        tabs = st.tabs(category_names)

        for i, (category, cat_suggestions) in enumerate(categories.items()):
            with tabs[i]:
                for j, suggestion in enumerate(cat_suggestions):
                    _render_single_keyword_card(suggestion, j + 1)
    else:
        # If only one category, just display all suggestions
        for i, suggestion in enumerate(suggestions):
            _render_single_keyword_card(suggestion, i + 1)


def render_keyword_suggestions_with_actionable_tips(suggestions: List[KeywordSuggestion]):
    """
    Render keyword suggestions with actionable tips for implementation.

    Args:
        suggestions: List of KeywordSuggestion entities to display
    """
    st.subheader("🔑 Keyword Suggestions with Implementation Tips")

    if not suggestions:
        st.info("No keyword suggestions available.")
        return

    for i, suggestion in enumerate(suggestions):
        with st.expander(f"{suggestion.keyword} (Relevance: {suggestion.relevance_score:.2f})"):
            st.write(f"**Category:** {suggestion.category}")
            st.write(f"**Role Alignment:** {suggestion.role_alignment}")
            st.write(f"**Justification:** {suggestion.justification}")

            # Add implementation tips based on category
            tips = _get_implementation_tips(suggestion)
            if tips:
                st.write("**Implementation Tips:**")
                for tip in tips:
                    st.write(f"- {tip}")


def _get_implementation_tips(suggestion: KeywordSuggestion) -> List[str]:
    """
    Get implementation tips based on the keyword category.

    Args:
        suggestion: The KeywordSuggestion to get tips for

    Returns:
        List of implementation tips
    """
    category = suggestion.category.lower()

    tips = []

    if "technical" in category or "programming" in category or "framework" in category:
        tips = [
            "Include this skill in your 'Technical Skills' section",
            "Mention specific projects where you've used this technology",
            "Highlight any certifications or training related to this skill"
        ]
    elif "tool" in category:
        tips = [
            "List this tool in your 'Technical Tools' or 'Software' section",
            "Describe how you've used this tool in your work experience",
            "Include specific examples of projects completed with this tool"
        ]
    elif "soft skill" in category:
        tips = [
            "Demonstrate this skill through your work experience descriptions",
            "Include examples of how you've applied this skill in professional settings",
            "Use action verbs that reflect this soft skill in your bullet points"
        ]
    elif "industry" in category:
        tips = [
            "Include industry-specific projects in your portfolio",
            "Mention relevant industry experience in your summary",
            "Use industry terminology in your resume to show familiarity"
        ]
    else:
        tips = [
            f"Consider adding '{suggestion.keyword}' to relevant sections of your resume",
            f"Think about how '{suggestion.keyword}' relates to your target role",
            "Look for opportunities to naturally incorporate this term in your experience descriptions"
        ]

    return tips


def render_top_keyword_suggestions(suggestions: List[KeywordSuggestion], top_n: int = 5):
    """
    Render only the top N keyword suggestions.

    Args:
        suggestions: List of KeywordSuggestion entities to display
        top_n: Number of top suggestions to display (default 5)
    """
    st.subheader(f"🔥 Top {top_n} Keyword Suggestions")

    if not suggestions:
        st.info("No keyword suggestions available.")
        return

    # Sort suggestions by relevance score (descending)
    sorted_suggestions = sorted(suggestions, key=lambda x: x.relevance_score, reverse=True)

    # Display only the top N suggestions
    top_suggestions = sorted_suggestions[:top_n]

    for i, suggestion in enumerate(top_suggestions):
        _render_single_keyword_card(suggestion, i + 1)

    # Show how many suggestions were not displayed
    if len(suggestions) > top_n:
        st.write(f"Showing {top_n} of {len(suggestions)} suggestions. Consider implementing these high-impact keywords first.")


def render_keyword_suggestions_summary(suggestions: List[KeywordSuggestion]):
    """
    Render a summary of keyword suggestions.

    Args:
        suggestions: List of KeywordSuggestion entities to summarize
    """
    st.subheader("📋 Keyword Suggestions Summary")

    if not suggestions:
        st.info("No keyword suggestions available.")
        return

    # Calculate statistics
    total_suggestions = len(suggestions)
    avg_relevance = sum(s.relevance_score for s in suggestions) / len(suggestions) if suggestions else 0

    # Count by category
    category_counts = {}
    for suggestion in suggestions:
        category = suggestion.category
        category_counts[category] = category_counts.get(category, 0) + 1

    # Display statistics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Suggestions", total_suggestions)
    with col2:
        st.metric("Average Relevance", f"{avg_relevance:.2f}")

    # Display category breakdown
    if category_counts:
        st.write("**Category Breakdown:**")
        for category, count in category_counts.items():
            st.write(f"- {category}: {count} suggestions")


def _get_color_for_relevance(relevance_score: float) -> tuple:
    """
    Get appropriate color and background color for a relevance score.

    Args:
        relevance_score: The relevance score (0-1)

    Returns:
        Tuple of (border_color, background_color)
    """
    if relevance_score >= 0.8:
        return "#28a745", "#d4edda"  # High relevance - green
    elif relevance_score >= 0.5:
        return "#ffc107", "#fff3cd"  # Medium relevance - yellow
    else:
        return "#dc3545", "#f8d7da"  # Low relevance - red