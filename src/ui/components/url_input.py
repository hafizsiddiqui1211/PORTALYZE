"""URL input component for Resume Analyzer Core"""
import streamlit as st
from typing import Dict, Optional, Tuple
from src.models.profile_url import ProfileURL
from src.services.url_validator import URLValidator


def render_url_input_form() -> Tuple[Dict[str, str], bool]:
    """
    Render the URL input form with validation.

    Returns:
        Tuple of (urls_dict, is_submitted) where urls_dict contains the entered URLs
        and is_submitted indicates if the form was submitted
    """
    st.header("🔗 Profile URL Input")
    st.write("Enter your profile URLs for analysis. We'll validate and analyze each profile.")

    # Initialize session state for URL inputs if not already done
    if 'linkedin_url' not in st.session_state:
        st.session_state.linkedin_url = ""
    if 'github_url' not in st.session_state:
        st.session_state.github_url = ""
    if 'portfolio_url' not in st.session_state:
        st.session_state.portfolio_url = ""

    # Create form for URL input
    with st.form(key="url_input_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            linkedin_url = st.text_input(
                "LinkedIn Profile URL",
                value=st.session_state.linkedin_url,
                placeholder="https://www.linkedin.com/in/your-profile",
                help="Enter your LinkedIn profile URL"
            )

        with col2:
            github_url = st.text_input(
                "GitHub Profile URL",
                value=st.session_state.github_url,
                placeholder="https://github.com/your-username",
                help="Enter your GitHub profile URL"
            )

        with col3:
            portfolio_url = st.text_input(
                "Portfolio Website URL",
                value=st.session_state.portfolio_url,
                placeholder="https://your-portfolio.com",
                help="Enter your personal portfolio website URL"
            )

        submit_button = st.form_submit_button("Validate & Analyze Profiles")

    # Handle form submission
    if submit_button:
        # Update session state with entered URLs
        st.session_state.linkedin_url = linkedin_url
        st.session_state.github_url = github_url
        st.session_state.portfolio_url = portfolio_url

        # Validate URLs
        validator = URLValidator()

        # Collect non-empty URLs
        urls_to_validate = {}
        if linkedin_url.strip():
            urls_to_validate["linkedin"] = linkedin_url
        if github_url.strip():
            urls_to_validate["github"] = github_url
        if portfolio_url.strip():
            urls_to_validate["portfolio"] = portfolio_url

        if not urls_to_validate:
            st.warning("Please enter at least one profile URL.")
            return {}, False

        # Validate each URL
        all_valid = True
        for platform, url in urls_to_validate.items():
            is_valid, error_msg = validator.validate_url_format(url)
            if not is_valid:
                st.error(f"Invalid {platform.title()} URL: {error_msg}")
                all_valid = False
            else:
                # Check accessibility
                is_accessible = validator.check_url_accessibility(url)
                if not is_accessible:
                    st.warning(f"{platform.title()} URL may not be accessible: {url}")

        if not all_valid:
            return {}, False

        # If all URLs are valid, return them
        return urls_to_validate, True

    return {}, False


def render_url_validation_status(profile_urls: Dict[str, ProfileURL]):
    """
    Render validation status for the entered URLs.

    Args:
        profile_urls: Dictionary of ProfileURL entities keyed by platform
    """
    if not profile_urls:
        return

    st.subheader("✅ URL Validation Status")

    for platform, profile_url in profile_urls.items():
        if profile_url.is_valid and profile_url.is_accessible:
            st.success(f"✅ **{platform.title()} URL**: Valid and accessible")
        elif profile_url.is_valid and not profile_url.is_accessible:
            st.warning(f"⚠️ **{platform.title()} URL**: Valid format but not accessible")
        else:
            st.error(f"❌ **{platform.title()} URL**: Invalid - {profile_url.error_message}")


