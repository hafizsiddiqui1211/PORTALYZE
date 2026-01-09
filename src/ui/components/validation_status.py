"""Validation status component for Resume Analyzer Core"""
import streamlit as st
from typing import Dict, Optional
from src.models.profile_url import ProfileURL


def render_validation_status(profile_url: Optional[ProfileURL], platform_name: str = "Profile"):
    """
    Render validation status for a profile URL with visual indicators.

    Args:
        profile_url: ProfileURL entity to display status for
        platform_name: Name of the platform (e.g., "LinkedIn", "GitHub", "Portfolio")
    """
    if profile_url is None:
        st.info(f"❌ No {platform_name} URL provided")
        return

    # Determine status and display appropriate indicator
    if profile_url.error_message:
        # Error occurred during validation
        st.error(f"❌ **{platform_name} URL Invalid:** {profile_url.error_message}")

        # Provide specific feedback based on the error
        error_lower = profile_url.error_message.lower()
        if "format" in error_lower or "invalid" in error_lower:
            st.caption("🔧 Please check the URL format. It should be a valid web address.")
        elif "accessible" in error_lower or "connection" in error_lower:
            st.caption("🌐 The URL format is correct but the site may not be accessible. Check if the profile is public.")
        else:
            st.caption(" troubleshoot the issue with the URL.")
    elif not profile_url.is_valid:
        # URL format is invalid
        st.error(f"❌ **{platform_name} URL Invalid:** Incorrect format")
        st.caption(f"Please enter a valid {platform_name} profile URL")
    elif not profile_url.is_accessible:
        # URL format is valid but not accessible
        st.warning(f"⚠️ **{platform_name} URL Valid but Not Accessible:** {profile_url.url}")
        st.caption(f"The {platform_name} URL format is valid, but we couldn't access the profile. This might be because:")
        st.caption("- The profile is set to private")
        st.caption("- The profile doesn't exist anymore")
        st.caption("- The website is temporarily down")
    else:
        # URL is valid and accessible
        st.success(f"✅ **{platform_name} URL Validated Successfully:** {profile_url.url}")
        st.caption(f"This {platform_name} profile will be included in the analysis")


def render_validation_status_detailed(profile_url: Optional[ProfileURL], platform_name: str = "Profile"):
    """
    Render detailed validation status with more information.

    Args:
        profile_url: ProfileURL entity to display status for
        platform_name: Name of the platform (e.g., "LinkedIn", "GitHub", "Portfolio")
    """
    if profile_url is None:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write("❌")
        with col2:
            st.write(f"**{platform_name} URL:** No URL provided")
        return

    # Create columns for status icon and details
    col1, col2 = st.columns([1, 4])

    with col1:
        if profile_url.error_message:
            st.write("❌")
        elif not profile_url.is_valid:
            st.write("❌")
        elif not profile_url.is_accessible:
            st.write("⚠️")
        else:
            st.write("✅")

    with col2:
        st.write(f"**{platform_name} URL:** {profile_url.url}")

        if profile_url.error_message:
            st.error(f"*Error:* {profile_url.error_message}")
        elif not profile_url.is_valid:
            st.error("*Status:* Invalid format")
        elif not profile_url.is_accessible:
            st.warning("*Status:* Valid format but not accessible")
            st.info("*Note:* The profile might be private or temporarily unavailable")
        else:
            st.success("*Status:* Valid and accessible")
            if profile_url.profile_type:
                st.info(f"*Detected Type:* {profile_url.profile_type}")


def render_multiple_validation_statuses(profile_urls: Dict[str, ProfileURL]):
    """
    Render validation status for multiple profile URLs.

    Args:
        profile_urls: Dictionary of profile URLs keyed by platform name
    """
    if not profile_urls:
        st.info("No profile URLs to validate.")
        return

    st.subheader("Validation Status Overview")

    # Create a summary of validation results
    total_urls = len(profile_urls)
    valid_urls = sum(1 for url in profile_urls.values() if url and url.is_valid and url.is_accessible)
    invalid_urls = sum(1 for url in profile_urls.values() if url and not url.is_valid)
    inaccessible_urls = sum(1 for url in profile_urls.values() if url and url.is_valid and not url.is_accessible)

    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total URLs", total_urls)
    col2.metric("Valid & Accessible", valid_urls)
    col3.metric("Invalid Format", invalid_urls)
    col4.metric("Inaccessible", inaccessible_urls)

    # Display individual statuses
    for platform, profile_url in profile_urls.items():
        render_validation_status(profile_url, platform.capitalize())


