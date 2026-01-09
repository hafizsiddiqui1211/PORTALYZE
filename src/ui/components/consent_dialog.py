"""Consent dialog component for requesting user consent for data processing"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Callable, Any


class ConsentDialog:
    """UI component for requesting and managing user consent for data processing"""

    def __init__(self):
        pass

    def render(self,
               session_id: str,
               data_description: str = "your resume and profile data",
               on_consent_granted: Optional[Callable] = None,
               on_consent_denied: Optional[Callable] = None,
               key_prefix: str = "consent_dialog") -> bool:
        """
        Render a consent dialog requesting permission to process user data.

        Args:
            session_id: Unique session identifier
            data_description: Description of the data being processed
            on_consent_granted: Callback function when consent is granted
            on_consent_denied: Callback function when consent is denied
            key_prefix: Prefix for Streamlit widget keys to ensure uniqueness

        Returns:
            bool: True if consent was granted, False otherwise
        """
        consent_key = f"{key_prefix}_consent_{session_id}"
        timestamp_key = f"{key_prefix}_timestamp_{session_id}"

        # Check if consent was already given in this session
        if st.session_state.get(consent_key, False):
            return True

        # Display the consent dialog
        with st.container():
            st.markdown(
                """
                <div style="
                    border: 2px solid #3498db;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                    background-color: #f8f9fa;
                ">
                    <h3 style="color: #2980b9; margin-top: 0;">Data Processing Consent</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Consent explanation
            st.markdown(
                f"""
                <div style="margin: 15px 0;">
                    <p><strong>We need your consent to process {data_description}.</strong></p>

                    <h4>What we store:</h4>
                    <ul>
                        <li>Uploaded resume content (text only)</li>
                        <li>Profile analysis results</li>
                        <li>Role recommendations generated</li>
                        <li>Temporary session data</li>
                    </ul>

                    <h4>Why we store it:</h4>
                    <ul>
                        <li>To generate role recommendations for you</li>
                        <li>To provide personalized insights</li>
                        <li>To improve our recommendation accuracy</li>
                    </ul>

                    <h4>How long we keep it:</h4>
                    <ul>
                        <li>All data is automatically deleted after 24 hours</li>
                        <li>You can request deletion at any time</li>
                        <li>No permanent storage of your personal data</li>
                    </ul>

                    <h4>Your rights:</h4>
                    <ul>
                        <li>You can withdraw consent at any time</li>
                        <li>You can request deletion of your data</li>
                        <li>You can ask questions about data processing</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Consent buttons
            col1, col2 = st.columns(2)

            with col1:
                consent_granted = st.button(
                    "✅ I Consent",
                    key=f"{consent_key}_grant",
                    type="primary"
                )

            with col2:
                consent_denied = st.button(
                    "❌ Decline Consent",
                    key=f"{consent_key}_deny",
                    type="secondary"
                )

            # Handle consent decisions
            if consent_granted:
                st.session_state[consent_key] = True
                st.session_state[timestamp_key] = datetime.now().isoformat()

                # Show success message
                st.success("Thank you for granting consent! Your data will be processed securely.")

                # Call the callback if provided
                if on_consent_granted:
                    on_consent_granted()

                return True

            elif consent_denied:
                st.session_state[consent_key] = False
                st.session_state[timestamp_key] = datetime.now().isoformat()

                # Show information message
                st.info("Consent declined. We cannot process your data without consent.")

                # Call the callback if provided
                if on_consent_denied:
                    on_consent_denied()

                return False

            # If no decision made yet, return False
            return False

    def render_consent_status(self, session_id: str, key_prefix: str = "consent_status"):
        """
        Render the current consent status for a session.

        Args:
            session_id: Unique session identifier
            key_prefix: Prefix for Streamlit widget keys
        """
        consent_key = f"{key_prefix}_consent_{session_id}"
        timestamp_key = f"{key_prefix}_timestamp_{session_id}"

        consent_given = st.session_state.get(consent_key, None)

        if consent_given is None:
            st.info("Consent has not been requested yet.")
        elif consent_given:
            timestamp_str = st.session_state.get(timestamp_key, "Unknown")
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                st.success(f"✅ Consent granted on {timestamp.strftime('%Y-%m-%d %H:%M')}")
            except:
                st.success("✅ Consent granted")
        else:
            timestamp_str = st.session_state.get(timestamp_key, "Unknown")
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                st.warning(f"❌ Consent declined on {timestamp.strftime('%Y-%m-%d %H:%M')}")
            except:
                st.warning("❌ Consent declined")

    def has_consent(self, session_id: str, key_prefix: str = "consent_check") -> bool:
        """
        Check if consent has been granted for a session.

        Args:
            session_id: Unique session identifier
            key_prefix: Prefix for Streamlit widget keys

        Returns:
            bool: True if consent was granted, False otherwise
        """
        consent_key = f"{key_prefix}_consent_{session_id}"
        return st.session_state.get(consent_key, False)

    def revoke_consent(self, session_id: str, key_prefix: str = "consent_revoke"):
        """
        Revoke consent for a session.

        Args:
            session_id: Unique session identifier
            key_prefix: Prefix for Streamlit widget keys
        """
        consent_key = f"{key_prefix}_consent_{session_id}"
        timestamp_key = f"{key_prefix}_timestamp_{session_id}"

        st.session_state[consent_key] = False
        st.session_state[timestamp_key] = datetime.now().isoformat()

        st.success("Consent has been revoked. Your data will not be processed.")

    def render_consent_management(self, session_id: str, key_prefix: str = "consent_management"):
        """
        Render a comprehensive consent management interface.

        Args:
            session_id: Unique session identifier
            key_prefix: Prefix for Streamlit widget keys
        """
        # Display current status
        self.render_consent_status(session_id, f"{key_prefix}_status")

        # If consent was given, provide option to revoke
        if self.has_consent(session_id, f"{key_prefix}_check"):
            if st.button("Revoke Consent", key=f"{key_prefix}_revoke_btn"):
                self.revoke_consent(session_id, f"{key_prefix}_revoke")

        # If consent was not given, provide option to request again
        else:
            current_consent = st.session_state.get(f"{key_prefix}_consent_{session_id}", None)
            if current_consent is False:  # Consent was explicitly denied
                if st.button("Request Consent Again", key=f"{key_prefix}_request_again"):
                    # Reset the consent state to None to allow requesting again
                    st.session_state[f"{key_prefix}_consent_{session_id}"] = None

    def render_inline_consent(self,
                           session_id: str,
                           consent_text: str = "I consent to having my data processed for role recommendations",
                           key_prefix: str = "inline_consent") -> bool:
        """
        Render an inline consent checkbox.

        Args:
            session_id: Unique session identifier
            consent_text: Text to display next to the consent checkbox
            key_prefix: Prefix for Streamlit widget keys

        Returns:
            bool: True if consent was granted, False otherwise
        """
        consent_key = f"{key_prefix}_consent_{session_id}"

        # Check if consent was already given
        if st.session_state.get(consent_key, False):
            return True

        # Create inline consent checkbox
        consent_given = st.checkbox(
            consent_text,
            key=f"{consent_key}_checkbox",
            value=st.session_state.get(consent_key, False)
        )

        if consent_given:
            st.session_state[consent_key] = True
            st.session_state[f"{key_prefix}_timestamp_{session_id}"] = datetime.now().isoformat()

        return consent_given


def show_consent_dialog(session_id: str,
                        data_description: str = "your resume and profile data",
                        on_consent_granted: Optional[Callable] = None,
                        on_consent_denied: Optional[Callable] = None,
                        key_prefix: str = "consent_dialog") -> bool:
    """
    Convenience function to show a consent dialog in a Streamlit app.

    Args:
        session_id: Unique session identifier
        data_description: Description of the data being processed
        on_consent_granted: Callback function when consent is granted
        on_consent_denied: Callback function when consent is denied
        key_prefix: Prefix for Streamlit widget keys

    Returns:
        bool: True if consent was granted, False otherwise
    """
    dialog = ConsentDialog()
    return dialog.render(session_id, data_description, on_consent_granted, on_consent_denied, key_prefix)


def show_consent_status(session_id: str, key_prefix: str = "consent_status"):
    """
    Convenience function to show consent status in a Streamlit app.

    Args:
        session_id: Unique session identifier
        key_prefix: Prefix for Streamlit widget keys
    """
    dialog = ConsentDialog()
    dialog.render_consent_status(session_id, key_prefix)


def check_consent(session_id: str, key_prefix: str = "consent_check") -> bool:
    """
    Convenience function to check if consent has been granted.

    Args:
        session_id: Unique session identifier
        key_prefix: Prefix for Streamlit widget keys

    Returns:
        bool: True if consent was granted, False otherwise
    """
    dialog = ConsentDialog()
    return dialog.has_consent(session_id, key_prefix)