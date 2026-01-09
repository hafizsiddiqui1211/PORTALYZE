"""Streamlit main application for Resume Analyzer Core"""

import streamlit as st
from pathlib import Path
import tempfile
import os
import sys
from typing import Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv(".env"))
    api_key = os.getenv("GEMINI_API_KEY")

except ImportError:
    # If python-dotenv is not installed, continue without loading .env file
    pass

# Add the project root to the Python path to resolve 'src' imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import our modules
from src.services.file_processor import FileProcessor
from src.services.text_extractor import TextExtractor
from src.services.ats_analyzer import ATSAnalyzer
from src.services.ai_service import AIService
from src.services.url_validator import URLValidator
from src.services.linkedin_extractor import LinkedInExtractor
from src.services.github_extractor import GitHubExtractor
from src.services.portfolio_extractor import PortfolioExtractor
from src.services.ai_service import AIService
from src.ui.components.file_uploader import render_file_uploader_with_validation
from src.ui.components.url_input import render_url_input_form
from src.ui.pages.resume_analyzer import render_resume_analyzer_page
from src.ui.pages.profile_analyzer import render_profile_analyzer_page
from src.ui.pages.dashboard import render_dashboard_page
from src.utils.constants import MAX_FILE_SIZE, SUPPORTED_FILE_TYPES
from src.utils.security import cleanup_old_temp_files_with_sessions
from src.utils.logger import setup_logging, get_logger
from src.utils.theme import apply_theme


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    # Resume analysis state
    if "resume_analyzed" not in st.session_state:
        st.session_state.resume_analyzed = False
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "keyword_suggestions" not in st.session_state:
        st.session_state.keyword_suggestions = []
    if "original_filename" not in st.session_state:
        st.session_state.original_filename = ""

    # Profile analysis state
    if "profile_analyzed" not in st.session_state:
        st.session_state.profile_analyzed = False
    if "profile_urls" not in st.session_state:
        st.session_state.profile_urls = {}
    if "profile_data" not in st.session_state:
        st.session_state.profile_data = {}
    if "profile_analyses" not in st.session_state:
        st.session_state.profile_analyses = {}

    # Active page state
    if "active_page" not in st.session_state:
        st.session_state.active_page = "resume_analyzer"

    # Theme state
    if "theme" not in st.session_state:
        st.session_state.theme = "system"  # Default to system theme


