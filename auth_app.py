
import streamlit as st

from style import apply_style, show_header
from auth import register_user, login_user


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Cloud Expense Tracker",
    page_icon="💰",
    layout="centered"
)


# ==========================================
# APPLY CUSTOM DESIGN
# ==========================================

apply_style()
show_header()


# ==========================================
# SESSION INITIALIZATION
# ==========================================

if "user" not in st.session_state:
    st.session_state.user = None


# ==========================================
# USER LOGIN STATUS
# ==========================================

if st.session_state.user:

    user = st.session_state.user

    st.subheader("Welcome! Manage your money smartly.")

    # Welcome message with BLACK text
    st.markdown(
        f"""
        <div style="
            background-color: #ffffff;
            color: #000000;
            padding: 12px 18px;
            border-radius: 10px;
            font-weight: 600;
            margin: 10px 0;
        ">
            Welcome, {user['name']}!
        </div>
        """,
        unsafe_allow_html=True
    )

    # User email
    st.markdown(
        f"""
        <p style="color: #ffffff;">
            <b>Email:</b> {user['email']}
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Logout button
    if st.button("Logout", use_container_width=True):

        st.session_state.user = None
        st.rerun()


# ==========================================
# LOGIN AND REGISTRATION
# ==========================================

else:

    st.subheader("Welcome! Manage your money smartly.")

    login_tab, register_tab = st.tabs(
        ["Login", "Create Account"]
    )


    # ======================================
    # LOGIN PAGE
    # ======================================

    with login_tab:

        st.subheader("Login to your account")

        with st.form("login_form"):

            email = st.text_input(
                "Email Address",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            login_button = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login_button:

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                user = login_user(
                    email.strip(),
                    password
                )

                if user:

                    st.session_state.user = user

                    st.success("Login successful!")

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )


    # ======================================
    # REGISTRATION PAGE
    # ======================================

    with register_tab:

        st.subheader("Create a new account")

        with st.form("register_form"):

            name = st.text_input(
                "Full Name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email Address",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Create Password",
                type="password",
                placeholder="Create a password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password"
            )

            register_button = st.form_submit_button(
                "Register",
                use_container_width=True
            )

        if register_button:

            if not name or not email or not password:

                st.warning(
                    "Please fill in all required fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 8:

                st.warning(
                    "Password must contain at least 8 characters."
                )

            else:

                success, message = register_user(
                    name.strip(),
                    email.strip(),
                    password
                )

                if success:

                    st.success(message)

                    st.info(
                        "You can now log in using your account."
                    )

                else:

                    st.error(message)
