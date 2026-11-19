
import streamlit as st


def require_login():

    user = st.session_state.get("user")

    if not user:

        st.warning(
            "Please log in to access this page."
        )

        if st.button("🔐 Go to Login"):
            st.switch_page("auth_app.py")

        st.stop()

    return user
