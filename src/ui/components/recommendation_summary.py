"""Recommendation summary component for job role recommender"""

import streamlit as st
from typing import List, Optional
from datetime import datetime

from ...models.role_recommendation import RecommendedRole


class RecommendationSummary:
    """UI component for displaying a summary of role recommendations"""

    def __init__(self):
        pass

    def render(
        self,
        recommended_roles: List[RecommendedRole],
        show_top_n: int = 3,
        show_detailed_metrics: bool = True
    ):
        """
        Render a summary of role recommendations.

        Args:
            recommended_roles: List of recommended roles to summarize
            show_top_n: Number of top roles to show in detail
            show_detailed_metrics: Whether to show detailed metrics
        """
        if not recommended_roles:
            st.info("No role recommendations to display.")
            return

        # Sort roles by fit score (descending)
        sorted_roles = sorted(recommended_roles, key=lambda r: r.fit_score, reverse=True)

        # Display summary header
        total_roles = len(sorted_roles)
        avg_fit_score = sum(r.fit_score for r in sorted_roles) / total_roles if total_roles > 0 else 0
        top_role = sorted_roles[0] if sorted_roles else None

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Roles Recommended", total_roles)
        with col2:
            st.metric("Avg. Fit Score", f"{avg_fit_score:.1%}")
        with col3:
            if top_role:
                st.metric("Top Role", top_role.title)

        st.markdown("---")

        # Show top roles in detail
        st.subheader(f"Top {min(show_top_n, total_roles)} Recommendations")

        for i, role in enumerate(sorted_roles[:show_top_n]):
            self._render_role_summary_card(role, i + 1)

        # Show summary statistics
        if show_detailed_metrics:
            self._render_detailed_metrics(sorted_roles)

    def _render_role_summary_card(self, role: RecommendedRole, rank: int):
        """Render a summary card for a single role."""
        # Determine color based on fit score
        fit_score = role.fit_score
        if fit_score >= 0.8:
            card_color = "#2ecc71"  # Green
            score_text = "Excellent Match"
        elif fit_score >= 0.6:
            card_color = "#f39c12"  # Orange
            score_text = "Good Match"
        elif fit_score >= 0.4:
            card_color = "#e67e22"  # Amber
            score_text = "Moderate Match"
        else:
            card_color = "#e74c3c"  # Red
            score_text = "Low Match"

        # Create the card using a container
        with st.container():
            st.markdown(
                f"""
                <div style="
                    border: 2px solid {card_color};
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: #f9f9f9;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h5 style="margin: 0; color: #2c3e50;">{rank}. {role.title}</h5>
                        <span style="font-weight: bold; color: {card_color};">{fit_score:.1%}</span>
                    </div>
                    <p style="margin: 8px 0 5px 0; font-size: 0.9em; color: #7f8c8d;">
                        {role.industry} • {role.seniority_level}
                    </p>
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 0.8em;">{score_text}</span>
                        </div>
                        <div style="width: 100%; background-color: #ecf0f1; border-radius: 5px; margin: 5px 0;">
                            <div style="
                                width: {fit_score * 100}%;
                                height: 8px;
                                background-color: {card_color};
                                border-radius: 5px;
                            "></div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    def _render_detailed_metrics(self, sorted_roles: List[RecommendedRole]):
        """Render detailed metrics about the recommendations."""
        st.subheader("Detailed Metrics")

        # Breakdown by seniority level
        seniority_counts = {}
        for role in sorted_roles:
            level = role.seniority_level
            seniority_counts[level] = seniority_counts.get(level, 0) + 1

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**By Seniority Level:**")
            for level, count in seniority_counts.items():
                st.write(f"- {level}: {count}")

        # Breakdown by fit score ranges
        excellent_count = sum(1 for r in sorted_roles if r.fit_score >= 0.8)
        good_count = sum(1 for r in sorted_roles if 0.6 <= r.fit_score < 0.8)
        moderate_count = sum(1 for r in sorted_roles if 0.4 <= r.fit_score < 0.6)
        low_count = sum(1 for r in sorted_roles if r.fit_score < 0.4)

        with col2:
            st.write("**By Fit Score:**")
            st.write(f"- Excellent (80%+): {excellent_count}")
            st.write(f"- Good (60-79%): {good_count}")
            st.write(f"- Moderate (40-59%): {moderate_count}")
            st.write(f"- Low (<40%): {low_count}")

        # Average metrics by industry
        industry_metrics = {}
        for role in sorted_roles:
            industry = role.industry
            if industry not in industry_metrics:
                industry_metrics[industry] = []
            industry_metrics[industry].append(role.fit_score)

        with col3:
            st.write("**By Industry:**")
            for industry, scores in industry_metrics.items():
                avg_score = sum(scores) / len(scores)
                st.write(f"- {industry}: {avg_score:.1%}")


def show_recommendation_summary(
    recommended_roles: List[RecommendedRole],
    show_top_n: int = 3,
    show_detailed_metrics: bool = True
):
    """
    Convenience function to show recommendation summary.

    Args:
        recommended_roles: List of recommended roles to summarize
        show_top_n: Number of top roles to show in detail
        show_detailed_metrics: Whether to show detailed metrics
    """
    summary = RecommendationSummary()
    summary.render(recommended_roles, show_top_n, show_detailed_metrics)