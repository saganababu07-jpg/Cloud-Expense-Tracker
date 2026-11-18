import streamlit as st
from database import get_connection

st.title("Cloud Expense Tracker")
st.subheader("MySQL Database Connection")

connection = get_connection()

if connection:
    st.success("Successfully connected to MySQL!")

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")

    tables = cursor.fetchall()

    st.write("Tables in expense_tracker:")

    for table in tables:
        st.write("✅", table[0])

    cursor.close()
    connection.close()

else:
    st.error("MySQL connection failed.")