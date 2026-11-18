
import streamlit as st

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Cloud-Based Expense Tracker")

st.success("Welcome! Your application is running successfully.")

st.subheader("My Financial Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Income", "₹15,000")
col2.metric("Total Expenses", "₹9,000")
col3.metric("Balance", "₹6,000")

st.divider()

st.write("Your Expense Tracker is ready!")

st.balloons()

