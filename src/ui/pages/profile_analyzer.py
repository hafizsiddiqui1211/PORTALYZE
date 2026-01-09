"""Profile Analyzer page for Resume Analyzer Core"""
import streamlit as st
from typing import Dict, List, Optional
from src.models.profile_url import ProfileURL
from src.models.profile_analysis import ProfileAnalysis
from src.services.url_validator import URLValidator
from src.services.linkedin_extractor import LinkedInExtractor
from src.services.github_extractor import GitHubExtractor
from src.services.portfolio_extractor import PortfolioExtractor
from src.services.ai_service import AIService
from src.ui.components.url_input import render_url_input_form
from src.ui.components.validation_status import render_validation_status_detailed
from src.ui.components.results_display import render_analysis_results, render_profile_comparison
from src.utils.logger import get_logger


def render_profile_analyzer_page(
    url_validator: URLValidator,
    linkedin_extractor: LinkedInExtractor,
    github_extractor: GitHubExtractor,
    portfolio_extractor: PortfolioExtractor,
    ai_service: AIService
):
    """Render the profile analyzer page."""
    st.title("🌐 Profile Analyzer")
    st.subheader("Analyze your LinkedIn, GitHub, and portfolio websites for optimization")

    # Initialize session state for profile analysis
    if 'profile_urls' not in st.session_state:
        st.session_state.profile_urls = {}
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {}
    if 'profile_analyses' not in st.session_state:
        st.session_state.profile_analyses = {}
    if 'profiles_analyzed' not in st.session_state:
        st.session_state.profiles_analyzed = False

    # Main content area
    if not st.session_state.profiles_analyzed:
        # URL input section
        profile_urls, submitted = render_url_input_form()

        if submitted and profile_urls:
            with st.spinner("Validating profile URLs..."):
                validated_urls = {}
                all_valid = True

                for platform, url in profile_urls.items():
                    if url.strip():  # Only process non-empty URLs
                        is_valid, error_msg = url_validator.validate_url_format(url)
                        is_accessible = url_validator.check_url_accessibility(url) if is_valid else False

                        profile_url = ProfileURL.create_new(
                            url=url,
                            session_id="current_session",  # In a real app, use actual session ID
                            profile_type=url_validator.detect_profile_type(url),
                            is_valid=is_valid,
                            is_accessible=is_accessible,
                            error_message=error_msg if not is_valid else None
                        )

                        validated_urls[platform] = profile_url

                        if not is_valid:
                            all_valid = False
                            st.error(f"Invalid {platform} URL: {error_msg}")

                if all_valid:
                    st.session_state.profile_urls = validated_urls

                    # Show validation results
                    st.subheader("✅ URL Validation Results")
                    for platform, profile_url in validated_urls.items():
                        render_validation_status_detailed(profile_url, platform.title())

                    # Extract profile data
                    with st.spinner("Extracting profile data..."):
                        profile_data = {}
                        extraction_errors = []

                        for platform, profile_url in validated_urls.items():
                            if profile_url.is_valid and profile_url.is_accessible:
                                try:
                                    if profile_url.profile_type == "LINKEDIN":
                                        data = linkedin_extractor.extract(profile_url.url)
                                        # Check if LinkedIn extraction returned minimal data due to privacy restrictions
                                        if data and len(data) <= 3:  # Only contains url, profile_type and maybe profile_image
                                            st.warning(f"⚠️ LinkedIn profile may have limited public data available due to privacy settings. Only basic information could be extracted.")
                                    elif profile_url.profile_type == "GITHUB":
                                        data = github_extractor.extract(profile_url.url)
                                    else:  # PORTFOLIO
                                        data = portfolio_extractor.extract(profile_url.url)

                                    profile_data[platform] = data
                                except Exception as e:
                                    # Handle LinkedIn-specific privacy/access errors
                                    error_str = str(e).lower()
                                    if profile_url.profile_type == "LINKEDIN" and (
                                        "private" in error_str or "not found" in error_str or
                                        "404" in error_str or "forbidden" in error_str or
                                        "access denied" in error_str or "rate limit" in error_str or
                                        "scraping" in error_str or "block" in error_str
                                    ):
                                        st.warning(f"⚠️ LinkedIn profile may not be publicly accessible due to privacy settings. Profile: {profile_url.url}")
                                        # Still try to create minimal data for the profile
                                        data = {
                                            "url": profile_url.url,
                                            "profile_type": "LINKEDIN",
                                            "error": "Profile not publicly accessible due to privacy settings"
                                        }
                                        profile_data[platform] = data
                                    else:
                                        extraction_errors.append(f"Error extracting {platform} profile: {str(e)}")
                                        st.error(f"Error extracting {platform} profile: {str(e)}")

                        if extraction_errors:
                            st.warning(f"Some profiles had extraction errors, but {len(profile_data)} profiles were extracted successfully.")

                        st.session_state.profile_data = profile_data

                    # Analyze profiles
                    with st.spinner("Analyzing profiles with AI..."):
                        profile_analyses = {}
                        analysis_errors = []

                        for platform, profile_datum in profile_data.items():
                            try:
                                # Use the ai_service to analyze the profile
                                # Note: This is a simplified implementation - the actual method may vary
                                # depending on how the AIService is designed to work with profile data
                                analysis = ai_service.analyze_profile(
                                    profile_data=profile_datum,
                                    profile_type=profile_datum.profile_type
                                )
                                profile_analyses[platform] = analysis
                            except Exception as e:
                                analysis_errors.append(f"Error analyzing {platform} profile: {str(e)}")
                                st.error(f"Error analyzing {platform} profile: {str(e)}")

                        if analysis_errors:
                            st.warning(f"Some profiles had analysis errors, but {len(profile_analyses)} profiles were analyzed successfully.")

                        st.session_state.profile_analyses = profile_analyses

                        # Only set profiles_analyzed to True if at least one profile was analyzed
                        st.session_state.profiles_analyzed = len(profile_analyses) > 0

                    if profile_analyses:  # At least one profile was analyzed successfully
                        st.success(f"Successfully analyzed {len(profile_analyses)} profiles!")
                        st.rerun()
                    else:
                        st.error("No profiles could be analyzed successfully.")
                        # Reset the state so user can try again
                        st.session_state.profiles_analyzed = False
                else:
                    st.warning("Please fix the invalid URLs before proceeding.")
    else:
        # Display analysis results
        if st.session_state.profile_analyses and len(st.session_state.profile_analyses) > 0:
            st.subheader("📈 Profile Analysis Results")

            # Display each profile analysis
            for platform, analysis in st.session_state.profile_analyses.items():
                profile_url = st.session_state.profile_urls.get(platform)
                render_analysis_results(analysis, profile_url)

            # If multiple profiles were analyzed, show comparison
            if len(st.session_state.profile_analyses) > 1:
                st.subheader("⚖️ Profile Comparison")
                analyses_list = list(st.session_state.profile_analyses.values())
                render_profile_comparison(analyses_list)

            # Button to analyze another set of profiles
            if st.button("🔄 Analyze Another Set of Profiles"):
                st.session_state.profiles_analyzed = False
                st.session_state.profile_urls = {}
                st.session_state.profile_data = {}
                st.session_state.profile_analyses = {}
                st.rerun()

        else:
            st.warning("No profile analysis results available. Please go back and enter profile URLs to analyze.")
            # Button to go back and analyze profiles
            if st.button("← Go Back to Enter Profile URLs"):
                st.session_state.profiles_analyzed = False
                st.session_state.profile_urls = {}
                st.session_state.profile_data = {}
                st.session_state.profile_analyses = {}
                st.rerun()