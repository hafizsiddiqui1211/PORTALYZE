"""Gap analysis display component for showing skill gaps and improvement suggestions"""

import streamlit as st
from typing import List, Optional
from enum import Enum

from ...models.gap_analysis import SkillGap, GapAnalysis


class ImportanceLevel(Enum):
    """Enumeration for skill gap importance levels"""
    CRITICAL = "CRITICAL"
    IMPORTANT = "IMPORTANT"
    NICE_TO_HAVE = "NICE_TO_HAVE"


class GapDisplay:
    """UI component for displaying skill gaps and improvement suggestions"""

    def __init__(self):
        pass

    def render(self,
               missing_skills: List[str],
               improvement_suggestions: List[str],
               skill_gaps: Optional[List[SkillGap]] = None,
               key_prefix: str = "gap_display"):
        """
        Render the gap analysis display.

        Args:
            missing_skills: List of missing skills
            improvement_suggestions: List of improvement suggestions
            skill_gaps: Optional list of SkillGap objects with importance levels
            key_prefix: Prefix for Streamlit widget keys to ensure uniqueness
        """
        if not missing_skills and not improvement_suggestions:
            st.info("No skill gaps or improvement suggestions identified.")
            return

        # Display missing skills section
        if missing_skills:
            st.subheader("🔍 Missing Skills")

            for i, skill in enumerate(missing_skills):
                # Default to IMPORTANT if no detailed gap analysis available
                importance = self._get_importance_for_skill(skill, skill_gaps)

                # Display skill with color coding based on importance
                self._display_skill_with_importance(skill, importance, f"{key_prefix}_skill_{i}")

        # Display improvement suggestions section
        if improvement_suggestions:
            st.subheader("💡 Improvement Suggestions")

            for i, suggestion in enumerate(improvement_suggestions):
                # Style based on importance if available
                card_key = f"{key_prefix}_suggestion_{i}"
                with st.container():
                    st.markdown(
                        f"""
                        <div style="
                            border-left: 4px solid #1f77b4;
                            padding: 10px;
                            margin: 10px 0;
                            background-color: #f8f9fa;
                            border-radius: 4px;
                        ">
                            <strong> suggestion</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                        )

    def _get_importance_for_skill(self, skill: str, skill_gaps: Optional[List[SkillGap]]) -> ImportanceLevel:
        """
        Get the importance level for a skill from the skill gaps list.

        Args:
            skill: The skill name
            skill_gaps: List of SkillGap objects with importance levels

        Returns:
            ImportanceLevel: The importance level for the skill
        """
        if skill_gaps:
            for gap in skill_gaps:
                if gap.skill_name.lower() == skill.lower():
                    # Convert string importance to enum
                    try:
                        return ImportanceLevel(gap.importance.upper())
                    except ValueError:
                        # Default to IMPORTANT if invalid importance value
                        return ImportanceLevel.IMPORTANT

        # Default importance if not specified
        return ImportanceLevel.IMPORTANT

    def _display_skill_with_importance(self, skill: str, importance: ImportanceLevel, key: str):
        """
        Display a skill with color coding based on importance.

        Args:
            skill: The skill name to display
            importance: The importance level of the skill
            key: Unique key for the Streamlit element
        """
        # Define colors based on importance
        color_map = {
            ImportanceLevel.CRITICAL: "#dc3545",      # Red
            ImportanceLevel.IMPORTANT: "#fd7e14",     # Orange
            ImportanceLevel.NICE_TO_HAVE: "#6c757d"  # Gray
        }

        icon_map = {
            ImportanceLevel.CRITICAL: "🔴",
            ImportanceLevel.IMPORTANT: "🟡",
            ImportanceLevel.NICE_TO_HAVE: "⚪"
        }

        color = color_map[importance]
        icon = icon_map[importance]

        # Create styled container for the skill
        st.markdown(
            f"""
            <div style="
                border-left: 4px solid {color};
                padding: 8px 12px;
                margin: 8px 0;
                background-color: #f8f9fa;
                border-radius: 0 4px 4px 0;
                display: flex;
                align-items: center;
            ">
                <span style="margin-right: 10px; font-size: 1.2em;">{icon}</span>
                <span style="color: #495057; font-weight: 500;">{skill}</span>
                <span style="
                    margin-left: auto;
                    padding: 2px 8px;
                    background-color: {color}20;
                    color: {color};
                    border-radius: 12px;
                    font-size: 0.8em;
                    text-transform: uppercase;
                    font-weight: bold;
                ">{importance.value}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    def render_gap_analysis_summary(self,
                                  gap_analysis: GapAnalysis,
                                  key_prefix: str = "gap_summary"):
        """
        Render a summary view of the gap analysis.

        Args:
            gap_analysis: The GapAnalysis object to display
            key_prefix: Prefix for Streamlit widget keys
        """
        if not gap_analysis.missing_skills and not gap_analysis.improvement_suggestions:
            st.info("No gaps identified in the analysis.")
            return

        # Create summary statistics
        total_gaps = len(gap_analysis.missing_skills) if gap_analysis.missing_skills else 0
        total_suggestions = len(gap_analysis.improvement_suggestions) if gap_analysis.improvement_suggestions else 0

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Missing Skills", total_gaps)

        with col2:
            st.metric("Improvement Suggestions", total_suggestions)

        # Display the actual gaps and suggestions
        self.render(
            missing_skills=gap_analysis.missing_skills or [],
            improvement_suggestions=gap_analysis.improvement_suggestions or [],
            skill_gaps=gap_analysis.skill_gaps,
            key_prefix=key_prefix
        )

    def render_priority_aware_display(self,
                                    missing_skills: List[str],
                                    improvement_suggestions: List[str],
                                    skill_gaps: Optional[List[SkillGap]] = None,
                                    key_prefix: str = "priority_gap_display"):
        """
        Render gap analysis with priority ordering and visual emphasis.

        Args:
            missing_skills: List of missing skills
            improvement_suggestions: List of improvement suggestions
            skill_gaps: Optional list of SkillGap objects with importance levels
            key_prefix: Prefix for Streamlit widget keys
        """
        if not missing_skills and not improvement_suggestions:
            st.info("No skill gaps or improvement suggestions identified.")
            return

        # Separate skills by importance level
        critical_skills = []
        important_skills = []
        nice_to_have_skills = []

        if skill_gaps:
            for gap in skill_gaps:
                try:
                    importance = ImportanceLevel(gap.importance.upper())
                    if importance == ImportanceLevel.CRITICAL:
                        critical_skills.append(gap.skill_name)
                    elif importance == ImportanceLevel.IMPORTANT:
                        important_skills.append(gap.skill_name)
                    else:
                        nice_to_have_skills.append(gap.skill_name)
                except ValueError:
                    # Default to important if invalid importance value
                    important_skills.append(gap.skill_name)
        else:
            # If no detailed gap analysis, treat all as important
            important_skills = missing_skills

        # Display in order of priority
        if critical_skills:
            st.subheader("🔴 Critical Gaps")
            st.markdown("**Address these first to significantly improve role fit**")
            for skill in critical_skills:
                self._display_skill_with_importance(
                    skill,
                    ImportanceLevel.CRITICAL,
                    f"{key_prefix}_critical_{skill.replace(' ', '_')}"
                )

        if important_skills:
            st.subheader("🟡 Important Gaps")
            st.markdown("**Focus on these next to strengthen your profile**")
            for skill in important_skills:
                self._display_skill_with_importance(
                    skill,
                    ImportanceLevel.IMPORTANT,
                    f"{key_prefix}_important_{skill.replace(' ', '_')}"
                )

        if nice_to_have_skills:
            st.subheader("⚪ Nice-to-Have Skills")
            st.markdown("**Consider these for long-term growth**")
            for skill in nice_to_have_skills:
                self._display_skill_with_importance(
                    skill,
                    ImportanceLevel.NICE_TO_HAVE,
                    f"{key_prefix}_nice_{skill.replace(' ', '_')}"
                )

        # Display improvement suggestions
        if improvement_suggestions:
            st.subheader("💡 Actionable Steps")
            st.markdown("**Concrete steps to address identified gaps**")

            for i, suggestion in enumerate(improvement_suggestions):
                st.markdown(
                    f"""
                    <div style="
                        padding: 12px;
                        margin: 8px 0;
                        background-color: #e7f3ff;
                        border-radius: 6px;
                        border-left: 3px solid #1f77b4;
                    ">
                        <span style="color: #1f77b4; font-weight: 600;">Step {i+1}:</span> {suggestion}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def show_gap_display(missing_skills: List[str],
                     improvement_suggestions: List[str],
                     skill_gaps: Optional[List[SkillGap]] = None,
                     key_prefix: str = "gap_display"):
    """
    Convenience function to show gap analysis in a Streamlit app.

    Args:
        missing_skills: List of missing skills
        improvement_suggestions: List of improvement suggestions
        skill_gaps: Optional list of SkillGap objects with importance levels
        key_prefix: Prefix for Streamlit widget keys
    """
    display = GapDisplay()
    display.render(missing_skills, improvement_suggestions, skill_gaps, key_prefix)


def show_priority_gap_display(missing_skills: List[str],
                             improvement_suggestions: List[str],
                             skill_gaps: Optional[List[SkillGap]] = None,
                             key_prefix: str = "priority_gap_display"):
    """
    Convenience function to show priority-aware gap analysis in a Streamlit app.

    Args:
        missing_skills: List of missing skills
        improvement_suggestions: List of improvement suggestions
        skill_gaps: Optional list of SkillGap objects with importance levels
        key_prefix: Prefix for Streamlit widget keys
    """
    display = GapDisplay()
    display.render_priority_aware_display(missing_skills, improvement_suggestions, skill_gaps, key_prefix)