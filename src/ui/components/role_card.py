"""Role recommendation card component for job role recommender"""

import streamlit as st
from typing import List
from datetime import datetime

from ...models.role_recommendation import RecommendedRole


class RoleCard:
    """UI component for displaying a role recommendation"""

    def __init__(self):
        pass

    def render(self, recommended_role: RecommendedRole, key_prefix: str = "role_card"):
        """
        Render a role recommendation card.

        Args:
            recommended_role: The recommended role to display
            key_prefix: Prefix for Streamlit widget keys to ensure uniqueness
        """
        # Determine color based on fit score
        fit_score = recommended_role.fit_score
        if fit_score >= 0.8:
            card_color = "🟢"
            score_text = "Excellent Match"
        elif fit_score >= 0.6:
            card_color = "🟡"
            score_text = "Good Match"
        elif fit_score >= 0.4:
            card_color = "🟠"
            score_text = "Moderate Match"
        else:
            card_color = "🔴"
            score_text = "Low Match"

        # Create the card using a container
        with st.container():
            st.markdown(
                f"""
                <div style="
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: #f9f9f9;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #1f77b4;">{recommended_role.title}</h4>
                        <span style="font-size: 1.2em;">{card_color}</span>
                    </div>
                    <p style="margin: 8px 0 5px 0; font-weight: bold; color: #666;">
                        {recommended_role.industry} • {recommended_role.seniority_level}
                    </p>
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span>Fit Score: {score_text}</span>
                            <span style="font-weight: bold; color: #1f77b4;">{fit_score:.1%}</span>
                        </div>
                        <div style="width: 100%; background-color: #e0e0e0; border-radius: 5px; margin: 5px 0;">
                            <div style="
                                width: {fit_score * 100}%;
                                height: 10px;
                                background-color: {'#2ecc71' if fit_score >= 0.6 else '#f39c12' if fit_score >= 0.4 else '#e74c3c'};
                                border-radius: 5px;
                            "></div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Expandable section for justifications
            with st.expander("View Justification", expanded=False):
                self._render_justification_details(recommended_role)

            # Expandable section for skill gaps and suggestions
            if recommended_role.skill_gaps or recommended_role.improvement_suggestions:
                with st.expander("Skill Gaps & Improvements", expanded=False):
                    self._render_skill_gaps_and_suggestions(recommended_role)

    def _render_justification_details(self, recommended_role: RecommendedRole):
        """Render the justification details for the role."""
        justification = recommended_role.justification

        if 'skill_alignment' in justification:
            st.markdown(f"**Skill Alignment:** {justification['skill_alignment']}")

        if 'project_relevance' in justification:
            st.markdown(f"**Project Relevance:** {justification['project_relevance']}")

        if 'technology_match' in justification:
            st.markdown(f"**Technology Match:** {justification['technology_match']}")

        if 'experience_alignment' in justification:
            st.markdown(f"**Experience Alignment:** {justification['experience_alignment']}")

        # Show conflict explanations if present
        if 'conflict_explanation' in justification:
            st.markdown("**⚠️ Conflict Explanation:**")
            st.warning(f"{justification['conflict_explanation']}")
            st.markdown("*This suggests multiple potential career paths or mixed signals in your profile.*")

        # Show confidence factors
        if recommended_role.confidence_factors:
            st.markdown("**Confidence Factors:**")
            for factor in recommended_role.confidence_factors:
                st.markdown(f"- {factor}")

    def _render_skill_gaps_and_suggestions(self, recommended_role: RecommendedRole):
        """Render skill gaps and improvement suggestions."""
        from .gap_display import show_priority_gap_display

        # Use the new gap display component for better visualization
        show_priority_gap_display(
            missing_skills=recommended_role.skill_gaps or [],
            improvement_suggestions=recommended_role.improvement_suggestions or [],
            skill_gaps=None,  # If we have detailed SkillGap objects, we'd pass them here
            key_prefix=f"role_gaps_{recommended_role.role_id}"
        )

    def render_multiple_roles(self, recommended_roles: List[RecommendedRole], key_prefix: str = "role_cards"):
        """
        Render multiple role recommendation cards.

        Args:
            recommended_roles: List of recommended roles to display
            key_prefix: Prefix for Streamlit widget keys
        """
        if not recommended_roles:
            st.info("No role recommendations to display.")
            return

        # Sort roles by fit score (descending)
        sorted_roles = sorted(recommended_roles, key=lambda r: r.fit_score, reverse=True)

        # Display each role
        for i, role in enumerate(sorted_roles):
            self.render(role, key_prefix=f"{key_prefix}_role_{i}")

        # Show summary statistics
        avg_fit_score = sum(r.fit_score for r in sorted_roles) / len(sorted_roles)
        st.markdown(f"**Average Fit Score:** {avg_fit_score:.1%} across {len(sorted_roles)} roles")


# Function to use the role card in Streamlit apps
def show_role_card(recommended_role: RecommendedRole, key_prefix: str = "role_card"):
    """
    Convenience function to show a role card in a Streamlit app.

    Args:
        recommended_role: The recommended role to display
        key_prefix: Prefix for Streamlit widget keys
    """
    card = RoleCard()
    card.render(recommended_role, key_prefix)


def show_multiple_role_cards(recommended_roles: List[RecommendedRole], key_prefix: str = "role_cards"):
    """
    Convenience function to show multiple role cards in a Streamlit app.

    Args:
        recommended_roles: List of recommended roles to display
        key_prefix: Prefix for Streamlit widget keys
    """
    card = RoleCard()
    card.render_multiple_roles(recommended_roles, key_prefix)