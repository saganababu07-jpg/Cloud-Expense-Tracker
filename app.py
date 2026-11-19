
import streamlit as st
from auth_app import render_auth_app

st.set_page_config(
    page_title="Cloud Expense Tracker",
    page_icon="💰",
    layout="wide"
)

render_auth_app()