def render_url_input_with_validation() -> Tuple[Dict[str, str], bool]:
    """
    Render URL input with real-time validation.

    Returns:
        Tuple of (urls_dict, is_submitted)
    """
    st.header("🔗 Profile URL Input with Validation")
    st.write("Enter your profile URLs for analysis. URLs will be validated in real-time.")

    # Initialize session state
    if 'linkedin_url' not in st.session_state:
        st.session_state.linkedin_url = ""
    if 'github_url' not in st.session_state:
        st.session_state.github_url = ""
    if 'portfolio_url' not in st.session_state:
        st.session_state.portfolio_url = ""
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = {}

    # URL input fields
    col1, col2, col3 = st.columns(3)

    with col1:
        linkedin_url = st.text_input(
            "LinkedIn Profile URL",
            value=st.session_state.linkedin_url,
            placeholder="https://www.linkedin.com/in/your-profile"
        )
        # Real-time validation for LinkedIn URL
        if linkedin_url != st.session_state.linkedin_url:
            st.session_state.linkedin_url = linkedin_url
            if linkedin_url.strip():
                validator = URLValidator()
                is_valid, error_msg = validator.validate_url_format(linkedin_url)
                if is_valid:
                    is_accessible = validator.check_url_accessibility(linkedin_url)
                    profile_url = ProfileURL.create_new(
                        url=linkedin_url,
                        session_id="temp",
                        profile_type=validator.detect_profile_type(linkedin_url),
                        is_valid=True,
                        is_accessible=is_accessible
                    )
                    st.session_state.validation_results["linkedin"] = profile_url
                    if is_accessible:
                        st.success("✅ Valid and accessible")
                    else:
                        st.warning("⚠️ Valid format but not accessible")
                else:
                    st.error(f"❌ {error_msg}")

    with col2:
        github_url = st.text_input(
            "GitHub Profile URL",
            value=st.session_state.github_url,
            placeholder="https://github.com/your-username"
        )
        # Real-time validation for GitHub URL
        if github_url != st.session_state.github_url:
            st.session_state.github_url = github_url
            if github_url.strip():
                validator = URLValidator()
                is_valid, error_msg = validator.validate_url_format(github_url)
                if is_valid:
                    is_accessible = validator.check_url_accessibility(github_url)
                    profile_url = ProfileURL.create_new(
                        url=github_url,
                        session_id="temp",
                        profile_type=validator.detect_profile_type(github_url),
                        is_valid=True,
                        is_accessible=is_accessible
                    )
                    st.session_state.validation_results["github"] = profile_url
                    if is_accessible:
                        st.success("✅ Valid and accessible")
                    else:
                        st.warning("⚠️ Valid format but not accessible")
                else:
                    st.error(f"❌ {error_msg}")

    with col3:
        portfolio_url = st.text_input(
            "Portfolio Website URL",
            value=st.session_state.portfolio_url,
            placeholder="https://your-portfolio.com"
        )
        # Real-time validation for Portfolio URL
        if portfolio_url != st.session_state.portfolio_url:
            st.session_state.portfolio_url = portfolio_url
            if portfolio_url.strip():
                validator = URLValidator()
                is_valid, error_msg = validator.validate_url_format(portfolio_url)
                if is_valid:
                    is_accessible = validator.check_url_accessibility(portfolio_url)
                    profile_url = ProfileURL.create_new(
                        url=portfolio_url,
                        session_id="temp",
                        profile_type=validator.detect_profile_type(portfolio_url),
                        is_valid=True,
                        is_accessible=is_accessible
                    )
                    st.session_state.validation_results["portfolio"] = profile_url
                    if is_accessible:
                        st.success("✅ Valid and accessible")
                    else:
                        st.warning("⚠️ Valid format but not accessible")
                else:
                    st.error(f"❌ {error_msg}")

    # Submit button
    submitted = st.button("Analyze Profiles")

    if submitted:
        # Collect valid URLs
        urls_to_submit = {}

        if linkedin_url and "linkedin" in st.session_state.validation_results:
            linkedin_validation = st.session_state.validation_results["linkedin"]
            if linkedin_validation.is_valid:
                urls_to_submit["linkedin"] = linkedin_url

        if github_url and "github" in st.session_state.validation_results:
            github_validation = st.session_state.validation_results["github"]
            if github_validation.is_valid:
                urls_to_submit["github"] = github_url

        if portfolio_url and "portfolio" in st.session_state.validation_results:
            portfolio_validation = st.session_state.validation_results["portfolio"]
            if portfolio_validation.is_valid:
                urls_to_submit["portfolio"] = portfolio_url

        return urls_to_submit, True

    return {}, False


