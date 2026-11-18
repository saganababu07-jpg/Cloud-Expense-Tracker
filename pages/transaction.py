from style import apply_style, show_header
import streamlit as st
import pandas as pd
apply_style()
show_header()
st.set_page_config(page_title="Transactions", page_icon="🧾")

st.title("🧾 Transaction History")
st.write("View and manage your financial transactions.")

# Sample transaction data
data = {
    "Date": [
        "2026-11-01",
        "2026-11-03",
        "2026-11-05",
        "2026-11-08",
        "2026-11-10",
        "2026-11-12"
    ],
    "Category": [
        "Food", "Travel", "Shopping",
        "Education", "Food", "Bills"
    ],
    "Description": [
        "Lunch", "Bus Ticket", "Clothes",
        "Course Fee", "Dinner", "Electricity"
    ],
    "Amount": [250, 150, 1500, 2000, 350, 800]
}

df = pd.DataFrame(data)

df["Date"] = pd.to_datetime(df["Date"])

# Filters
st.subheader("Filter Transactions")

col1, col2 = st.columns(2)

with col1:
    category = st.selectbox(
        "Select Category",
        ["All"] + list(df["Category"].unique())
    )

with col2:
    search = st.text_input("Search Description")

filtered_df = df.copy()

if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if search:
    filtered_df = filtered_df[
        filtered_df["Description"].str.contains(
            search, case=False, na=False
        )
    ]

# Summary
st.divider()

col1, col2 = st.columns(2)

col1.metric("Total Transactions", len(filtered_df))

col2.metric(
    "Total Spending",
    f"₹{filtered_df['Amount'].sum():,.2f}"
)

# Display transactions
st.subheader("All Transactions")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# Download CSV
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Transactions CSV",
    data=csv,
    file_name="transactions.csv",
    mime="text/csv"
)
