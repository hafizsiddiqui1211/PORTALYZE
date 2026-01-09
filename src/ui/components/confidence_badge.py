"""Confidence badge component for displaying confidence levels in role recommendations"""

import streamlit as st
from typing import Optional, List
from enum import Enum


class ConfidenceLevel(Enum):
    """Enumeration for confidence levels"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ConfidenceBadge:
    """UI component for displaying confidence indicators with color-coded badges"""

    def __init__(self):
        pass

    def render(self, confidence_score: float, factors: Optional[List[str]] = None, key_prefix: str = "confidence_badge"):
        """
        Render a confidence badge based on the confidence score.

        Args:
            confidence_score: Confidence score between 0.0 and 1.0
            factors: List of factors that influence the confidence
            key_prefix: Prefix for Streamlit widget keys to ensure uniqueness
        """
        confidence_level = self._get_confidence_level(confidence_score)
        badge_info = self._get_badge_info(confidence_level)

        # Display the main confidence badge
        self._display_confidence_badge(confidence_level, confidence_score, badge_info)

        # Display confidence factors if provided
        if factors:
            self._display_confidence_factors(factors, key_prefix)

    def _get_confidence_level(self, confidence_score: float) -> ConfidenceLevel:
        """
        Determine the confidence level based on the score.

        Args:
            confidence_score: Confidence score between 0.0 and 1.0

        Returns:
            ConfidenceLevel: The determined confidence level
        """
        if confidence_score >= 0.7:
            return ConfidenceLevel.HIGH
        elif confidence_score >= 0.4:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    def _get_badge_info(self, confidence_level: ConfidenceLevel) -> dict:
        """
        Get display information for a confidence level.

        Args:
            confidence_level: The confidence level

        Returns:
            Dictionary with color, icon, and text information
        """
        info_map = {
            ConfidenceLevel.HIGH: {
                "color": "#2ecc71",  # Green
                "icon": "🟢",
                "text": "High Confidence",
                "description": "Strong match with comprehensive profile data"
            },
            ConfidenceLevel.MEDIUM: {
                "color": "#f39c12",  # Orange
                "icon": "🟡",
                "text": "Medium Confidence",
                "description": "Reasonable match with partial profile data"
            },
            ConfidenceLevel.LOW: {
                "color": "#e74c3c",  # Red
                "icon": "🔴",
                "text": "Low Confidence",
                "description": "Limited match with minimal profile data"
            }
        }

        return info_map[confidence_level]

    def _display_confidence_badge(self, confidence_level: ConfidenceLevel, confidence_score: float, badge_info: dict):
        """
        Display the confidence badge with color coding.

        Args:
            confidence_level: The confidence level
            confidence_score: The numerical confidence score
            badge_info: Dictionary with display information
        """
        # Create a styled container for the confidence badge
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 16px;
                margin: 10px 0;
                background-color: {badge_info['color']}20;
                border: 1px solid {badge_info['color']};
                border-radius: 8px;
                color: {badge_info['color']};
            ">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.5em; margin-right: 10px;">{badge_info['icon']}</span>
                    <div>
                        <div style="font-weight: bold; font-size: 1.1em;">{badge_info['text']}</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">{badge_info['description']}</div>
                    </div>
                </div>
                <div style="font-weight: bold; font-size: 1.2em; text-align: right;">
                    {confidence_score:.1%}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    def _display_confidence_factors(self, factors: List[str], key_prefix: str):
        """
        Display confidence factors with expandable explanation.

        Args:
            factors: List of factors that influence confidence
            key_prefix: Prefix for Streamlit widget keys
        """
        with st.expander("Confidence Factors", expanded=False):
            st.markdown("**Factors affecting confidence:**")
            for i, factor in enumerate(factors):
                st.markdown(f"{i+1}. {factor}")

    def render_compact_badge(self, confidence_score: float, key_prefix: str = "compact_confidence"):
        """
        Render a compact confidence badge suitable for inline display.

        Args:
            confidence_score: Confidence score between 0.0 and 1.0
            key_prefix: Prefix for Streamlit widget keys
        """
        confidence_level = self._get_confidence_level(confidence_score)
        badge_info = self._get_badge_info(confidence_level)

        # Create a compact badge
        st.markdown(
            f"""
            <span style="
                display: inline-block;
                padding: 4px 10px;
                margin: 2px;
                background-color: {badge_info['color']}20;
                color: {badge_info['color']};
                border: 1px solid {badge_info['color']};
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: bold;
            ">
                {badge_info['icon']} {confidence_score:.0%}
            </span>
            """,
            unsafe_allow_html=True
        )

    def render_detailed_confidence_analysis(self,
                                          confidence_score: float,
                                          factors: Optional[List[str]] = None,
                                          recommendations_count: int = 0,
                                          data_completeness: float = 0.0,
                                          key_prefix: str = "detailed_confidence"):
        """
        Render a detailed confidence analysis with multiple metrics.

        Args:
            confidence_score: Overall confidence score
            factors: List of confidence factors
            recommendations_count: Number of recommendations made
            data_completeness: Completeness of profile data (0.0 to 1.0)
            key_prefix: Prefix for Streamlit widget keys
        """
        col1, col2, col3 = st.columns(3)

        with col1:
            self._display_metric_card(
                "Overall Confidence",
                f"{confidence_score:.1%}",
                self._get_confidence_level(confidence_score)
            )

        with col2:
            self._display_metric_card(
                "Recommendations",
                str(recommendations_count),
                ConfidenceLevel.HIGH if recommendations_count > 0 else ConfidenceLevel.LOW
            )

        with col3:
            self._display_metric_card(
                "Data Completeness",
                f"{data_completeness:.1%}",
                self._get_confidence_level(data_completeness)
            )

        # Display factors if available
        if factors:
            with st.expander("Detailed Confidence Analysis", expanded=True):
                st.markdown("#### Confidence Factors")
                for factor in factors:
                    confidence_level = self._assess_factor_impact(factor)
                    factor_icon = self._get_factor_icon(confidence_level)
                    st.markdown(f"{factor_icon} {factor}")

    def _display_metric_card(self, title: str, value: str, confidence_level: ConfidenceLevel):
        """
        Display a metric card with appropriate styling.

        Args:
            title: Title of the metric
            value: Value to display
            confidence_level: Confidence level for styling
        """
        badge_info = self._get_badge_info(confidence_level)

        st.markdown(
            f"""
            <div style="
                padding: 12px;
                text-align: center;
                background-color: {badge_info['color']}10;
                border: 1px solid {badge_info['color']}40;
                border-radius: 8px;
                margin: 5px 0;
            ">
                <div style="font-size: 1.4em; font-weight: bold; color: {badge_info['color']};">
                    {value}
                </div>
                <div style="font-size: 0.8em; color: #666;">
                    {title}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    def _assess_factor_impact(self, factor: str) -> ConfidenceLevel:
        """
        Assess the impact of a confidence factor.

        Args:
            factor: The confidence factor text

        Returns:
            ConfidenceLevel: The impact level
        """
        # Simple heuristic based on keywords in the factor
        factor_lower = factor.lower()

        if any(keyword in factor_lower for keyword in ['strong', 'good', 'excellent', 'comprehensive']):
            return ConfidenceLevel.HIGH
        elif any(keyword in factor_lower for keyword in ['moderate', 'partial', 'some']):
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    def _get_factor_icon(self, confidence_level: ConfidenceLevel) -> str:
        """
        Get an appropriate icon for a confidence level.

        Args:
            confidence_level: The confidence level

        Returns:
            String with appropriate icon
        """
        icon_map = {
            ConfidenceLevel.HIGH: "✅",
            ConfidenceLevel.MEDIUM: "⚠️",
            ConfidenceLevel.LOW: "❌"
        }
        return icon_map[confidence_level]


def show_confidence_badge(confidence_score: float, factors: Optional[List[str]] = None, key_prefix: str = "confidence_badge"):
    """
    Convenience function to show a confidence badge in a Streamlit app.

    Args:
        confidence_score: Confidence score between 0.0 and 1.0
        factors: List of factors that influence the confidence
        key_prefix: Prefix for Streamlit widget keys
    """
    badge = ConfidenceBadge()
    badge.render(confidence_score, factors, key_prefix)


def show_compact_confidence_badge(confidence_score: float, key_prefix: str = "compact_confidence"):
    """
    Convenience function to show a compact confidence badge in a Streamlit app.

    Args:
        confidence_score: Confidence score between 0.0 and 1.0
        key_prefix: Prefix for Streamlit widget keys
    """
    badge = ConfidenceBadge()
    badge.render_compact_badge(confidence_score, key_prefix)