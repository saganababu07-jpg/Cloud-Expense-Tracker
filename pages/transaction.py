
import streamlit as st
import pandas as pd

from database import get_connection
from style import apply_style, show_header
from auth_guard import require_login


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Transaction History",
    page_icon="🧾",
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

st.title("🧾 Transaction History")

st.write(
    "View your income and expense transactions."
)

st.markdown(
    f"""
    <h4 style="color: black; font-weight: bold;">
        Logged in as {user['name']}
    </h4>
    """,
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# DATABASE CONNECTION
# ==========================================

connection = get_connection()

if connection:

    try:

        cursor = connection.cursor(dictionary=True)

        # ==================================
        # FETCH EXPENSES
        # ==================================

        cursor.execute(
            """
            SELECT
                expense_date AS transaction_date,
                category AS description,
                amount,
                'Expense' AS transaction_type
            FROM expenses
            WHERE user_id = %s
            """,
            (user_id,)
        )

        expense_records = cursor.fetchall()

        # ==================================
        # FETCH INCOME
        # ==================================

        cursor.execute(
            """
            SELECT
                income_date AS transaction_date,
                source AS description,
                amount,
                'Income' AS transaction_type
            FROM income
            WHERE user_id = %s
            """,
            (user_id,)
        )

        income_records = cursor.fetchall()

        cursor.close()

        # ==================================
        # COMBINE TRANSACTIONS
        # ==================================

        all_records = (
            expense_records + income_records
        )

        if all_records:

            df = pd.DataFrame(all_records)

            df["transaction_date"] = pd.to_datetime(
                df["transaction_date"]
            )

            df["amount"] = pd.to_numeric(
                df["amount"]
            )

            df = df.sort_values(
                by="transaction_date",
                ascending=False
            )

            # ==================================
            # FILTERS
            # ==================================

            st.subheader("🔍 Filter Transactions")

            col1, col2 = st.columns(2)

            with col1:

                transaction_filter = st.selectbox(
                    "Transaction Type",
                    [
                        "All",
                        "Income",
                        "Expense"
                    ]
                )

            with col2:

                search = st.text_input(
                    "Search Description"
                )

            filtered_df = df.copy()

            if transaction_filter != "All":

                filtered_df = filtered_df[
                    filtered_df["transaction_type"]
                    == transaction_filter
                ]

            if search:

                filtered_df = filtered_df[
                    filtered_df["description"].str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ]

            # ==================================
            # SUMMARY
            # ==================================

            st.divider()

            total_income = df.loc[
                df["transaction_type"] == "Income",
                "amount"
            ].sum()

            total_expenses = df.loc[
                df["transaction_type"] == "Expense",
                "amount"
            ].sum()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Income",
                f"₹{total_income:,.2f}"
            )

            col2.metric(
                "Total Expenses",
                f"₹{total_expenses:,.2f}"
            )

            col3.metric(
                "Net Balance",
                f"₹{total_income - total_expenses:,.2f}"
            )

            st.divider()

            # ==================================
            # TRANSACTION TABLE
            # ==================================

            st.subheader("📋 All Transactions")

            display_df = filtered_df.rename(
                columns={
                    "transaction_date": "Date",
                    "description": "Description",
                    "amount": "Amount",
                    "transaction_type": "Type"
                }
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            # ==================================
            # TRANSACTION SUMMARY
            # ==================================

            st.divider()

            col1, col2 = st.columns(2)

            col1.metric(
                "Total Transactions",
                len(filtered_df)
            )

            col2.metric(
                "Filtered Amount",
                f"₹{filtered_df['amount'].sum():,.2f}"
            )

            # ==================================
            # DOWNLOAD TRANSACTIONS
            # ==================================

            csv = display_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📥 Download Transactions CSV",
                data=csv,
                file_name="transactions.csv",
                mime="text/csv"
            )

        else:

            st.info(
                "No transactions found. "
                "Start by adding income or expenses."
            )

    except Exception as e:

        st.error(
            f"Unable to retrieve transactions: {e}"
        )

    finally:

        connection.close()

else:

    st.error(
        "Could not connect to Aiven MySQL."
    )


st.divider()

st.caption(
    "Cloud Expense Tracker | Transaction Management"
)