def main():
    """Main application function."""
    # Initialize logging
    logger = setup_logging()
    logger.info("Starting Resume & Profile Analyzer application")

    st.set_page_config(
        page_title="PORTALYZE",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # Initialize session state
    initialize_session_state()

    # Apply the selected theme
    apply_theme()

    # Initialize services
    file_processor = FileProcessor(max_file_size=MAX_FILE_SIZE)
    text_extractor = TextExtractor()
    ats_analyzer = ATSAnalyzer()
    ai_service = AIService()  # Will use GEMINI_API_KEY from environment
    url_validator = URLValidator()
    linkedin_extractor = LinkedInExtractor()
    github_extractor = GitHubExtractor()
    portfolio_extractor = PortfolioExtractor()
    ai_service2 = AIService()  # Will use GEMINI_API_KEY from environment

    # Create navigation sidebar
    with st.sidebar:
        st.image("https://placehold.co/200x50?text=PORTALYZE", width=200)

        st.header("🧭 Navigation")
        page = st.radio(
            "Select Analysis Type:",
            [
                "Resume Analyzer",
                # "Profile Analyzer",
                "Role Recommendations",
                # "Unified Dashboard",
            ],
            index=[
                "Resume Analyzer",
                # "Profile Analyzer",
                "Role Recommendations",
                # "Unified Dashboard",
            ].index(st.session_state.active_page.replace("_", " ").title())
            if st.session_state.active_page.replace("_", " ").title()
            in [
                "Resume Analyzer",
                # "Profile Analyzer",
                "Role Recommendations",
                # "Unified Dashboard",
            ]
            else 0,
        )

        # Update active page based on selection
        page_mapping = {
            "Resume Analyzer": "resume_analyzer",
            # "Profile Analyzer": "profile_analyzer",
            "Role Recommendations": "role_recommendations",
            # "Unified Dashboard": "dashboard",
        }
        st.session_state.active_page = page_mapping[page]

        st.divider()

        st.header("📋 How It Works")
        st.write("""
        **Resume Analyzer**: Upload your resume for ATS compatibility analysis
        
        **Role Recommendations**: Get personalized role suggestions based on your profile
        """)

        st.header("ℹ️ About")
        st.write("Enhance your professional presence with AI-powered analysis.")

        # Theme selection
        st.header("🎨 Theme")
        theme_options = {
            "system": "Use system setting",
            "light": "Light theme",
            "dark": "Dark theme",
        }
        theme_keys = list(theme_options.keys())
        theme_values = list(theme_options.values())

        # Get current theme index
        try:
            current_index = theme_keys.index(st.session_state.theme)
        except ValueError:
            current_index = 0  # Default to system if invalid theme is stored

        selected_label = st.radio(
            "Choose theme:",
            options=theme_values,
            index=current_index,
            key="theme_selector",
            horizontal=True,
        )

        # Convert back to theme key
        selected_theme = theme_keys[theme_values.index(selected_label)]

        if selected_theme != st.session_state.theme:
            st.session_state.theme = selected_theme
            st.rerun()

        # Clean up old temp files periodically
        if st.button("🧹 Clean Temp Files"):
            cleanup_old_temp_files_with_sessions()
            st.success("Temporary files cleaned!")

    # Main content area based on selected page
    if st.session_state.active_page == "resume_analyzer":
        render_resume_analyzer_page(
            file_processor=file_processor,
            text_extractor=text_extractor,
            ats_analyzer=ats_analyzer,
            ai_service=ai_service,
        )
    elif st.session_state.active_page == "profile_analyzer":
        render_profile_analyzer_page(
            url_validator=url_validator,
            linkedin_extractor=linkedin_extractor,
            github_extractor=github_extractor,
            portfolio_extractor=portfolio_extractor,
            ai_service=ai_service2,
        )
    elif st.session_state.active_page == "role_recommendations":
        render_role_recommendations_page()
    elif st.session_state.active_page == "dashboard":
        render_dashboard_page()


def render_role_recommendations_page():
    """Render the role recommendations page."""
    import streamlit as st
    from src.ui.components.industry_selector import show_industry_selector
    from src.ui.components.role_card import show_multiple_role_cards
    from src.services.signal_aggregator import get_signal_aggregator
    from src.services.role_inferencer import get_role_inferencer
    from src.services.consent_manager import get_consent_manager
    import asyncio

    st.header("🎯 Role Recommendations")
    st.write(
        "Get personalized role suggestions based on your profile and target industries."
    )

    # Check if we have resume and profile data to work with
    has_resume_data = st.session_state.get("analysis_result") is not None
    has_profile_data = st.session_state.get("profile_analyzed", False)

    if not has_resume_data and not has_profile_data:
        st.warning(
            "Please complete Resume Analysis and/or Profile Analysis first to get role recommendations."
        )
        st.info("Navigate to Resume Analyzer or Profile Analyzer to get started.")
        return

    # Display data availability summary
    col1, col2 = st.columns(2)
    with col1:
        if has_resume_data:
            st.success("✅ Resume data available")
        else:
            st.info("ℹ️ Complete Resume Analysis for better recommendations")

    with col2:
        if has_profile_data:
            st.success("✅ Profile data available")
        else:
            st.info("ℹ️ Complete Profile Analysis for better recommendations")

    # Get user's industry selection
    industry_selection = show_industry_selector()

    if industry_selection:
        # Aggregate signals from resume and profile data
        signal_agg = get_signal_aggregator()

        # Prepare resume analysis data
        resume_analysis = st.session_state.get("analysis_result", {})

        # Prepare profile analyses data
        profile_analyses = []
        if st.session_state.get("profile_analyses"):
            for profile_type, analysis in st.session_state["profile_analyses"].items():
                profile_analyses.append({"profile_type": profile_type, **analysis})

        # Aggregate signals
        profile_signals = signal_agg.aggregate_signals(
            resume_analysis=resume_analysis,
            profile_analyses=profile_analyses,
            session_id=st.session_state.get("session_id", "default-session"),
        )

        # Get role recommendations
        if st.button("Generate Role Recommendations"):
            with st.spinner(
                "Analyzing your profile and generating role recommendations..."
            ):
                try:
                    # Initialize role inferencer
                    role_inf = get_role_inferencer()

                    # Get recommendations with timeout
                    recommendations = role_inf.infer_roles_sync_with_timeout(
                        profile_signals=profile_signals,
                        industries=industry_selection.industries,
                        max_roles=5,
                    )

                    if recommendations:
                        st.success(
                            f"Generated {len(recommendations.roles)} role recommendations!"
                        )

                        # Display recommendations
                        show_multiple_role_cards(recommendations.roles)

                        # Store recommendations in session state
                        st.session_state["role_recommendations"] = recommendations

                        # Update dashboard recommendations for seamless integration
                        st.session_state["dashboard_recommendations"] = (
                            recommendations.roles
                        )

                    else:
                        st.error(
                            "Failed to generate role recommendations. Please try again."
                        )

                except Exception as e:
                    st.error(f"Error generating recommendations: {str(e)}")


if __name__ == "__main__":
    main()
