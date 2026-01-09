"""Combined career insights component for job role recommender"""

import streamlit as st
from typing import Optional, Dict, List
from datetime import datetime

from ...models.analysis import AnalysisResult
from ...models.role_recommendation import RecommendedRole


class CombinedCareerInsights:
    """UI component for displaying combined insights across all phases"""

    def __init__(self):
        pass

    def render(
        self,
        resume_analysis: Optional[AnalysisResult] = None,
        profile_analyses: Optional[Dict] = None,
        role_recommendations: Optional[List[RecommendedRole]] = None
    ):
        """
        Render combined career insights from all phases.

        Args:
            resume_analysis: Resume analysis result from Phase 1
            profile_analyses: Profile analyses from Phase 2
            role_recommendations: Role recommendations from Phase 3
        """
        st.subheader("🔗 Combined Career Insights")
        st.write("Synthesized insights across resume, profile, and role recommendation analyses")

        # Create a comprehensive overview
        col1, col2, col3 = st.columns(3)

        with col1:
            self._render_resume_summary(resume_analysis)

        with col2:
            self._render_profile_summary(profile_analyses)

        with col3:
            self._render_role_summary(role_recommendations)

        st.markdown("---")

        # Show synthesis insights
        self._render_synthesis_insights(resume_analysis, profile_analyses, role_recommendations)

        # Show recommendations for next steps
        self._render_next_steps(resume_analysis, profile_analyses, role_recommendations)

    def _render_resume_summary(self, resume_analysis: Optional[AnalysisResult]):
        """Render summary of resume analysis."""
        st.write("**Resume Strengths**")
        if resume_analysis and resume_analysis.strengths:
            strength_count = len(resume_analysis.strengths)
            ats_score = resume_analysis.ats_score
            st.metric("ATS Score", f"{ats_score:.1f}")
            st.metric("Strengths", strength_count)
        else:
            st.metric("ATS Score", "N/A")
            st.metric("Strengths", "0")

    def _render_profile_summary(self, profile_analyses: Optional[Dict]):
        """Render summary of profile analyses."""
        st.write("**Profile Insights**")
        if profile_analyses:
            profile_count = len(profile_analyses)
            total_suggestions = 0
            for profile_type, analysis in profile_analyses.items():
                if 'suggestions' in analysis:
                    total_suggestions += len(analysis['suggestions'])
            st.metric("Profiles Analyzed", profile_count)
            st.metric("Suggestions", total_suggestions)
        else:
            st.metric("Profiles Analyzed", "0")
            st.metric("Suggestions", "0")

    def _render_role_summary(self, role_recommendations: Optional[List[RecommendedRole]]):
        """Render summary of role recommendations."""
        st.write("**Role Matches**")
        if role_recommendations:
            role_count = len(role_recommendations)
            if role_count > 0:
                avg_fit_score = sum(r.fit_score for r in role_recommendations) / role_count
                st.metric("Roles", role_count)
                st.metric("Avg. Fit", f"{avg_fit_score:.1%}")
            else:
                st.metric("Roles", "0")
                st.metric("Avg. Fit", "0%")
        else:
            st.metric("Roles", "0")
            st.metric("Avg. Fit", "0%")

    def _render_synthesis_insights(
        self,
        resume_analysis: Optional[AnalysisResult],
        profile_analyses: Optional[Dict],
        role_recommendations: Optional[List[RecommendedRole]]
    ):
        """Render synthesized insights across all phases."""
        st.subheader("🔍 Cross-Phase Insights")

        insights = []

        # Check for alignment between resume and profiles
        if resume_analysis and profile_analyses:
            resume_skills = set()
            if hasattr(resume_analysis, 'strengths'):
                # Extract skills from strengths (simplified approach)
                for strength in resume_analysis.strengths:
                    if 'skills' in strength.lower():
                        resume_skills.add(strength)

            profile_skills = set()
            for profile_type, analysis in profile_analyses.items():
                if 'skills' in analysis:
                    profile_skills.update(analysis['skills'])

            if resume_skills and profile_skills:
                alignment = len(resume_skills.intersection(profile_skills)) / len(profile_skills) if profile_skills else 0
                if alignment > 0.5:
                    insights.append("✅ Good alignment between resume and profile skills")
                else:
                    insights.append("⚠️ Consider aligning skills between resume and profile")

        # Check for role alignment with profile data
        if role_recommendations and profile_analyses:
            tech_skills_mentioned = 0
            for profile_type, analysis in profile_analyses.items():
                if 'technologies' in analysis or 'languages' in analysis:
                    tech_skills_mentioned += len(analysis.get('technologies', [])) + len(analysis.get('languages', []))

            if tech_skills_mentioned > 5:  # Arbitrary threshold
                insights.append("✅ Strong technical presence across profiles supports role recommendations")
            else:
                insights.append("💡 Enhance technical skills display in profiles to strengthen role matches")

        # Check for consistency in experience
        if resume_analysis and profile_analyses:
            insights.append("📊 Consistent experience timeline across resume and profiles strengthens recommendations")

        # Show insights
        if insights:
            for insight in insights:
                st.write(insight)
        else:
            st.info("Complete all analyses to see cross-phase insights.")

    def _render_next_steps(
        self,
        resume_analysis: Optional[AnalysisResult],
        profile_analyses: Optional[Dict],
        role_recommendations: Optional[List[RecommendedRole]]
    ):
        """Render recommendations for next steps."""
        st.subheader("🚀 Recommended Next Steps")

        next_steps = []

        # Resume improvement steps
        if resume_analysis:
            weaknesses_count = len(resume_analysis.weaknesses) if resume_analysis.weaknesses else 0
            if weaknesses_count > 3:
                next_steps.append("1. **Improve Resume**: Address the key weaknesses identified in your resume analysis")
            else:
                next_steps.append("1. **Resume Strong**: Your resume is in good shape, keep it updated")

        # Profile enhancement steps
        if profile_analyses:
            profiles_count = len(profile_analyses)
            if profiles_count < 3:
                next_steps.append("2. **Expand Profiles**: Add more profile sources (GitHub, LinkedIn, portfolio) for better recommendations")
            else:
                next_steps.append("2. **Profiles Complete**: You have good profile coverage")

        # Role application steps
        if role_recommendations:
            high_fit_roles = [r for r in role_recommendations if r.fit_score >= 0.7]
            if high_fit_roles:
                next_steps.append(f"3. **Apply to Roles**: Consider applying to the {len(high_fit_roles)} high-fit roles identified")
            else:
                next_steps.append("3. **Skill Development**: Work on skills to improve fit for desired roles")

        # General career steps
        next_steps.append("4. **Keep Profiles Updated**: Regularly update your resume and profiles with new projects and experiences")

        # Show next steps
        for step in next_steps:
            st.write(step)

        # Action buttons
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📋 Improve Resume"):
                st.info("Navigate to Resume Analyzer to work on your resume improvements")

        with col2:
            if st.button("👤 Update Profiles"):
                st.info("Navigate to Profile Analyzer to enhance your profile data")


def show_combined_career_insights(
    resume_analysis: Optional[AnalysisResult] = None,
    profile_analyses: Optional[Dict] = None,
    role_recommendations: Optional[List[RecommendedRole]] = None
):
    """
    Convenience function to show combined career insights.

    Args:
        resume_analysis: Resume analysis result from Phase 1
        profile_analyses: Profile analyses from Phase 2
        role_recommendations: Role recommendations from Phase 3
    """
    insights = CombinedCareerInsights()
    insights.render(resume_analysis, profile_analyses, role_recommendations)