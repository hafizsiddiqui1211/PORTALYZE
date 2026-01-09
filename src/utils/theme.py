"""Theme utility functions for Resume & Profile Analyzer"""
import streamlit as st

def get_theme_css(theme: str = "system") -> str:
    """
    Returns CSS for the selected theme.

    Args:
        theme: Theme to apply - "light", "dark", or "system"

    Returns:
        CSS string for the theme
    """
    if theme == "dark":
        return """
        <style>
        /* Dark theme CSS */
        html {
            color-scheme: dark;
        }

        body {
            color: #e6edf3 !important;
            background-color: #0e1117 !important;
        }

        .stApp {
            background-color: #0e1117 !important;
            color: #e6edf3 !important;
        }

        /* General text and background colors */
        .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader, .stCaption, .stCodeBlock {
            color: #e6edf3 !important;
        }

        /* Input fields */
        input, textarea, select, .stSelectbox, .stTextInput, .stTextArea {
            background-color: #0d1117 !important;
            color: #e6edf3 !important;
            border-color: #30363d !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #238636 !important;
            color: white !important;
            border: 1px solid #238636 !important;
        }

        .stButton>button:hover {
            background-color: #2ea043 !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #161b22 !important;
            color: #e6edf3 !important;
        }

        [data-testid="stSidebar"] * {
            color: #e6edf3 !important;
        }

        /* Data frames and tables */
        .stDataFrame, .stTable {
            background-color: #161b22 !important;
            border-color: #30363d !important;
        }

        /* Containers and cards */
        .stContainer, .stExpander, [data-testid="stVerticalBlock"] {
            background-color: #161b22 !important;
        }

        /* Borders */
        .st-emotion-cache-16txtl3, .st-emotion-cache-13ln4kf {
            border-color: #30363d !important;
        }

        /* Radio buttons and checkboxes */
        .stRadio, .stCheckbox {
            color: #e6edf3 !important;
        }

        /* Slider and number input */
        .stSlider, .stNumberInput {
            color: #e6edf3 !important;
        }

        /* Links */
        a {
            color: #58a6ff !important;
        }

        a:visited {
            color: #58a6ff !important;
        }

        /* Custom components with hardcoded colors */
        [style*="#f0f2f6" i] {
            background-color: #161b22 !important;
        }

        [style*="#d4edda" i] {
            background-color: #161b22 !important;
            border-color: #30363d !important;
        }

        [style*="#e8f5e8" i] {
            background-color: #161b22 !important;
            border-left-color: #2ea043 !important;
        }

        [style*="#f8d7da" i] {
            background-color: #161b22 !important;
            border-color: #30363d !important;
        }

        [style*="#c3e6cb" i] {
            border-color: #30363d !important;
        }

        [style*="#f5c6cb" i] {
            border-color: #30363d !important;
        }

        /* Text colors in custom components */
        [style*="#155724" i] {
            color: #e6edf3 !important;
        }

        [style*="#721c24" i] {
            color: #e6edf3 !important;
        }

        [style*="#dc3545" i] {
            color: #ff7b72 !important;
        }

        [style*="#fd7e14" i] {
            color: #ffa657 !important;
        }

        [style*="#ffc107" i] {
            color: #d29922 !important;
        }
        </style>
        """
    elif theme == "light":
        return """
        <style>
        /* Light theme CSS */
        html {
            color-scheme: light;
        }

        body {
            color: #212529 !important;
            background-color: #ffffff !important;
        }

        .stApp {
            background-color: #ffffff !important;
            color: #212529 !important;
        }

        /* General text and background colors */
        .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader, .stCaption, .stCodeBlock {
            color: #212529 !important;
        }

        /* Input fields */
        input, textarea, select, .stSelectbox, .stTextInput, .stTextArea {
            background-color: #ffffff !important;
            color: #212529 !important;
            border-color: #ced4da !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #0d6efd !important;
            color: white !important;
            border: 1px solid #0d6efd !important;
        }

        .stButton>button:hover {
            background-color: #0b5ed7 !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa !important;
            color: #212529 !important;
        }

        [data-testid="stSidebar"] * {
            color: #212529 !important;
        }

        /* Data frames and tables */
        .stDataFrame, .stTable {
            background-color: #ffffff !important;
            border-color: #dee2e6 !important;
        }

        /* Containers and cards */
        .stContainer, .stExpander, [data-testid="stVerticalBlock"] {
            background-color: #ffffff !important;
        }

        /* Borders */
        .st-emotion-cache-16txtl3, .st-emotion-cache-13ln4kf {
            border-color: #dee2e6 !important;
        }

        /* Radio buttons and checkboxes */
        .stRadio, .stCheckbox {
            color: #212529 !important;
        }

        /* Slider and number input */
        .stSlider, .stNumberInput {
            color: #212529 !important;
        }

        /* Links */
        a {
            color: #0d6efd !important;
        }

        a:visited {
            color: #0d6efd !important;
        }

        /* Custom components with hardcoded colors */
        [style*="#f0f2f6" i] {
            background-color: #f8f9fa !important;
        }

        [style*="#d4edda" i] {
            background-color: #d4edda !important;
            border-color: #c3e6cb !important;
        }

        [style*="#e8f5e8" i] {
            background-color: #e8f5e8 !important;
            border-left-color: #28a745 !important;
        }

        [style*="#f8d7da" i] {
            background-color: #f8d7da !important;
            border-color: #f5c6cb !important;
        }

        [style*="#c3e6cb" i] {
            border-color: #c3e6cb !important;
        }

        [style*="#f5c6cb" i] {
            border-color: #f5c6cb !important;
        }

        /* Text colors in custom components */
        [style*="#155724" i] {
            color: #155724 !important;
        }

        [style*="#721c24" i] {
            color: #721c24 !important;
        }

        [style*="#dc3545" i] {
            color: #dc3545 !important;
        }

        [style*="#fd7e14" i] {
            color: #fd7e14 !important;
        }

        [style*="#ffc107" i] {
            color: #ffc107 !important;
        }
        </style>
        """
    else:  # system theme (default behavior)
        return """
        <style>
        /* System theme follows OS preference */
        @media (prefers-color-scheme: dark) {
            html {
                color-scheme: dark;
            }

            body {
                color: #e6edf3 !important;
                background-color: #0e1117 !important;
            }

            .stApp {
                background-color: #0e1117 !important;
                color: #e6edf3 !important;
            }

            /* General text and background colors */
            .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader, .stCaption, .stCodeBlock {
                color: #e6edf3 !important;
            }

            /* Input fields */
            input, textarea, select, .stSelectbox, .stTextInput, .stTextArea {
                background-color: #0d1117 !important;
                color: #e6edf3 !important;
                border-color: #30363d !important;
            }

            /* Buttons */
            .stButton>button {
                background-color: #238636 !important;
                color: white !important;
                border: 1px solid #238636 !important;
            }

            .stButton>button:hover {
                background-color: #2ea043 !important;
            }

            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #161b22 !important;
                color: #e6edf3 !important;
            }

            [data-testid="stSidebar"] * {
                color: #e6edf3 !important;
            }

            /* Data frames and tables */
            .stDataFrame, .stTable {
                background-color: #161b22 !important;
                border-color: #30363d !important;
            }

            /* Containers and cards */
            .stContainer, .stExpander, [data-testid="stVerticalBlock"] {
                background-color: #161b22 !important;
            }

            /* Borders */
            .st-emotion-cache-16txtl3, .st-emotion-cache-13ln4kf {
                border-color: #30363d !important;
            }

            /* Radio buttons and checkboxes */
            .stRadio, .stCheckbox {
                color: #e6edf3 !important;
            }

            /* Slider and number input */
            .stSlider, .stNumberInput {
                color: #e6edf3 !important;
            }

            /* Links */
            a {
                color: #58a6ff !important;
            }

            a:visited {
                color: #58a6ff !important;
            }

            /* Custom components with hardcoded colors */
            [style*="#f0f2f6" i] {
                background-color: #161b22 !important;
            }

            [style*="#d4edda" i] {
                background-color: #161b22 !important;
                border-color: #30363d !important;
            }

            [style*="#e8f5e8" i] {
                background-color: #161b22 !important;
                border-left-color: #2ea043 !important;
            }

            [style*="#f8d7da" i] {
                background-color: #161b22 !important;
                border-color: #30363d !important;
            }

            [style*="#c3e6cb" i] {
                border-color: #30363d !important;
            }

            [style*="#f5c6cb" i] {
                border-color: #30363d !important;
            }

            /* Text colors in custom components */
            [style*="#155724" i] {
                color: #e6edf3 !important;
            }

            [style*="#721c24" i] {
                color: #e6edf3 !important;
            }

            [style*="#dc3545" i] {
                color: #ff7b72 !important;
            }

            [style*="#fd7e14" i] {
                color: #ffa657 !important;
            }

            [style*="#ffc107" i] {
                color: #d29922 !important;
            }
        }

        @media (prefers-color-scheme: light) {
            html {
                color-scheme: light;
            }

            body {
                color: #212529 !important;
                background-color: #ffffff !important;
            }

            .stApp {
                background-color: #ffffff !important;
                color: #212529 !important;
            }

            /* General text and background colors */
            .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader, .stCaption, .stCodeBlock {
                color: #212529 !important;
            }

            /* Input fields */
            input, textarea, select, .stSelectbox, .stTextInput, .stTextArea {
                background-color: #ffffff !important;
                color: #212529 !important;
                border-color: #ced4da !important;
            }

            /* Buttons */
            .stButton>button {
                background-color: #0d6efd !important;
                color: white !important;
                border: 1px solid #0d6efd !important;
            }

            .stButton>button:hover {
                background-color: #0b5ed7 !important;
            }

            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #f8f9fa !important;
                color: #212529 !important;
            }

            [data-testid="stSidebar"] * {
                color: #212529 !important;
            }

            /* Data frames and tables */
            .stDataFrame, .stTable {
                background-color: #ffffff !important;
                border-color: #dee2e6 !important;
            }

            /* Containers and cards */
            .stContainer, .stExpander, [data-testid="stVerticalBlock"] {
                background-color: #ffffff !important;
            }

            /* Borders */
            .st-emotion-cache-16txtl3, .st-emotion-cache-13ln4kf {
                border-color: #dee2e6 !important;
            }

            /* Radio buttons and checkboxes */
            .stRadio, .stCheckbox {
                color: #212529 !important;
            }

            /* Slider and number input */
            .stSlider, .stNumberInput {
                color: #212529 !important;
            }

            /* Links */
            a {
                color: #0d6efd !important;
            }

            a:visited {
                color: #0d6efd !important;
            }

            /* Custom components with hardcoded colors */
            [style*="#f0f2f6" i] {
                background-color: #f8f9fa !important;
            }

            [style*="#d4edda" i] {
                background-color: #d4edda !important;
                border-color: #c3e6cb !important;
            }

            [style*="#e8f5e8" i] {
                background-color: #e8f5e8 !important;
                border-left-color: #28a745 !important;
            }

            [style*="#f8d7da" i] {
                background-color: #f8d7da !important;
                border-color: #f5c6cb !important;
            }

            [style*="#c3e6cb" i] {
                border-color: #c3e6cb !important;
            }

            [style*="#f5c6cb" i] {
                border-color: #f5c6cb !important;
            }

            /* Text colors in custom components */
            [style*="#155724" i] {
                color: #155724 !important;
            }

            [style*="#721c24" i] {
                color: #721c24 !important;
            }

            [style*="#dc3545" i] {
                color: #dc3545 !important;
            }

            [style*="#fd7e14" i] {
                color: #fd7e14 !important;
            }

            [style*="#ffc107" i] {
                color: #ffc107 !important;
            }
        }
        </style>
        """

def apply_theme():
    """
    Apply the selected theme to the Streamlit app.
    This should be called early in the app to ensure theme is applied.
    """
    # Get the current theme from session state, default to 'system'
    current_theme = st.session_state.get('theme', 'system')

    # Apply the CSS for the selected theme
    css = get_theme_css(current_theme)
    st.markdown(css, unsafe_allow_html=True)