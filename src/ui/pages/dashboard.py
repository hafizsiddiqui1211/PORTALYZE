"""Unified Dashboard for Resume Analyzer Core"""
import streamlit as st
from typing import Dict, List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import our modules
from src.models.analysis import AnalysisResult
from src.models.profile_analysis import ProfileAnalysis
from src.models.alignment_result import AlignmentResult
from src.ui.components.results_display import render_analysis_results, render_profile_comparison
from src.ui.components.export import render_export_options
from src.ui.components.navigation import render_main_navigation
from src.services.alignment_analyzer import AlignmentAnalyzer


class DashboardPage:
    """Main dashboard page showing unified view of all analysis results"""

    def __init__(self):
        self.alignment_analyzer = AlignmentAnalyzer()

    def render(self):
        """Render the unified dashboard"""
        st.title("📊 Unified Analysis Dashboard")
        st.markdown("""
        View comprehensive analysis results for your resume and profiles in one place.
        Compare scores, identify alignment gaps, and get actionable recommendations.
        """)

        # Initialize session state for dashboard
        self._initialize_session_state()

        # Check if we have any analysis results to display
        has_resume_analysis = st.session_state.get('ra_analysis_result') is not None
        has_profile_analyses = bool(st.session_state.get('pa_profile_analyses', {}))

        if not has_resume_analysis and not has_profile_analyses:
            self._render_empty_state()
            return

        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Overview",
            "📄 Resume Analysis",
            "🌐 Profile Analyses",
            "⚖️ Alignment",
            "📤 Export"
        ])

        with tab1:
            self._render_overview_tab(has_resume_analysis, has_profile_analyses)

        with tab2:
            self._render_resume_tab(has_resume_analysis)

        with tab3:
            self._render_profiles_tab(has_profile_analyses)

        with tab4:
            self._render_alignment_tab(has_resume_analysis, has_profile_analyses)

        with tab5:
            self._render_export_tab()

    def _initialize_session_state(self):
        """Initialize session state variables for the dashboard."""
        if 'dashboard_view' not in st.session_state:
            st.session_state.dashboard_view = "overview"
        if 'comparison_mode' not in st.session_state:
            st.session_state.comparison_mode = "scores"

    def _render_empty_state(self):
        """Render the empty state when no analyses are available."""
        st.info("""
        ## Welcome to the Resume & Profile Analyzer Dashboard

        To get started:
        1. Analyze your resume using the Resume Analyzer
        2. Analyze your profiles (LinkedIn, GitHub, Portfolio) using the Profile Analyzer
        3. Return here to see a unified view of all your analyses

        The dashboard will show:
        - Resume analysis results
        - Profile analysis results
        - Cross-platform alignment analysis
        - Export options for reports
        """)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Resume Analyzer"):
                st.session_state.active_page = "resume_analyzer"
                st.rerun()

        with col2:
            if st.button("Go to Profile Analyzer"):
                st.session_state.active_page = "profile_analyzer"
                st.rerun()

    def _render_overview_tab(self, has_resume_analysis: bool, has_profile_analyses: bool):
        """Render the overview tab with summary metrics."""
        st.header("📊 Analysis Overview")

        # Summary metrics
        cols = st.columns(4)

        with cols[0]:
            if has_resume_analysis:
                resume_score = st.session_state.ra_analysis_result.ats_score
                st.metric(
                    label="Resume ATS Score",
                    value=f"{resume_score:.1f}",
                    delta="Resume analyzed" if resume_score > 0 else "No resume analysis"
                )
            else:
                st.metric(
                    label="Resume ATS Score",
                    value="-",
                    delta="No resume analysis"
                )

        with cols[1]:
            if has_profile_analyses and st.session_state.pa_profile_analyses:
                avg_profile_score = sum(
                    analysis.overall_score for analysis in st.session_state.pa_profile_analyses.values()
                ) / len(st.session_state.pa_profile_analyses)
                st.metric(
                    label="Avg. Profile Score",
                    value=f"{avg_profile_score:.1f}",
                    delta=f"{len(st.session_state.pa_profile_analyses)} profiles analyzed"
                )
            else:
                st.metric(
                    label="Avg. Profile Score",
                    value="-",
                    delta="No profile analyses"
                )

        with cols[2]:
            if has_resume_analysis:
                resume_strengths = len(st.session_state.ra_analysis_result.strengths) if st.session_state.ra_analysis_result else 0
                st.metric(
                    label="Resume Strengths",
                    value=resume_strengths,
                    delta="Resume elements"
                )
            else:
                st.metric(
                    label="Resume Strengths",
                    value="-",
                    delta="No resume data"
                )

        with cols[3]:
            if has_profile_analyses:
                total_suggestions = sum(
                    len(analysis.suggestions) for analysis in st.session_state.pa_profile_analyses.values()
                ) if st.session_state.pa_profile_analyses else 0
                st.metric(
                    label="Total Suggestions",
                    value=total_suggestions,
                    delta="Across all profiles"
                )
            else:
                st.metric(
                    label="Total Suggestions",
                    value="-",
                    delta="No profile data"
                )

        # Charts section
        if has_resume_analysis or has_profile_analyses:
            st.subheader("📈 Score Comparison")

            # Prepare data for visualization
            chart_data = []

            if has_resume_analysis:
                chart_data.append({
                    'Type': 'Resume',
                    'Score': st.session_state.ra_analysis_result.ats_score,
                    'Category': 'ATS Score'
                })

            if has_profile_analyses:
                for platform, analysis in st.session_state.pa_profile_analyses.items():
                    chart_data.append({
                        'Type': f'{platform.title()}',
                        'Score': analysis.overall_score,
                        'Category': 'Profile Score'
                    })

            if chart_data:
                df = pd.DataFrame(chart_data)

                fig = px.bar(
                    df,
                    x='Type',
                    y='Score',
                    color='Category',
                    title="Comparison of Resume and Profile Scores",
                    range_y=[0, 100]
                )

                st.plotly_chart(fig, use_container_width=True)

    def _render_resume_tab(self, has_resume_analysis: bool):
        """Render the resume analysis tab."""
        st.header("📄 Resume Analysis Results")

        if not has_resume_analysis or not st.session_state.get('ra_analysis_result'):
            st.info("No resume analysis available. Please analyze your resume first.")
            if st.button("Go to Resume Analyzer"):
                st.session_state.active_page = "resume_analyzer"
                st.rerun()
            return

        # Display resume analysis results
        resume_analysis = st.session_state.ra_analysis_result
        st.subheader(f"Resume Analysis: {resume_analysis.ats_score}/100 ATS Score")

        # Resume-specific metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ATS Compatibility", f"{resume_analysis.ats_score:.1f}/100")
        with col2:
            st.metric("Strengths Identified", len(resume_analysis.strengths))
        with col3:
            st.metric("Improvement Areas", len(resume_analysis.weaknesses))

        # Show resume strengths and weaknesses
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Resume Strengths")
            for strength in resume_analysis.strengths:
                st.success(f"• {strength}")

        with col2:
            st.subheader("⚠️ Resume Weaknesses")
            for weakness in resume_analysis.weaknesses:
                st.warning(f"• {weakness}")

        # Show section feedback
        if resume_analysis.section_feedback:
            st.subheader("📋 Section Feedback")
            for section, feedback in resume_analysis.section_feedback.items():
                with st.expander(f"{section.title()} Section"):
                    st.write(feedback)

        # Show overall feedback
        if resume_analysis.overall_feedback:
            st.subheader("📝 Overall Feedback")
            st.info(resume_analysis.overall_feedback)

    def _render_profiles_tab(self, has_profile_analyses: bool):
        """Render the profiles analysis tab."""
        st.header("🌐 Profile Analysis Results")

        if not has_profile_analyses or not st.session_state.get('pa_profile_analyses'):
            st.info("No profile analyses available. Please analyze your profiles first.")
            if st.button("Go to Profile Analyzer"):
                st.session_state.active_page = "profile_analyzer"
                st.rerun()
            return

        # Show individual profile analyses
        profile_analyses = st.session_state.pa_profile_analyses

        # Create tabs for each profile
        profile_tabs = st.tabs([platform.title() for platform in profile_analyses.keys()])

        for i, (platform, analysis) in enumerate(profile_analyses.items()):
            with profile_tabs[i]:
                # Get the corresponding profile URL if available
                profile_url = None
                if st.session_state.get('pa_profile_urls'):
                    profile_url = st.session_state.pa_profile_urls.get(platform)

                # Render analysis results for this profile
                render_analysis_results(analysis, profile_url)

        # Show comparison if multiple profiles analyzed
        if len(profile_analyses) > 1:
            st.subheader("⚖️ Profile Comparison")
            analyses_list = list(profile_analyses.values())
            render_profile_comparison(analyses_list)

    def _render_alignment_tab(self, has_resume_analysis: bool, has_profile_analyses: bool):
        """Render the alignment analysis tab."""
        st.header("⚖️ Resume-Profile Alignment")

        if not has_resume_analysis or not has_profile_analyses:
            st.info("Both resume and profile analyses are needed for alignment analysis.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Analyze Resume"):
                    st.session_state.active_page = "resume_analyzer"
                    st.rerun()
            with col2:
                if st.button("Analyze Profiles"):
                    st.session_state.active_page = "profile_analyzer"
                    st.rerun()
            return

        # Perform alignment analysis
        resume_analysis = st.session_state.ra_analysis_result
        profile_analyses = st.session_state.pa_profile_analyses

        with st.spinner("Analyzing alignment between resume and profiles..."):
            try:
                alignment_result = self.alignment_analyzer.analyze_alignment(
                    resume_analysis=resume_analysis,
                    profile_analyses=profile_analyses
                )

                # Display alignment results
                st.subheader(f"Overall Alignment Score: {alignment_result.overall_score:.1f}/100")

                # Alignment metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Skill Alignment", f"{alignment_result.skill_alignment:.1f}/100")
                with col2:
                    st.metric("Experience Alignment", f"{alignment_result.experience_alignment:.1f}/100")
                with col3:
                    st.metric("Project Alignment", f"{alignment_result.project_alignment:.1f}/100")

                # Show discrepancies
                if alignment_result.discrepancies:
                    st.subheader("🔍 Identified Discrepancies")
                    for discrepancy in alignment_result.discrepancies:
                        st.error(f"• {discrepancy}")

                # Show recommendations
                if alignment_result.recommendations:
                    st.subheader("💡 Alignment Recommendations")
                    for recommendation in alignment_result.recommendations:
                        st.info(f"• {recommendation}")

                # Visualization of alignment by category
                st.subheader("📈 Alignment Visualization")

                alignment_data = {
                    'Category': ['Skills', 'Experience', 'Projects'],
                    'Alignment Score': [
                        alignment_result.skill_alignment,
                        alignment_result.experience_alignment,
                        alignment_result.project_alignment
                    ]
                }

                df = pd.DataFrame(alignment_data)

                fig = px.bar(
                    df,
                    x='Category',
                    y='Alignment Score',
                    title="Alignment Scores by Category",
                    range_y=[0, 100],
                    color='Category',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )

                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error performing alignment analysis: {str(e)}")
                st.info("Please ensure both resume and profile analyses are complete.")

    def _render_export_tab(self):
        """Render the export options tab."""
        st.header("📤 Export Analysis Results")

        has_resume_analysis = st.session_state.get('ra_analysis_result') is not None
        has_profile_analyses = bool(st.session_state.get('pa_profile_analyses', {}))

        if not has_resume_analysis and not has_profile_analyses:
            st.info("No analysis results available to export.")
            return

        # Prepare data for export
        resume_analysis = st.session_state.get('ra_analysis_result')
        profile_analyses = st.session_state.get('pa_profile_analyses', {})
        profile_urls = st.session_state.get('pa_profile_urls', {})

        # Show export options
        render_export_options(
            resume_analysis=resume_analysis,
            profile_analyses=profile_analyses,
            profile_urls=profile_urls
        )

        # Additional export options specific to dashboard
        st.subheader("Dashboard-Specific Exports")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Export Dashboard Summary"):
                # Create a summary of all analyses
                summary_data = {
                    "generated_at": datetime.now().isoformat(),
                    "resume_analysis": resume_analysis.to_dict() if resume_analysis else None,
                    "profile_analyses": {
                        platform: analysis.to_dict()
                        for platform, analysis in profile_analyses.items()
                    } if profile_analyses else {},
                    "has_resume_analysis": has_resume_analysis,
                    "has_profile_analyses": has_profile_analyses,
                    "profile_count": len(profile_analyses) if profile_analyses else 0
                }

                json_str = json.dumps(summary_data, indent=2)
                st.download_button(
                    label="Download Summary JSON",
                    data=json_str,
                    file_name=f"dashboard_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

        with col2:
            if st.button("Export Comparison Report"):
                # Create a comparison report
                comparison_data = self._generate_comparison_report()

                if comparison_data:
                    csv_str = self._generate_comparison_csv(comparison_data)
                    st.download_button(
                        label="Download Comparison CSV",
                        data=csv_str,
                        file_name=f"profile_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )

    def _generate_comparison_report(self) -> Optional[Dict]:
        """Generate comparison data for export."""
        has_resume_analysis = st.session_state.get('ra_analysis_result') is not None
        has_profile_analyses = bool(st.session_state.get('pa_profile_analyses', {}))

        if not has_resume_analysis and not has_profile_analyses:
            return None

        comparison_data = {
            "summary": {
                "resume_ats_score": st.session_state.ra_analysis_result.ats_score if has_resume_analysis else 0,
                "average_profile_score": 0,
                "profile_count": 0,
                "resume_strengths_count": len(st.session_state.ra_analysis_result.strengths) if has_resume_analysis else 0,
                "total_suggestions_count": 0
            },
            "detailed": []
        }

        if has_profile_analyses:
            avg_score = sum(
                analysis.overall_score for analysis in st.session_state.pa_profile_analyses.values()
            ) / len(st.session_state.pa_profile_analyses)
            comparison_data["summary"]["average_profile_score"] = avg_score
            comparison_data["summary"]["profile_count"] = len(st.session_state.pa_profile_analyses)

            total_suggestions = sum(
                len(analysis.suggestions) for analysis in st.session_state.pa_profile_analyses.values()
            )
            comparison_data["summary"]["total_suggestions_count"] = total_suggestions

            # Add detailed profile data
            for platform, analysis in st.session_state.pa_profile_analyses.items():
                profile_detail = {
                    "platform": platform,
                    "overall_score": analysis.overall_score,
                    "clarity_score": analysis.clarity_score,
                    "impact_score": analysis.impact_score,
                    "strengths_count": len(analysis.strengths),
                    "weaknesses_count": len(analysis.weaknesses),
                    "suggestions_count": len(analysis.suggestions)
                }
                comparison_data["detailed"].append(profile_detail)

        return comparison_data

    def _generate_comparison_csv(self, comparison_data: Dict) -> str:
        """Generate CSV string from comparison data."""
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)

        # Write header
        header = [
            "Metric", "Resume",
            *[f"{item['platform'].title()} (Profile)" for item in comparison_data.get("detailed", [])]
        ]
        writer.writerow(header)

        # Write data rows
        # Scores row
        scores_row = ["Overall Score"]
        scores_row.append(str(comparison_data["summary"]["resume_ats_score"]))
        scores_row.extend([str(item["overall_score"]) for item in comparison_data.get("detailed", [])])
        writer.writerow(scores_row)

        # Clarity scores row (for profiles only)
        clarity_row = ["Clarity Score"]
        clarity_row.append("")  # Resume doesn't have clarity score in same way
        clarity_row.extend([str(item["clarity_score"]) for item in comparison_data.get("detailed", [])])
        writer.writerow(clarity_row)

        # Impact scores row (for profiles only)
        impact_row = ["Impact Score"]
        impact_row.append("")  # Resume doesn't have impact score in same way
        impact_row.extend([str(item["impact_score"]) for item in comparison_data.get("detailed", [])])
        writer.writerow(impact_row)

        # Counts row
        counts_row = ["Strengths Count"]
        counts_row.append(str(comparison_data["summary"]["resume_strengths_count"]))
        counts_row.extend([str(item["strengths_count"]) for item in comparison_data.get("detailed", [])])
        writer.writerow(counts_row)

        return output.getvalue()


def render_dashboard_page():
    """Render the main dashboard page."""
    dashboard = DashboardPage()
    dashboard.render()


def _calculate_overall_health_score(
    resume_analysis: Optional[AnalysisResult],
    profile_analyses: Optional[Dict[str, ProfileAnalysis]]
) -> float:
    """
    Calculate an overall health score based on resume and profile analyses.

    Args:
        resume_analysis: Resume analysis result
        profile_analyses: Dictionary of profile analyses

    Returns:
        Overall health score (0-100)
    """
    scores = []

    # Add resume score if available
    if resume_analysis:
        scores.append(resume_analysis.ats_score)

    # Add profile scores if available
    if profile_analyses:
        for analysis in profile_analyses.values():
            scores.append(analysis.overall_score)

    # Return average if we have scores, otherwise 0
    return sum(scores) / len(scores) if scores else 0.0


def _get_health_level(score: float) -> str:
    """
    Get the health level based on the score.

    Args:
        score: Health score (0-100)

    Returns:
        Health level as a string
    """
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    else:
        return "Needs Improvement"


def _get_top_recommendations(
    resume_analysis: Optional[AnalysisResult],
    profile_analyses: Optional[Dict[str, ProfileAnalysis]]
) -> List[str]:
    """
    Get the top recommendations across all analyses.

    Args:
        resume_analysis: Resume analysis result
        profile_analyses: Dictionary of profile analyses

    Returns:
        List of top recommendations
    """
    recommendations = []

    # Add resume recommendations if available
    if resume_analysis and hasattr(resume_analysis, 'weaknesses'):
        for weakness in resume_analysis.weaknesses[:2]:  # Top 2 resume issues
            recommendations.append(f"Resume: {weakness}")

    # Add profile recommendations if available
    if profile_analyses:
        for platform, analysis in profile_analyses.items():
            if hasattr(analysis, 'suggestions'):
                # Get high-priority suggestions
                high_priority_suggestions = [
                    suggestion for suggestion in analysis.suggestions
                    if getattr(suggestion, 'priority', '').upper() == 'HIGH'
                ]
                for suggestion in high_priority_suggestions[:2]:  # Top 2 per platform
                    if hasattr(suggestion, 'description'):
                        recommendations.append(f"{platform.title()}: {suggestion.description}")
                    elif isinstance(suggestion, dict):
                        recommendations.append(f"{platform.title()}: {suggestion.get('description', 'General improvement needed')}")

    return recommendations[:5]  # Return top 5 recommendations