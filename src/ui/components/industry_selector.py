"""Industry selector component for job role recommender"""

import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime

from ...models.industry import IndustrySelection
from ...utils.constants import SUPPORTED_INDUSTRIES


class IndustrySelector:
    """UI component for selecting target industries and specializations"""

    def __init__(self):
        pass

    def render(self, key_prefix: str = "industry_selection") -> Optional[IndustrySelection]:
        """
        Render the industry selection component.

        Args:
            key_prefix: Prefix for Streamlit widget keys to ensure uniqueness

        Returns:
            IndustrySelection object if selection is made, None otherwise
        """
        st.subheader("Select Target Industries")

        # Industry selection with multi-select
        selected_industries = st.multiselect(
            label="Choose your target industries:",
            options=SUPPORTED_INDUSTRIES,
            default=[],
            key=f"{key_prefix}_industries"
        )

        if not selected_industries:
            st.info("Please select at least one industry to receive role recommendations.")
            return None

        # Specialization selection based on selected industries
        specializations = self._get_specializations_for_industries(selected_industries)
        selected_specializations = []

        if specializations:
            st.markdown("**Select Specializations (Optional)**")

            # Create expandable sections for each selected industry
            for industry, industry_specs in specializations.items():
                with st.expander(f"Specializations for {industry}", expanded=False):
                    industry_selected = st.multiselect(
                        label=f"Select specializations for {industry}:",
                        options=industry_specs,
                        default=[],
                        key=f"{key_prefix}_specs_{industry.lower().replace('/', '').replace(' ', '_')}",
                        help=f"Select relevant specializations for {industry} roles"
                    )
                    selected_specializations.extend(industry_selected)

        # Create industry selection object
        if selected_industries:
            selection_id = f"selection_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(selected_industries)) % 10000}"
            session_id = st.session_state.get('session_id', 'unknown')

            industry_selection = IndustrySelection(
                selection_id=selection_id,
                session_id=session_id,
                industries=selected_industries,
                specializations=selected_specializations if selected_specializations else None,
                selection_timestamp=datetime.now()
            )

            return industry_selection

        return None

    def _get_specializations_for_industries(self, industries: List[str]) -> Dict[str, List[str]]:
        """
        Get available specializations for the selected industries.

        Args:
            industries: List of selected industries

        Returns:
            Dictionary mapping industries to their specializations
        """
        specializations_map = {
            "AI/ML": [
                "Machine Learning Engineer",
                "Data Scientist",
                "AI Researcher",
                "Computer Vision Engineer",
                "NLP Engineer",
                "MLOps Engineer"
            ],
            "Software Engineering": [
                "Frontend Developer",
                "Backend Developer",
                "Full Stack Developer",
                "DevOps Engineer",
                "Platform Engineer",
                "Security Engineer",
                "Mobile Developer"
            ],
            "Data": [
                "Data Engineer",
                "Data Analyst",
                "Business Intelligence Analyst",
                "Data Architect",
                "Analytics Engineer",
                "Data Science Manager"
            ],
            "FinTech": [
                "FinTech Developer",
                "Quantitative Developer",
                "Blockchain Developer",
                "Payment Systems Engineer",
                "Risk Engineer",
                "Compliance Engineer"
            ],
            "EdTech": [
                "Learning Platform Developer",
                "Educational Data Analyst",
                "EdTech Product Manager",
                "Instructional Designer",
                "Learning Experience Designer"
            ],
            "Cloud": [
                "Cloud Solutions Architect",
                "AWS Engineer",
                "Azure Engineer",
                "Google Cloud Engineer",
                "Cloud Security Engineer",
                "Cloud DevOps Engineer"
            ],
            "Cybersecurity": [
                "Security Engineer",
                "Security Analyst",
                "Penetration Tester",
                "Security Architect",
                "Incident Responder",
                "Compliance Specialist"
            ],
            "DevOps": [
                "DevOps Engineer",
                "Site Reliability Engineer",
                "Infrastructure Engineer",
                "Platform Engineer",
                "Release Engineer",
                "CI/CD Specialist"
            ]
        }

        # Return specializations only for the selected industries
        result = {}
        for industry in industries:
            if industry in specializations_map:
                result[industry] = specializations_map[industry]

        return result

    def display_selection_summary(self, selection: IndustrySelection):
        """
        Display a summary of the industry selection.

        Args:
            selection: IndustrySelection object to display
        """
        st.success(f"Selected {len(selection.industries)} industry(ies): {', '.join(selection.industries)}")

        if selection.specializations:
            st.info(f"Selected specializations: {', '.join(selection.specializations)}")

        st.caption(f"Selection ID: {selection.selection_id}")
        st.caption(f"Timestamp: {selection.selection_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")


# Function to use the industry selector in Streamlit apps
def show_industry_selector(key_prefix: str = "industry_selection") -> Optional[IndustrySelection]:
    """
    Convenience function to show the industry selector in a Streamlit app.

    Args:
        key_prefix: Prefix for Streamlit widget keys

    Returns:
        IndustrySelection object if selection is made, None otherwise
    """
    selector = IndustrySelector()
    return selector.render(key_prefix)