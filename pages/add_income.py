
import streamlit as st
from database import get_connection
from style import apply_style, show_header
from datetime import date
from decimal import Decimal
import html


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Add Income | Cloud Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# -----------------------------------
# APPLY COMMON DESIGN
# -----------------------------------

apply_style()
show_header()


# -----------------------------------
# LOGIN AUTHENTICATION
# -----------------------------------

from auth_guard import require_login

user = require_login()
user_name = html.escape(str(user["name"]))


# -----------------------------------
# PAGE HEADER
# -----------------------------------

st.title("💰 Add New Income")


# Welcome message - BLACK TEXT

st.markdown(
    f"""
    <div style="
        background-color: #ffffff;
        color: #000000;
        padding: 14px 18px;
        border-radius: 10px;
        margin: 10px 0;
        font-weight: 600;
        font-size: 16px;
    ">
        Logged in as {user_name}! Record your earnings below.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# -----------------------------------
# INCOME SUMMARY INFORMATION
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Income Tracking",
        value="Active",
        delta="Ready to record"
    )

with col2:
    st.metric(
        label="Database",
        value="Connected",
        delta="MySQL"
    )

with col3:
    st.metric(
        label="Account",
        value="Verified",
        delta="Logged in"
    )

st.divider()


# -----------------------------------
# INCOME CATEGORIES
# -----------------------------------

income_sources = [
    "Salary",
    "Freelance",
    "Business",
    "Investment",
    "Part-time Job",
    "Rental Income",
    "Gift",
    "Other"
]


# -----------------------------------
# INCOME ENTRY FORM
# -----------------------------------

st.subheader("📝 Income Details")

with st.form("income_form", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox(
            "Income Source",
            income_sources
        )

    with col2:
        amount = st.number_input(
            "Income Amount (₹)",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

    income_date = st.date_input(
        "Income Date",
        value=date.today(),
        max_value=date.today()
    )

    st.markdown("### 💡 Additional Information")

    notes = st.text_input(
        "Notes (Optional)",
        placeholder="Example: Monthly salary, freelance project..."
    )

    submit = st.form_submit_button(
        "💰 Save Income",
        use_container_width=True
    )


# -----------------------------------
# SAVE INCOME TO MYSQL
# -----------------------------------

if submit:

    if amount <= 0:

        st.error(
            "Please enter an income amount greater than zero."
        )

    else:

        connection = get_connection()

        if connection:

            cursor = None

            try:

                cursor = connection.cursor()

                query = """
                    INSERT INTO income
                    (user_id, source, amount, income_date)
                    VALUES (%s, %s, %s, %s)
                """

                values = (
                    user["user_id"],
                    source,
                    Decimal(str(amount)),
                    income_date
                )

                cursor.execute(query, values)

                connection.commit()

                st.success(
                    "Income successfully saved to MySQL!"
                )

                st.balloons()

                safe_source = html.escape(source)
                safe_notes = html.escape(
                    notes if notes else "No additional notes"
                )

                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(
                            110deg, #065f46, #047857
                        );
                        padding: 22px;
                        border-radius: 15px;
                        margin-top: 15px;
                    ">
                        <h3 style="color:white;">
                            ✅ Income Recorded Successfully!
                        </h3>

                        <h2 style="color:#a7f3d0;">
                            ₹{amount:,.2f}
                        </h2>

                        <p style="color:white;">
                            Source: {safe_source}<br>
                            Date: {income_date.strftime('%d-%m-%Y')}<br>
                            Notes: {safe_notes}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:

                connection.rollback()

                st.error(f"Unable to save income: {e}")

            finally:

                if cursor:
                    cursor.close()

                connection.close()


# -----------------------------------
# RECENT INCOME HISTORY
# -----------------------------------

st.divider()

st.subheader("📊 Recent Income Records")

if st.button("🔄 Refresh Income History"):

    connection = get_connection()

    if connection:

        cursor = None

        try:

            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT source, amount, income_date
                FROM income
                WHERE user_id = %s
                ORDER BY income_date DESC, income_id DESC
                LIMIT 10
                """,
                (user["user_id"],)
            )

            records = cursor.fetchall()

            if records:

                st.dataframe(
                    records,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info("No income records found yet.")

        except Exception as e:

            st.error(
                f"Unable to retrieve income history: {e}"
            )

        finally:

            if cursor:
                cursor.close()

            connection.close()


# -----------------------------------
# FOOTER
# -----------------------------------

st.caption(
    "Cloud Expense Tracker | Secure Income Management"
)
