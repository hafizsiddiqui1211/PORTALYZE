"""Navigation components for Resume Analyzer Core"""
import streamlit as st
from typing import Optional, Dict, Any
from src.models.profile_url import ProfileURL
from src.models.profile_analysis import ProfileAnalysis


def render_main_navigation(current_step: str = "input"):
    """
    Render the main navigation for the application.

    Args:
        current_step: Current step in the process ('input', 'validation', 'results')
    """
    # Create navigation tabs
    tabs = st.tabs(["🔗 Profile URLs", "✅ Validation Status", "📊 Analysis Results", "📋 Summary"])

    # Define step titles
    step_titles = {
        "input": "Profile URL Input",
        "validation": "Validation Status",
        "results": "Analysis Results",
        "summary": "Profile Summary"
    }

    # Update page title based on current step
    st.header(f"🎯 {step_titles.get(current_step, 'Profile Analysis')}")

    return tabs


def render_step_indicator(current_step: str, total_steps: int = 4):
    """
    Render a step indicator showing progress through the process.

    Args:
        current_step: Current step identifier ('input', 'validation', 'results', 'summary')
        total_steps: Total number of steps in the process
    """
    step_map = {
        "input": 1,
        "validation": 2,
        "results": 3,
        "summary": 4
    }

    current_step_num = step_map.get(current_step, 1)

    # Create progress bar
    progress_value = (current_step_num - 1) / (total_steps - 1) if total_steps > 1 else 0
    st.progress(progress_value)

    # Create step labels
    col1, col2, col3, col4 = st.columns(4)

    steps = [
        ("🔗 URLs", "input"),
        ("✅ Validation", "validation"),
        ("📊 Results", "results"),
        ("📋 Summary", "summary")
    ]

    for i, (label, step_key) in enumerate(steps):
        if step_key == current_step:
            # Current step - highlight
            with locals()[f"col{i+1}"]:
                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                        background-color: #007bff;
                        color: white;
                        padding: 8px;
                        border-radius: 4px;
                        font-weight: bold;
                    ">
                        {label}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            # Previous steps - filled if completed
            is_completed = step_map[step_key] < current_step_num
            bg_color = "#28a745" if is_completed else "#e9ecef"
            text_color = "white" if is_completed else "#6c757d"

            with locals()[f"col{i+1}"]:
                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                        background-color: {bg_color};
                        color: {text_color};
                        padding: 8px;
                        border-radius: 4px;
                    ">
                        {label}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def render_navigation_buttons(
    current_step: str,
    on_prev_clicked=None,
    on_next_clicked=None,
    disable_next: bool = False,
    next_label: str = "Next"
):
    """
    Render navigation buttons for moving between steps.

    Args:
        current_step: Current step identifier
        on_prev_clicked: Callback function for previous button
        on_next_clicked: Callback function for next button
        disable_next: Whether to disable the next button
        next_label: Label for the next button
    """
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_step != "input":
            if st.button("⬅️ Previous", key="prev_btn", type="secondary"):
                if on_prev_clicked:
                    on_prev_clicked()

    with col2:
        # Space filler
        st.write("")

    with col3:
        if current_step != "summary":
            if st.button(next_label + " ➡️", key="next_btn", type="primary", disabled=disable_next):
                if on_next_clicked:
                    on_next_clicked()
        else:
            if st.button("🔄 Analyze Again", key="restart_btn", type="secondary"):
                # Reset session state to restart the process
                for key in list(st.session_state.keys()):
                    if key.startswith(('url_', 'validation_', 'analysis_', 'step_')):
                        del st.session_state[key]


