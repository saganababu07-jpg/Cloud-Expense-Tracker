
import streamlit as st


def require_login():

    user = st.session_state.get("user")

    if not user:

        st.warning(
            "Please log in to access this page."
        )

        st.page_link(
            "auth_app.py",
            label="Go to Login",
            icon="🔐"
        )

        st.stop()

    return user