def render_profile_selection_interface() -> Tuple[Dict[str, str], bool]:
    """
    Render a more comprehensive profile selection interface.

    Returns:
        Tuple of (urls_dict, is_submitted)
    """
    st.header("🎯 Profile Analysis Setup")
    st.write("Enter the URLs for your profiles that you'd like us to analyze and provide feedback on.")

    # Initialize session state
    if 'profiles_data' not in st.session_state:
        st.session_state.profiles_data = {
            'linkedin': {'url': '', 'validated': False, 'accessible': False, 'error': ''},
            'github': {'url': '', 'validated': False, 'accessible': False, 'error': ''},
            'portfolio': {'url': '', 'validated': False, 'accessible': False, 'error': ''}
        }

    # Create tabs for each profile type
    tab1, tab2, tab3 = st.tabs(["👔 LinkedIn Profile", "💻 GitHub Profile", "🌐 Portfolio Website"])

    with tab1:
        linkedin_url = st.text_input(
            "LinkedIn Profile URL",
            value=st.session_state.profiles_data['linkedin']['url'],
            placeholder="Paste your LinkedIn profile URL here...",
            help="Example: https://www.linkedin.com/in/your-profile"
        )

        # Update session state when URL changes
        if linkedin_url != st.session_state.profiles_data['linkedin']['url']:
            st.session_state.profiles_data['linkedin']['url'] = linkedin_url
            st.session_state.profiles_data['linkedin']['validated'] = False
            st.session_state.profiles_data['linkedin']['accessible'] = False
            st.session_state.profiles_data['linkedin']['error'] = ''

    with tab2:
        github_url = st.text_input(
            "GitHub Profile URL",
            value=st.session_state.profiles_data['github']['url'],
            placeholder="Paste your GitHub profile URL here...",
            help="Example: https://github.com/your-username"
        )

        # Update session state when URL changes
        if github_url != st.session_state.profiles_data['github']['url']:
            st.session_state.profiles_data['github']['url'] = github_url
            st.session_state.profiles_data['github']['validated'] = False
            st.session_state.profiles_data['github']['accessible'] = False
            st.session_state.profiles_data['github']['error'] = ''

    with tab3:
        portfolio_url = st.text_input(
            "Portfolio Website URL",
            value=st.session_state.profiles_data['portfolio']['url'],
            placeholder="Paste your portfolio website URL here...",
            help="Example: https://your-portfolio.com"
        )

        # Update session state when URL changes
        if portfolio_url != st.session_state.profiles_data['portfolio']['url']:
            st.session_state.profiles_data['portfolio']['url'] = portfolio_url
            st.session_state.profiles_data['portfolio']['validated'] = False
            st.session_state.profiles_data['portfolio']['accessible'] = False
            st.session_state.profiles_data['portfolio']['error'] = ''

    # Validation and submission buttons
    validate_col, analyze_col = st.columns([1, 1])

    with validate_col:
        validate_btn = st.button("🔍 Validate URLs", type="secondary")

    with analyze_col:
        analyze_btn = st.button("🚀 Analyze Profiles", type="primary")

    # Handle validation
    if validate_btn:
        validator = URLValidator()

        # Validate LinkedIn URL
        if linkedin_url.strip():
            is_valid, error_msg = validator.validate_url_format(linkedin_url)
            st.session_state.profiles_data['linkedin']['validated'] = is_valid
            st.session_state.profiles_data['linkedin']['error'] = error_msg or ''

            if is_valid:
                is_accessible = validator.check_url_accessibility(linkedin_url)
                st.session_state.profiles_data['linkedin']['accessible'] = is_accessible
                if is_accessible:
                    st.success(f"✅ LinkedIn URL validated and accessible")
                else:
                    st.warning(f"⚠️ LinkedIn URL format valid but not accessible")
            else:
                st.error(f"❌ LinkedIn URL invalid: {error_msg}")

        # Validate GitHub URL
        if github_url.strip():
            is_valid, error_msg = validator.validate_url_format(github_url)
            st.session_state.profiles_data['github']['validated'] = is_valid
            st.session_state.profiles_data['github']['error'] = error_msg or ''

            if is_valid:
                is_accessible = validator.check_url_accessibility(github_url)
                st.session_state.profiles_data['github']['accessible'] = is_accessible
                if is_accessible:
                    st.success(f"✅ GitHub URL validated and accessible")
                else:
                    st.warning(f"⚠️ GitHub URL format valid but not accessible")
            else:
                st.error(f"❌ GitHub URL invalid: {error_msg}")

        # Validate Portfolio URL
        if portfolio_url.strip():
            is_valid, error_msg = validator.validate_url_format(portfolio_url)
            st.session_state.profiles_data['portfolio']['validated'] = is_valid
            st.session_state.profiles_data['portfolio']['error'] = error_msg or ''

            if is_valid:
                is_accessible = validator.check_url_accessibility(portfolio_url)
                st.session_state.profiles_data['portfolio']['accessible'] = is_accessible
                if is_accessible:
                    st.success(f"✅ Portfolio URL validated and accessible")
                else:
                    st.warning(f"⚠️ Portfolio URL format valid but not accessible")
            else:
                st.error(f"❌ Portfolio URL invalid: {error_msg}")

    # Handle analysis submission
    if analyze_btn:
        # Check which URLs are valid
        valid_urls = {}

        if (st.session_state.profiles_data['linkedin']['url'] and
            st.session_state.profiles_data['linkedin']['validated']):
            valid_urls['linkedin'] = st.session_state.profiles_data['linkedin']['url']

        if (st.session_state.profiles_data['github']['url'] and
            st.session_state.profiles_data['github']['validated']):
            valid_urls['github'] = st.session_state.profiles_data['github']['url']

        if (st.session_state.profiles_data['portfolio']['url'] and
            st.session_state.profiles_data['portfolio']['validated']):
            valid_urls['portfolio'] = st.session_state.profiles_data['portfolio']['url']

        if not valid_urls:
            st.warning("Please enter and validate at least one profile URL.")
            return {}, False

        return valid_urls, True

    return {}, False