def render_profile_analyzer_nav():
    """
    Render the main navigation for the profile analyzer application.
    """
    # Use session state to track current view
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'input'

    # Create horizontal navigation
    nav_options = ['Input', 'Validation', 'Analysis', 'Export']
    nav_icons = ['🔗', '✅', '📊', '📤']

    # Create columns for navigation
    cols = st.columns(len(nav_options))

    for i, (option, icon) in enumerate(zip(nav_options, nav_icons)):
        with cols[i]:
            # Check if this is the current view
            is_current = (st.session_state.current_view == option.lower())

            # Style based on current state
            if is_current:
                btn_style = """
                    <div style="
                        background-color: #007BFF;
                        color: white;
                        padding: 10px;
                        border-radius: 5px;
                        text-align: center;
                        font-weight: bold;
                        border: 2px solid #0056b3;
                    ">
                        {} {}
                    </div>
                """.format(icon, option)
            else:
                btn_style = """
                    <div style="
                        background-color: #f8f9fa;
                        color: #495057;
                        padding: 10px;
                        border-radius: 5px;
                        text-align: center;
                        border: 1px solid #dee2e6;
                    ">
                        {} {}
                    </div>
                """.format(icon, option)

            # Create clickable area using form to handle clicks
            with st.form(key=f"nav_form_{option.lower()}"):
                st.markdown(btn_style, unsafe_allow_html=True)
                nav_submitted = st.form_submit_button(label="", help=f"Go to {option}")

                if nav_submitted:
                    st.session_state.current_view = option.lower()
                    st.rerun()

    # Add a separator
    st.markdown("---")


def switch_to_view(view_name: str):
    """
    Helper function to switch to a specific view.

    Args:
        view_name: Name of the view to switch to
    """
    st.session_state.current_view = view_name.lower()
    st.rerun()


