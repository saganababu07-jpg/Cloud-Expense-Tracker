
import streamlit as st
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=st.secrets["mysql"]["port"],
            ssl_ca="ca.pem",
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )

        if connection.is_connected():
            return connection

    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None
