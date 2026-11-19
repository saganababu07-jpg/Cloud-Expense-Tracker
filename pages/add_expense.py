
import streamlit as st
from style import apply_style, show_header
from database import get_connection
from datetime import date
from decimal import Decimal

st.set_page_config(
    page_title="Add Expense",
    page_icon="💸",
    layout="centered"
)

apply_style()
show_header()


st.title("💸 Add New Expense")
st.write("Record and manage your daily expenses.")

from auth_guard import require_login

user = require_login()

st.markdown(
    f"""
    <h3 style="color: black;">
        Successfully logged in as {user['name']}!
    </h3>
    """,
    unsafe_allow_html=True
)

# Expense categories
categories = [
    "Food",
    "Shopping",
    "Transportation",
    "Education",
    "Entertainment",
    "Healthcare",
    "Bills",
    "Travel",
    "Others"
]

# Expense form
with st.form("expense_form"):

    st.subheader("Expense Details")

    category = st.selectbox(
        "Select Category",
        categories
    )

    amount = st.number_input(
        "Expense Amount (₹)",
        min_value=0.0,
        step=10.0,
        format="%.2f"
    )

    expense_date = st.date_input(
        "Expense Date",
        value=date.today()
    )

    description = st.text_area(
        "Description",
        placeholder="Enter expense details..."
    )

    submit = st.form_submit_button(
        "Save Expense",
        use_container_width=True
    )

# Save expense to MySQL
if submit:

    if amount <= 0:
        st.error("Please enter an amount greater than zero.")

    else:

        connection = get_connection()

        if connection:

            cursor = None

            try:
                cursor = connection.cursor()

                query = """
                    INSERT INTO expenses
                    (user_id, category, amount, description, expense_date)
                    VALUES (%s, %s, %s, %s, %s)
                """

                values = (
                    user["user_id"],
                    category,
                    Decimal(str(amount)),
                    description.strip(),
                    expense_date
                )

                cursor.execute(query, values)
                connection.commit()

                st.success("Expense saved successfully!")
                st.balloons()

            except Exception as e:
                connection.rollback()
                st.error(f"Unable to save expense: {e}")

            finally:
                if cursor:
                    cursor.close()
                connection.close()