def render_breadcrumb_navigation(current_path: list):
    """
    Render breadcrumb navigation.

    Args:
        current_path: List of path segments representing the current location
    """
    if not current_path:
        return

    # Create a horizontal display of the path
    path_display = " > ".join(current_path)
    st.markdown(
        f"""
        <div style="
            background-color: #e9ecef;
            padding: 8px 12px;
            border-radius: 4px;
            margin-bottom: 16px;
            font-size: 0.9em;
        ">
            {path_display}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_responsive_sidebar_navigation():
    """
    Render a responsive sidebar navigation for larger screens.
    """
    with st.sidebar:
        st.header("📋 Navigation")

        # Define navigation items
        nav_items = [
            {"name": "Profile Input", "icon": "🔗", "view": "input"},
            {"name": "Validation", "icon": "✅", "view": "validation"},
            {"name": "Analysis", "icon": "📊", "view": "analysis"},
            {"name": "Results", "icon": "📈", "view": "results"},
            {"name": "Export", "icon": "📤", "view": "export"}
        ]

        # Create buttons for each navigation item
        for item in nav_items:
            is_active = st.session_state.get('current_view', 'input') == item['view']

            btn_label = f"{item['icon']} {item['name']}"
            btn_type = "primary" if is_active else "secondary"

            if st.button(
                btn_label,
                key=f"nav_{item['view']}",
                type=btn_type
            ):
                st.session_state.current_view = item['view']
                st.rerun()

        st.divider()

        # Additional utilities in sidebar
        if st.button("🔄 Reset Analysis"):
            # Clear relevant session state
            for key in list(st.session_state.keys()):
                if key.startswith(('url_', 'validation_', 'analysis_', 'profile_')):
                    del st.session_state[key]
            st.session_state.current_view = 'input'
            st.rerun()

        if st.button("ℹ️ Help"):
            st.info(
                "Welcome to the Profile Analyzer!\n\n"
                "1. **Input**: Enter your profile URLs\n"
                "2. **Validation**: Check URL validity and accessibility\n"
                "3. **Analysis**: Get AI-powered profile analysis\n"
                "4. **Results**: View detailed feedback and suggestions\n"
                "5. **Export**: Download your analysis report"
            )


def render_tab_navigation_with_completion_status(
    tabs_config: Dict[str, Dict[str, Any]],
    current_tab: str
):
    """
    Render tab navigation with visual indicators for completion status.

    Args:
        tabs_config: Configuration for tabs with completion status
                     Format: {"tab_key": {"title": "...", "completed": True/False, "disabled": True/False}}
        current_tab: Key of the currently active tab
    """
    # Create tabs with appropriate labels that show completion status
    tab_titles = []
    tab_keys = []

    for key, config in tabs_config.items():
        title = config["title"]
        completed = config.get("completed", False)
        disabled = config.get("disabled", False)

        # Add completion indicator to title
        if completed:
            title = f"✅ {title}"
        else:
            title = f"⚪ {title}"

        if disabled:
            title = f"🔒 {config['title']}"  # Lock icon for disabled

        tab_titles.append(title)
        tab_keys.append(key)

    tabs = st.tabs(tab_titles)

    # Return the active tab content container
    for i, key in enumerate(tab_keys):
        if key == current_tab:
            return tabs[i]

    # If current tab not found, return first tab
    return tabs[0] if tabs else None


def get_navigation_state_summary(
    profile_urls: Dict[str, ProfileURL],
    profile_analyses: Dict[str, ProfileAnalysis]
) -> Dict[str, Any]:
    """
    Get a summary of the navigation state for progress tracking.

    Args:
        profile_urls: Dictionary of profile URLs keyed by platform
        profile_analyses: Dictionary of profile analyses keyed by platform

    Returns:
        Dictionary with navigation state summary
    """
    total_profiles = len(profile_urls)
    validated_profiles = sum(1 for url in profile_urls.values() if url and url.is_valid)
    accessible_profiles = sum(1 for url in profile_urls.values() if url and url.is_accessible)
    analyzed_profiles = len(profile_analyses)

    return {
        "total_profiles": total_profiles,
        "validated_profiles": validated_profiles,
        "accessible_profiles": accessible_profiles,
        "analyzed_profiles": analyzed_profiles,
        "validation_progress": validated_profiles / total_profiles if total_profiles > 0 else 0,
        "analysis_progress": analyzed_profiles / total_profiles if total_profiles > 0 else 0,
        "all_validated": validated_profiles == total_profiles and total_profiles > 0,
        "all_analyzed": analyzed_profiles == total_profiles and total_profiles > 0
    }


def render_progress_tracker(stage: str, total_stages: int = 5):
    """
    Renders a progress tracker showing the current stage in the analysis pipeline.

    Args:
        stage: Current stage ('upload', 'validation', 'extraction', 'analysis', 'results')
        total_stages: Total number of stages in the process
    """
    stage_names = {
        'upload': 'URL Input',
        'validation': 'Validation',
        'extraction': 'Data Extraction',
        'analysis': 'AI Analysis',
        'results': 'Results Display'
    }

    stage_descriptions = {
        'upload': 'Enter your profile URLs',
        'validation': 'Validate URL format and accessibility',
        'extraction': 'Extract profile data',
        'analysis': 'Analyze profile content',
        'results': 'View analysis results'
    }

    # Calculate progress
    all_stages = ['upload', 'validation', 'extraction', 'analysis', 'results']
    current_index = all_stages.index(stage) if stage in all_stages else 0
    progress = (current_index + 1) / len(all_stages)

    # Display progress bar
    st.progress(progress)

    # Display stage indicators
    cols = st.columns(len(all_stages))
    for i, s in enumerate(all_stages):
        with cols[i]:
            if i < current_index:
                # Completed stage
                st.markdown(
                    f"""<div style='text-align: center;'>
                        <div style='background-color: #28a745; color: white; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; margin: 0 auto 5px;'>
                            ✓
                        </div>
                        <small>{stage_names[s]}</small>
                    </div>""",
                    unsafe_allow_html=True
                )
            elif i == current_index:
                # Current stage
                st.markdown(
                    f"""<div style='text-align: center;'>
                        <div style='background-color: #007bff; color: white; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; margin: 0 auto 5px;'>
                            {i+1}
                        </div>
                        <small style='font-weight: bold;'>{stage_names[s]}</small>
                    </div>""",
                    unsafe_allow_html=True
                )
            else:
                # Future stage
                st.markdown(
                    f"""<div style='text-align: center;'>
                        <div style='background-color: #e9ecef; color: #6c757d; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; margin: 0 auto 5px;'>
                            {i+1}
                        </div>
                        <small>{stage_names[s]}</small>
                    </div>""",
                    unsafe_allow_html=True
                )

    # Display current stage description
    st.caption(f"**Current:** {stage_descriptions[stage]}")