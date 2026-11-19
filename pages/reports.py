
import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_connection
from style import apply_style, show_header
from auth_guard import require_login


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Expense Reports",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# AUTHENTICATION
# ==========================================

user = require_login()
user_id = user["user_id"]


# ==========================================
# DESIGN
# ==========================================

apply_style()
show_header()

st.title("📊 Expense Reports")

st.write(
    "Analyze your spending habits and financial activities."
)

st.markdown(
    f"""
    <h4 style="color: black; font-weight: bold;">
        Welcome, {user['name']}!
    </h4>
    """,
    unsafe_allow_html=True
)

# ==========================================
# FETCH REAL EXPENSE DATA
# ==========================================

connection = get_connection()

if connection:

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT expense_date, category, amount, description
            FROM expenses
            WHERE user_id = %s
            ORDER BY expense_date DESC
            """,
            (user_id,)
        )

        records = cursor.fetchall()

        cursor.close()

        if records:

            df = pd.DataFrame(records)

            df["expense_date"] = pd.to_datetime(
                df["expense_date"]
            )

            df["amount"] = pd.to_numeric(
                df["amount"]
            )

            # ==================================
            # FINANCIAL SUMMARY
            # ==================================

            st.subheader("💰 Financial Summary")

            total_expense = df["amount"].sum()
            average_expense = df["amount"].mean()
            highest_expense = df["amount"].max()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Expenses",
                f"₹{total_expense:,.2f}"
            )

            col2.metric(
                "Average Expense",
                f"₹{average_expense:,.2f}"
            )

            col3.metric(
                "Highest Expense",
                f"₹{highest_expense:,.2f}"
            )

            st.divider()

            # ==================================
            # CATEGORY-WISE REPORT
            # ==================================

            st.subheader("📌 Category-wise Spending")

            category_data = (
                df.groupby("category")["amount"]
                .sum()
                .reset_index()
            )

            fig1 = px.pie(
                category_data,
                names="category",
                values="amount",
                hole=0.45,
                title="Expense Distribution"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            st.divider()

            # ==================================
            # DAILY EXPENSE ANALYSIS
            # ==================================

            st.subheader("📅 Daily Spending Analysis")

            daily_data = (
                df.groupby("expense_date")["amount"]
                .sum()
                .reset_index()
            )

            fig2 = px.bar(
                daily_data,
                x="expense_date",
                y="amount",
                title="Daily Expenses",
                labels={
                    "expense_date": "Date",
                    "amount": "Amount (₹)"
                }
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            st.divider()

            # ==================================
            # CATEGORY COMPARISON
            # ==================================

            st.subheader("📈 Category Comparison")

            fig3 = px.bar(
                category_data,
                x="category",
                y="amount",
                color="category",
                title="Total Spending by Category"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

            st.divider()

            # ==================================
            # EXPENSE RECORDS
            # ==================================

            st.subheader("📋 Expense Records")

            display_df = df.rename(
                columns={
                    "expense_date": "Date",
                    "category": "Category",
                    "amount": "Amount",
                    "description": "Description"
                }
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            # ==================================
            # DOWNLOAD REPORT
            # ==================================

            csv = display_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📥 Download Expense Report",
                data=csv,
                file_name="expense_report.csv",
                mime="text/csv"
            )

        else:

            st.info(
                "No expense records found. "
                "Add your first expense to generate reports."
            )

    except Exception as e:

        st.error(f"Unable to load expense reports: {e}")

    finally:

        connection.close()

else:

    st.error(
        "Database connection failed. "
        "Please check your Aiven MySQL connection."
    )


st.divider()

st.caption(
    "Cloud Expense Tracker | Personal Financial Reports"
)
