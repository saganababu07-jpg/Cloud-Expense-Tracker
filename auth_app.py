
import streamlit as st
import html

from style import apply_style, show_header
from auth import register_user, login_user


def render_auth_app():

    apply_style()
    show_header()

    # Initialize login session
    if "user" not in st.session_state:
        st.session_state.user = None

    # ==================================
    # HOME PAGE AFTER LOGIN
    # ==================================

    if st.session_state.user:

        user = st.session_state.user
        safe_name = html.escape(str(user["name"]))

        st.title("🏠 Welcome to Your Expense Tracker!")

        st.markdown(
    f"""
    <h3 style="color: black; font-weight: bold;">
        Successfully logged in as {safe_name}!
    </h3>
    """,
    unsafe_allow_html=True
)

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(120deg,#5426cc,#4134c7);
                padding: 28px;
                border-radius: 16px;
                color: white;
                margin: 15px 0;
            ">
                <h1 style="color:white;">
                    Hello, {safe_name}! 👋
                </h1>
                <h3 style="color:white;">
                    Welcome to Your Financial Space
                </h3>
                <p style="color:white;">
                    Track your money. Manage your future.
                    Make smarter financial decisions every day.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # About application
        st.header("🌟 About Our Application")

        st.write(
            """
            Cloud Expense Tracker is a personal financial
            management application designed to help you
            record income, manage daily expenses, monitor
            transactions and understand your spending habits.

            Manage your finances in one place with interactive
            dashboards, financial reports and secure
            cloud-based data storage.
            """
        )

        st.divider()

        # Motivational quote
        st.subheader("💡 Today's Financial Motivation")

        st.markdown(
    """
    <h4 style="color: black; font-weight: bold;">
        "Do not save what is left after spending,
        but spend what is left after saving."
    </h4>
    """,
    unsafe_allow_html=True
)
        st.divider()

        # Feature cards
        st.header("🚀 Explore Your Application")

        st.write(
            "Choose a feature below to manage your finances."
        )

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.subheader("💸 Add Expense")
                st.write(
                    "Record and manage your daily spending."
                )
                st.page_link(
                    "pages/add_expense.py",
                    label="Add Expense",
                    icon="💸",
                    use_container_width=True
                )

        with col2:
            with st.container(border=True):
                st.subheader("💰 Add Income")
                st.write(
                    "Record salary and other income sources."
                )
                st.page_link(
                    "pages/add_income.py",
                    label="Add Income",
                    icon="💰",
                    use_container_width=True
                )

        col3, col4 = st.columns(2)

        with col3:
            with st.container(border=True):
                st.subheader("🧾 Transactions")
                st.write(
                    "View and manage your transactions."
                )
                st.page_link(
                    "pages/transaction.py",
                    label="View Transactions",
                    icon="🧾",
                    use_container_width=True
                )

        with col4:
            with st.container(border=True):
                st.subheader("📊 Dashboard")
                st.write(
                    "Monitor income, expenses and balance."
                )
                st.page_link(
                    "pages/dashboard.py",
                    label="Open Dashboard",
                    icon="📊",
                    use_container_width=True
                )

        col5, col6 = st.columns(2)

        with col5:
            with st.container(border=True):
                st.subheader("📈 Reports")
                st.write(
                    "Analyze your financial activities."
                )
                st.page_link(
                    "pages/reports.py",
                    label="View Reports",
                    icon="📈",
                    use_container_width=True
                )

        st.divider()

        # Logout
        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            st.session_state.user = None
            st.rerun()

    # ==================================
    # LOGIN AND REGISTRATION
    # ==================================

    else:

        st.title("Welcome! Manage Your Money Smartly.")

        login_tab, register_tab = st.tabs(
            ["Login", "Create Account"]
        )

        with login_tab:

            st.subheader("Login to Your Account")

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

        with register_tab:

            st.subheader("Create a New Account")

            with st.form("register_form"):

                name = st.text_input("Full Name")

                email = st.text_input("Email Address")

                password = st.text_input(
                    "Create Password",
                    type="password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password"
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
                    st.error("Passwords do not match.")

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
render_auth_app()