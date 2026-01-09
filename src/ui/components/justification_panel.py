"""Justification panel component for displaying role recommendation justifications"""

import streamlit as st
from typing import Dict, Any, List, Optional

from ...models.role_recommendation import RecommendedRole


class JustificationPanel:
    """UI component for displaying detailed justifications for role recommendations"""

    def __init__(self):
        pass

    def render(self, recommended_role: RecommendedRole, key_prefix: str = "justification_panel"):
        """
        Render a detailed justification panel for a role recommendation.

        Args:
            recommended_role: The recommended role to display justifications for
            key_prefix: Prefix for Streamlit widget keys to ensure uniqueness
        """
        justification = recommended_role.justification

        if not justification:
            st.info("No justification details available for this role.")
            return

        # Display each justification component
        col1, col2 = st.columns(2)

        with col1:
            # Skill alignment
            if 'skill_alignment' in justification:
                with st.expander("🎯 Skill Alignment", expanded=True):
                    st.markdown(justification['skill_alignment'])

            # Experience alignment
            if 'experience_alignment' in justification:
                with st.expander("💼 Experience Alignment", expanded=True):
                    st.markdown(justification['experience_alignment'])

        with col2:
            # Project relevance
            if 'project_relevance' in justification:
                with st.expander("📁 Project Relevance", expanded=True):
                    st.markdown(justification['project_relevance'])

            # Technology match
            if 'technology_match' in justification:
                with st.expander("💻 Technology Match", expanded=True):
                    st.markdown(justification['technology_match'])

        # Seniority alignment if available
        if 'seniority_alignment' in justification:
            with st.expander("📈 Seniority Level Justification", expanded=True):
                st.markdown(justification['seniority_alignment'])

        # Additional reasoning if available
        if hasattr(recommended_role, 'reasoning') and recommended_role.reasoning:
            with st.expander("💡 Additional Reasoning", expanded=True):
                for reason in recommended_role.reasoning:
                    st.markdown(f"- {reason}")

    def render_multiple_justifications(self, recommended_roles: List[RecommendedRole], key_prefix: str = "justification_panels"):
        """
        Render justification panels for multiple role recommendations.

        Args:
            recommended_roles: List of recommended roles to display justifications for
            key_prefix: Prefix for Streamlit widget keys
        """
        if not recommended_roles:
            st.info("No role recommendations to display justifications for.")
            return

        # Create tabs for each role
        role_titles = [role.title for role in recommended_roles]
        tabs = st.tabs(role_titles)

        for i, (tab, role) in enumerate(zip(tabs, recommended_roles)):
            with tab:
                self.render(role, key_prefix=f"{key_prefix}_justification_{i}")

    def render_collapsible_justifications(self, recommended_roles: List[RecommendedRole], key_prefix: str = "collapsible_justifications"):
        """
        Render collapsible justifications for all roles in a single view.

        Args:
            recommended_roles: List of recommended roles to display justifications for
            key_prefix: Prefix for Streamlit widget keys
        """
        if not recommended_roles:
            st.info("No role recommendations to display justifications for.")
            return

        for i, role in enumerate(recommended_roles):
            with st.expander(f" Justiication for {role.title} - {role.industry}", expanded=False):
                self.render(role, key_prefix=f"{key_prefix}_role_{i}")


def show_justification_panel(recommended_role: RecommendedRole, key_prefix: str = "justification_panel"):
    """
    Convenience function to show a justification panel in a Streamlit app.

    Args:
        recommended_role: The recommended role to display justifications for
        key_prefix: Prefix for Streamlit widget keys
    """
    panel = JustificationPanel()
    panel.render(recommended_role, key_prefix)


def show_multiple_justification_panels(recommended_roles: List[RecommendedRole], key_prefix: str = "justification_panels"):
    """
    Convenience function to show multiple justification panels in a Streamlit app.

    Args:
        recommended_roles: List of recommended roles to display justifications for
        key_prefix: Prefix for Streamlit widget keys
    """
    panel = JustificationPanel()
    panel.render_multiple_justifications(recommended_roles, key_prefix)