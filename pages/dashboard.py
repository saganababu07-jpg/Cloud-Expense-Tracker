
import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_connection
from style import apply_style, show_header


st.set_page_config(
    page_title="Expense Dashboard",
    page_icon="📊",
    layout="wide"
)

apply_style()
show_header()

st.title("📊 Expense Dashboard")
st.write("Welcome to your financial overview!")


# Check login
if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in to access your dashboard.")
    st.stop()

user = st.session_state.user
user_id = user["user_id"]

st.markdown(f"### Hello, {user['name']}! 👋")


# Fetch financial information
connection = get_connection()

if connection:
    try:
        cursor = connection.cursor(dictionary=True)

        # Total income
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total_income
            FROM income
            WHERE user_id = %s
        """, (user_id,))

        income_result = cursor.fetchone()
        total_income = float(income_result["total_income"])

        # Total expenses
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total_expenses
            FROM expenses
            WHERE user_id = %s
        """, (user_id,))

        expense_result = cursor.fetchone()
        total_expenses = float(expense_result["total_expenses"])

        # Account balance starts at zero
        opening_balance = 0.00
        balance = opening_balance + total_income - total_expenses

        # Expense category breakdown
        cursor.execute("""
            SELECT category, SUM(amount) AS amount
            FROM expenses
            WHERE user_id = %s
            GROUP BY category
        """, (user_id,))

        category_records = cursor.fetchall()

        # Display financial metrics
        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 Total Income",
            f"₹{total_income:,.2f}"
        )

        col2.metric(
            "💸 Total Expenses",
            f"₹{total_expenses:,.2f}"
        )

        col3.metric(
            "🏦 Account Balance",
            f"₹{balance:,.2f}"
        )

        st.divider()

        # Expense distribution chart
        st.subheader("📈 Expense Distribution")

        if category_records:
            data = pd.DataFrame(category_records)

            data["amount"] = pd.to_numeric(data["amount"])

            fig = px.pie(
                data,
                names="category",
                values="amount",
                hole=0.5,
                title="Expenses by Category"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No expenses recorded yet. Add your first expense to see the chart.")

        # Financial summary
        st.divider()
        st.subheader("📋 Financial Summary")

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:
            st.metric("Starting Balance", "₹0.00")

        with summary_col2:
            st.metric("Available Balance", f"₹{balance:,.2f}")

        if balance < 0:
            st.warning("Your expenses are greater than your available income.")
        else:
            st.success("Your financial summary is up to date!")

        cursor.close()

    except Exception as e:
        st.error(f"Unable to load dashboard: {e}")

    finally:
        connection.close()

else:
    st.error("Could not connect to the database. Please check your MySQL connection.")
