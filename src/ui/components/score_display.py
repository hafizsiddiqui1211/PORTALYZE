"""ATS Score display component for Resume Analyzer Core"""
import streamlit as st
from typing import Tuple


def render_ats_score(ats_score: float, show_details: bool = True):
    """
    Render a prominent ATS score display with color coding.

    Args:
        ats_score: The ATS compatibility score (0-100)
        show_details: Whether to show detailed explanation
    """
    # Determine color and label based on score
    if ats_score >= 80:
        score_color = "green"
        score_label = "Excellent"
        score_icon = "🚀"
        description = "High ATS compatibility - Recruiters will easily find your resume!"
    elif ats_score >= 60:
        score_color = "orange"
        score_label = "Good"
        score_icon = "👍"
        description = "Moderate ATS compatibility - Good chances of being found."
    elif ats_score >= 40:
        score_color = "yellow"
        score_label = "Fair"
        score_icon = "⚠️"
        description = "Low ATS compatibility - Consider improvements for better visibility."
    else:
        score_color = "red"
        score_label = "Needs Improvement"
        score_icon = "❌"
        description = "Low ATS compatibility - Significant improvements needed."

    # Create the main score display
    st.subheader(f"{score_icon} ATS Compatibility Score")

    # Use columns to make it more prominent
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        pass  # Empty column for spacing
    with col2:
        # Display the score in a large, prominent format
        st.markdown(
            f"""
            <div style="
                text-align: center;
                padding: 20px;
                border-radius: 10px;
                background-color: #f0f2f6;
                border: 2px solid #{'00FF00' if ats_score >= 80 else 'FFA500' if ats_score >= 60 else 'FFFF00' if ats_score >= 40 else 'FF0000'};
                font-size: 36px;
                font-weight: bold;
                color: #{score_color};
            ">
                {ats_score:.1f}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Score label below the number
        st.markdown(
            f"""
            <div style="
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                color: #{score_color};
            ">
                {score_label}
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        pass  # Empty column for spacing

    # Show detailed explanation if requested
    if show_details:
        st.info(f"**{description}**")

        # Add a progress bar visualization
        st.progress(int(ats_score) / 100)

        # Show score ranges explanation
        with st.expander("What does this score mean?"):
            st.write("""
            - **90-100**: Excellent ATS compatibility. Your resume is optimized for ATS systems.
            - **70-89**: Good ATS compatibility. Minor improvements could help.
            - **50-69**: Fair ATS compatibility. Consider adding more relevant keywords.
            - **0-49**: Poor ATS compatibility. Significant improvements needed for ATS visibility.
            """)


def render_score_comparison(current_score: float, target_score: float = 80.0):
    """
    Render a comparison between current score and target score.

    Args:
        current_score: The current ATS score
        target_score: The target ATS score to achieve (default 80.0)
    """
    st.subheader("🎯 Score Comparison")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Current Score",
            value=f"{current_score:.1f}/100",
            delta=f"{current_score - target_score:+.1f}" if current_score != target_score else "On target"
        )

    with col2:
        st.metric(
            label="Target Score",
            value=f"{target_score:.1f}/100",
            delta="Goal"
        )

    with col3:
        improvement_needed = max(0, target_score - current_score)
        st.metric(
            label="Improvement Needed",
            value=f"{improvement_needed:.1f} pts",
            delta="To reach target" if improvement_needed > 0 else "Target achieved!"
        )

    # Visual comparison bar
    st.write("**Visual Comparison:**")
    progress_text = f"Progress toward target: {min(100, max(0, current_score))}% of {target_score}%"
    st.write(progress_text)

    # Create a combined progress visualization
    st.markdown(
        f"""
        <div style="width: 100%; height: 30px; background: linear-gradient(to right,
            {'green' if current_score >= target_score else 'lightgray'} 0%,
            {'green' if current_score >= target_score else 'lightgray'} {min(100, current_score):.1f}%,
            lightgray {min(100, current_score):.1f}%, lightgray 100%);
            border: 1px solid #ccc; border-radius: 5px; position: relative;">
            <div style="position: absolute; left: {min(100, current_score)-2:.1f}%; top: -10px;
                color: black; font-weight: bold;">✓ Current: {current_score:.1f}</div>
            <div style="position: absolute; left: {target_score-2:.1f}%; top: 20px;
                color: blue; font-weight: bold;">→ Target: {target_score:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_score_color(ats_score: float) -> Tuple[str, str]:
    """
    Get the appropriate color and label for a given ATS score.

    Args:
        ats_score: The ATS compatibility score (0-100)

    Returns:
        Tuple of (color_name, score_label)
    """
    if ats_score >= 80:
        return "green", "Excellent"
    elif ats_score >= 60:
        return "orange", "Good"
    elif ats_score >= 40:
        return "yellow", "Fair"
    else:
        return "red", "Needs Improvement"