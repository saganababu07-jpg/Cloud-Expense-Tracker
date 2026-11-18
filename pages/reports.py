from style import apply_style, show_header
import streamlit as st
import pandas as pd
import plotly.express as px
apply_style()
show_header()
st.title("📊 Expense Reports")

st.write("Analyze your spending habits and financial activities.")

# Sample data
data = {
    "Date": [
        "2026-11-01",
        "2026-11-03",
        "2026-11-05",
        "2026-11-08",
        "2026-11-10",
        "2026-11-12",
        "2026-11-15"
    ],
    "Category": [
        "Food", "Travel", "Shopping",
        "Education", "Food", "Bills", "Travel"
    ],
    "Amount": [250, 150, 1500, 2000, 350, 800, 200]
}

df = pd.DataFrame(data)

df["Date"] = pd.to_datetime(df["Date"])

# Financial summary
st.subheader("Financial Summary")

total_expense = df["Amount"].sum()
average_expense = df["Amount"].mean()
highest_expense = df["Amount"].max()

col1, col2, col3 = st.columns(3)

col1.metric("Total Expenses", f"₹{total_expense:,.2f}")
col2.metric("Average Expense", f"₹{average_expense:,.2f}")
col3.metric("Highest Expense", f"₹{highest_expense:,.2f}")

st.divider()

# Category-wise report
st.subheader("Category-wise Spending")

category_data = (
    df.groupby("Category")["Amount"]
    .sum()
    .reset_index()
)

fig1 = px.pie(
    category_data,
    names="Category",
    values="Amount",
    hole=0.45,
    title="Expense Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

# Daily expense report
st.subheader("Daily Spending Analysis")

daily_data = (
    df.groupby("Date")["Amount"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    daily_data,
    x="Date",
    y="Amount",
    title="Daily Expenses",
    labels={"Amount": "Amount (₹)"}
)

st.plotly_chart(fig2, use_container_width=True)

# Category comparison
st.subheader("Category Comparison")

fig3 = px.bar(
    category_data,
    x="Category",
    y="Amount",
    color="Category",
    title="Total Spending by Category"
)

st.plotly_chart(fig3, use_container_width=True)

# Download report
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Expense Report",
    data=csv,
    file_name="expense_report.csv",
    mime="text/csv"
)
