"""Analysis Comparison Component for Resume Analyzer Core"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List
from src.models.profile_analysis import ProfileAnalysis


def render_profile_comparison(analyses: List[ProfileAnalysis]):
    """
    Render a side-by-side comparison of multiple profile analyses.

    Args:
        analyses: List of ProfileAnalysis entities to compare
    """
    if not analyses or len(analyses) < 2:
        st.info("Add more profile analyses to enable comparison view.")
        return

    st.header("⚖️ Profile Analysis Comparison")

    # Create a summary table
    comparison_data = []
    for analysis in analyses:
        comparison_data.append({
            'Platform': analysis.profile_type,
            'Overall Score': round(analysis.overall_score, 1),
            'Clarity Score': round(analysis.clarity_score, 1),
            'Impact Score': round(analysis.impact_score, 1),
            'Strengths Count': len(analysis.strengths),
            'Weaknesses Count': len(analysis.weaknesses),
            'Suggestions Count': len(analysis.suggestions)
        })

    df = pd.DataFrame(comparison_data)

    # Display comparison table
    st.subheader("📊 Score Comparison Table")
    st.dataframe(df, use_container_width=True)

    # Create visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Radar chart for scores comparison
        radar_df = df[['Platform', 'Overall Score', 'Clarity Score', 'Impact Score']].copy()
        radar_df.set_index('Platform', inplace=True)

        # Create radar chart using Plotly
        fig = go.Figure()

        for idx, row in radar_df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=row.values,
                theta=radar_df.columns,
                fill='toself',
                name=idx
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Profile Scores Comparison",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bar chart for strengths/weaknesses comparison
        comparison_df = df[['Platform', 'Strengths Count', 'Weaknesses Count', 'Suggestions Count']].copy()

        # Melt the dataframe for plotting
        melted_df = comparison_df.melt(id_vars=['Platform'],
                                       value_vars=['Strengths Count', 'Weaknesses Count', 'Suggestions Count'],
                                       var_name='Aspect',
                                       value_name='Count')

        fig_bar = px.bar(melted_df,
                         x='Platform',
                         y='Count',
                         color='Aspect',
                         title="Profile Elements Comparison",
                         barmode='group',
                         height=400)

        st.plotly_chart(fig_bar, use_container_width=True)

    # Detailed comparison section
    st.subheader("🔍 Detailed Comparison")

    # Create tabs for each comparison aspect
    tab1, tab2, tab3, tab4 = st.tabs(["Scores", "Strengths", "Weaknesses", "Suggestions"])

    with tab1:
        _render_scores_comparison(analyses)

    with tab2:
        _render_strengths_comparison(analyses)

    with tab3:
        _render_weaknesses_comparison(analyses)

    with tab4:
        _render_suggestions_comparison(analyses)


def _render_scores_comparison(analyses: List[ProfileAnalysis]):
    """Render score comparison visualization."""
    score_comparison = []
    for analysis in analyses:
        score_comparison.append({
            'Platform': analysis.profile_type,
            'Overall': analysis.overall_score,
            'Clarity': analysis.clarity_score,
            'Impact': analysis.impact_score
        })

    df = pd.DataFrame(score_comparison)

    # Create a grouped bar chart
    fig = go.Figure(data=[
        go.Bar(name='Overall Score', x=df['Platform'], y=df['Overall']),
        go.Bar(name='Clarity Score', x=df['Platform'], y=df['Clarity']),
        go.Bar(name='Impact Score', x=df['Platform'], y=df['Impact'])
    ])

    fig.update_layout(
        title="Score Comparison by Category",
        xaxis_title="Platform",
        yaxis_title="Score (0-100)",
        barmode='group',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def _render_strengths_comparison(analyses: List[ProfileAnalysis]):
    """Render strengths comparison."""
    col1, col2 = st.columns(2)

    for i, analysis in enumerate(analyses):
        with col1 if i % 2 == 0 else col2:
            with st.container():
                st.subheader(f"{analysis.profile_type} Strengths")

                if analysis.strengths:
                    for strength in analysis.strengths:
                        st.success(f"✅ {strength}")
                else:
                    st.info("No strengths identified")

                st.markdown(f"**Total Strengths: {len(analysis.strengths)}**")


def _render_weaknesses_comparison(analyses: List[ProfileAnalysis]):
    """Render weaknesses comparison."""
    col1, col2 = st.columns(2)

    for i, analysis in enumerate(analyses):
        with col1 if i % 2 == 0 else col2:
            with st.container():
                st.subheader(f"{analysis.profile_type} Weaknesses")

                if analysis.weaknesses:
                    for weakness in analysis.weaknesses:
                        st.warning(f"⚠️ {weakness}")
                else:
                    st.info("No weaknesses identified")

                st.markdown(f"**Total Weaknesses: {len(analysis.weaknesses)}**")


def _render_suggestions_comparison(analyses: List[ProfileAnalysis]):
    """Render suggestions comparison."""
    # Group suggestions by category across all platforms
    all_suggestions_by_category = {}
    platform_colors = px.colors.qualitative.Set3

    for i, analysis in enumerate(analyses):
        for suggestion in analysis.suggestions:
            category = getattr(suggestion, 'category', 'General')
            if category not in all_suggestions_by_category:
                all_suggestions_by_category[category] = []

            all_suggestions_by_category[category].append({
                'platform': analysis.profile_type,
                'suggestion': getattr(suggestion, 'suggestion_text', str(suggestion)),
                'priority': getattr(suggestion, 'priority', 'MEDIUM')
            })

    # Display suggestions by category
    for category, suggestions in all_suggestions_by_category.items():
        with st.expander(f"Category: {category}", expanded=True):
            for suggestion_data in suggestions:
                priority = suggestion_data['priority']
                if priority.upper() == 'HIGH':
                    emoji = "🔴"
                    color = "rgba(220, 53, 69, 0.1)"  # Light red
                elif priority.upper() == 'LOW':
                    emoji = "🟡"
                    color = "rgba(255, 193, 7, 0.1)"  # Light yellow
                else:  # MEDIUM
                    emoji = "🟡"
                    color = "rgba(253, 126, 20, 0.1)"  # Light orange

                st.markdown(
                    f"""
                    <div style="
                        background-color: {color};
                        border-left: 4px solid {'#dc3545' if priority.upper() == 'HIGH' else '#fd7e14' if priority.upper() == 'MEDIUM' else '#ffc107'};
                        padding: 8px;
                        margin: 5px 0;
                        border-radius: 0 4px 4px 0;
                    ">
                        <strong>{emoji} [{suggestion_data['platform']}]</strong> {suggestion_data['suggestion']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def render_resume_profile_alignment_comparison(
    resume_analysis: dict,  # This would be from Phase 1
    profile_analyses: List[ProfileAnalysis]
):
    """
    Render comparison between resume analysis and profile analyses.

    Args:
        resume_analysis: Resume analysis result from Phase 1
        profile_analyses: List of profile analysis results from Phase 2
    """
    if not resume_analysis or not profile_analyses:
        st.info("Provide both resume analysis and profile analyses for alignment comparison.")
        return

    st.header("🔗 Resume-Profile Alignment Analysis")

    # Create alignment comparison table
    alignment_data = []

    for profile_analysis in profile_analyses:
        # This is a simplified alignment score calculation
        # In a real implementation, this would come from an alignment analysis service
        resume_strengths = resume_analysis.get('strengths', [])
        profile_strengths = profile_analysis.strengths

        # Calculate overlap in strengths
        strength_overlap = len(set(resume_strengths) & set(profile_strengths))
        total_unique_strengths = len(set(resume_strengths) | set(profile_strengths))
        alignment_score = (strength_overlap / total_unique_strengths * 100) if total_unique_strengths > 0 else 0

        alignment_data.append({
            'Profile Platform': profile_analysis.profile_type,
            'Resume Strengths': len(resume_strengths),
            'Profile Strengths': len(profile_analysis.strengths),
            'Aligned Strengths': strength_overlap,
            'Alignment Score': round(alignment_score, 1)
        })

    alignment_df = pd.DataFrame(alignment_data)

    # Display alignment table
    st.subheader("Alignment Scores")
    st.dataframe(alignment_df, use_container_width=True)

    # Create visualization
    fig = px.bar(
        alignment_df,
        x='Profile Platform',
        y='Alignment Score',
        title="Resume-Profile Alignment Scores",
        range_y=[0, 100],
        color='Profile Platform',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show alignment insights
    st.subheader("Alignment Insights")

    for _, row in alignment_df.iterrows():
        if row['Alignment Score'] >= 70:
            st.success(f"✅ {row['Profile Platform']} profile is well-aligned with your resume")
        elif row['Alignment Score'] >= 40:
            st.info(f"⚠️ {row['Profile Platform']} profile has moderate alignment with your resume")
        else:
            st.warning(f"❌ {row['Profile Platform']} profile has low alignment with your resume")


def render_profile_health_metrics(analyses: List[ProfileAnalysis]):
    """
    Render health metrics comparing profile performance.

    Args:
        analyses: List of ProfileAnalysis entities
    """
    if not analyses:
        return

    st.subheader("🏥 Profile Health Metrics")

    # Prepare data for metrics comparison
    health_metrics = []
    for analysis in analyses:
        health_metrics.append({
            'Platform': analysis.profile_type,
            'Overall Score': analysis.overall_score,
            'Clarity': analysis.clarity_score,
            'Impact': analysis.impact_score,
            'Strengths': len(analysis.strengths),
            'Weaknesses': len(analysis.weaknesses),
            'Suggestions': len(analysis.suggestions),
            'Health Index': (analysis.overall_score + analysis.clarity_score + analysis.impact_score) / 3
        })

    health_df = pd.DataFrame(health_metrics)

    # Create metrics grid
    cols = st.columns(len(analyses))

    for i, analysis in enumerate(analyses):
        with cols[i]:
            st.metric(
                label=f"{analysis.profile_type} Health",
                value=f"{analysis.overall_score:.1f}",
                delta=f"Clarity: {analysis.clarity_score:.1f}, Impact: {analysis.impact_score:.1f}"
            )

    # Create detailed comparison chart
    fig = go.Figure()

    for _, row in health_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['Overall Score'], row['Clarity'], row['Impact'], row['Health Index']],
            theta=['Overall Score', 'Clarity', 'Impact', 'Health Index'],
            fill='toself',
            name=row['Platform']
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Profile Health Comparison",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def get_profile_comparison_summary(analyses: List[ProfileAnalysis]) -> dict:
    """
    Generate a summary of profile comparisons.

    Args:
        analyses: List of ProfileAnalysis entities

    Returns:
        Dictionary with comparison summary
    """
    if not analyses:
        return {}

    summary = {
        "total_profiles": len(analyses),
        "average_overall_score": sum(a.overall_score for a in analyses) / len(analyses),
        "average_clarity_score": sum(a.clarity_score for a in analyses) / len(analyses),
        "average_impact_score": sum(a.impact_score for a in analyses) / len(analyses),
        "strongest_profile": max(analyses, key=lambda x: x.overall_score).profile_type if analyses else None,
        "weakest_profile": min(analyses, key=lambda x: x.overall_score).profile_type if analyses else None,
        "total_strengths": sum(len(a.strengths) for a in analyses),
        "total_weaknesses": sum(len(a.weaknesses) for a in analyses),
        "total_suggestions": sum(len(a.suggestions) for a in analyses)
    }

    return summary