def render_validation_status_with_spinner(url: str, platform_name: str = "Profile", validating: bool = False):
    """
    Render validation status with a spinner during validation.

    Args:
        url: The URL being validated
        platform_name: Name of the platform
        validating: Whether validation is in progress
    """
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if validating:
            st.write("⏳")  # Hourglass while validating
        else:
            # Determine final status icon after validation
            # This would need to be connected to the actual validation result
            st.write("🔄")  # Refresh icon as placeholder

    with col2:
        st.write(f"**{platform_name} URL:** {url}")

    with col3:
        if validating:
            st.write("Validating...")  # Show validating status


def render_profile_validation_card(profile_url: ProfileURL, platform_name: str = "Profile"):
    """
    Render a card-style validation status display.

    Args:
        profile_url: ProfileURL entity to display
        platform_name: Name of the platform
    """
    if profile_url is None:
        st.markdown(
            f"""
            <div style="
                border: 2px dashed #ccc;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                background-color: #fafafa;
            ">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 24px; margin-right: 10px;">❌</div>
                    <div>
                        <strong>{platform_name} Profile</strong><br>
                        <small>No URL provided</small>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # Determine status for styling
    if profile_url.error_message or not profile_url.is_valid:
        border_color = "#dc3545"  # Red for errors
        icon = "❌"
        status_text = "Invalid"
        bg_color = "#f8d7da"
    elif not profile_url.is_accessible:
        border_color = "#ffc107"  # Yellow for warnings
        icon = "⚠️"
        status_text = "Not Accessible"
        bg_color = "#fff3cd"
    else:
        border_color = "#28a745"  # Green for success
        icon = "✅"
        status_text = "Valid & Accessible"
        bg_color = "#d4edda"

    st.markdown(
        f"""
        <div style="
            border: 2px solid {border_color};
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background-color: {bg_color};
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center;">
                        <div style="font-size: 24px; margin-right: 10px;">{icon}</div>
                        <div>
                            <strong>{platform_name} Profile</strong><br>
                            <small style="color: #555;">{profile_url.url}</small>
                        </div>
                    </div>
                    <div style="margin-top: 10px;">
                        <span style="
                            background-color: {border_color};
                            color: white;
                            padding: 2px 8px;
                            border-radius: 12px;
                            font-size: 0.8em;
                        ">{status_text}</span>
                    </div>
                </div>
            </div>
            {f'<div style="margin-top: 10px; font-size: 0.9em;"><strong>Error:</strong> {profile_url.error_message}</div>' if profile_url.error_message else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def get_validation_summary(profile_urls: Dict[str, ProfileURL]) -> Dict[str, int]:
    """
    Get a summary of validation results.

    Args:
        profile_urls: Dictionary of profile URLs keyed by platform name

    Returns:
        Dictionary with counts of different validation statuses
    """
    summary = {
        "total": 0,
        "valid_accessible": 0,
        "valid_inaccessible": 0,
        "invalid_format": 0,
        "errors": 0
    }

    for profile_url in profile_urls.values():
        if profile_url is None:
            continue

        summary["total"] += 1

        if profile_url.error_message or not profile_url.is_valid:
            summary["errors"] += 1
        elif not profile_url.is_accessible:
            summary["valid_inaccessible"] += 1
        else:
            summary["valid_accessible"] += 1

    return summary


def is_validation_complete(profile_urls: Dict[str, ProfileURL]) -> bool:
    """
    Check if all provided URLs have been validated.

    Args:
        profile_urls: Dictionary of profile URLs keyed by platform name

    Returns:
        True if all non-None URLs have been validated, False otherwise
    """
    if not profile_urls:
        return False

    for profile_url in profile_urls.values():
        if profile_url is not None:
            # If there's a profile URL object, assume it's been validated
            # (since it would have been created after validation)
            continue

    # If we have at least one profile URL, consider validation complete
    return len(profile_urls) > 0 and any(url is not None for url in profile_urls.values())


def get_ready_for_analysis_count(profile_urls: Dict[str, ProfileURL]) -> int:
    """
    Get the count of URLs that are ready for analysis (valid and accessible).

    Args:
        profile_urls: Dictionary of profile URLs keyed by platform name

    Returns:
        Number of URLs ready for analysis
    """
    count = 0
    for profile_url in profile_urls.values():
        if profile_url and profile_url.is_valid and profile_url.is_accessible:
            count += 1
    return count