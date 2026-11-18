
import streamlit as st


# ==========================================
# GLOBAL APPLICATION STYLING
# ==========================================

def apply_style():

    st.markdown("""
    <style>

    /* =====================================
       MAIN APPLICATION BACKGROUND
    ===================================== */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, #312e81 0%, transparent 35%),
            radial-gradient(circle at 90% 90%, #581c87 0%, transparent 35%),
            linear-gradient(135deg, #0f172a, #111827, #1e1b4b);

        color: #f8fafc;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }


    /* =====================================
       SIDEBAR
    ===================================== */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827,
            #1e1b4b
        );

        border-right: 1px solid rgba(255,255,255,0.12);
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }


    /* =====================================
       HEADINGS
    ===================================== */

    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    h1 {
        letter-spacing: 0.5px;
    }


    /* =====================================
       GENERAL TEXT VISIBILITY
    ===================================== */

    .stApp p,
    .stApp span,
    .stApp label,
    .stApp [data-testid="stMarkdownContainer"] {
        color: #f8fafc;
    }

    [data-testid="stCaptionContainer"] {
        color: #e9d5ff !important;
    }


    /* =====================================
       TEXT INPUTS
    ===================================== */

    .stApp div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }

    .stApp div[data-baseweb="input"] input,
    .stApp input[type="text"],
    .stApp input[type="email"],
    .stApp input[type="password"],
    .stApp input[type="number"],
    .stApp input[type="search"] {

        background-color: #ffffff !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        caret-color: #111111 !important;
        opacity: 1 !important;
    }


    /* =====================================
       TEXT AREA
    ===================================== */

    .stApp div[data-baseweb="textarea"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }

    .stApp textarea {
        background-color: #ffffff !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        caret-color: #111111 !important;
        opacity: 1 !important;
    }


    /* =====================================
       NUMBER INPUT
    ===================================== */

    [data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: #ffffff !important;
    }

    [data-testid="stNumberInput"] input {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        background-color: #ffffff !important;
    }


    /* =====================================
       DATE INPUT
    ===================================== */

    [data-testid="stDateInput"] div[data-baseweb="input"] {
        background-color: #ffffff !important;
    }

    [data-testid="stDateInput"] input {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        background-color: #ffffff !important;
    }


    /* =====================================
       PLACEHOLDER TEXT
    ===================================== */

    .stApp input::placeholder,
    .stApp textarea::placeholder {
        color: #666666 !important;
        -webkit-text-fill-color: #666666 !important;
        opacity: 1 !important;
    }


    /* =====================================
       SELECT BOX
    ===================================== */

    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
    }

    div[data-baseweb="menu"] * {
        color: #111111 !important;
    }


    /* =====================================
       INPUT LABELS
    ===================================== */

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label {
        color: #ffffff !important;
    }


    /* =====================================
       BUTTONS
    ===================================== */

    .stButton button,
    .stFormSubmitButton button {

        background: linear-gradient(
            90deg,
            #7c3aed,
            #4f46e5
        ) !important;

        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.2rem;
        font-weight: 700;
        transition: 0.3s ease;
        width: 100%;
    }

    .stButton button:hover,
    .stFormSubmitButton button:hover {

        background: linear-gradient(
            90deg,
            #9333ea,
            #6366f1
        ) !important;

        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(124,58,237,0.4);
    }


    /* =====================================
       METRIC CARDS
    ===================================== */

    [data-testid="stMetric"] {

        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    [data-testid="stMetricValue"] {
        color: #c4b5fd !important;
        font-weight: 800;
    }

    [data-testid="stMetricLabel"] {
        color: #e9d5ff !important;
    }


    /* =====================================
       FORMS AND EXPANDERS
    ===================================== */

    [data-testid="stForm"],
    [data-testid="stExpander"] {

        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: 20px;
    }


    /* =====================================
       TABS
    ===================================== */

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }

    .stTabs [data-baseweb="tab"] {

        background: rgba(255,255,255,0.07);
        border-radius: 10px;
        color: #ffffff !important;
        padding: 10px 20px;
    }

    .stTabs [aria-selected="true"] {
        background: #6d28d9 !important;
    }


    /* =====================================
       DATAFRAMES
    ===================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        overflow: hidden;
    }


    /* =====================================
       ALERTS - SUCCESS / WARNING / ERROR
    ===================================== */

    [data-testid="stAlert"] {
        background-color: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 12px !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {
        color: #ffffff !important;
    }


    /* =====================================
       DIVIDERS
    ===================================== */

    hr {
        border-color: rgba(255,255,255,0.15);
    }


    /* =====================================
       HEADER AND FOOTER
    ===================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """, unsafe_allow_html=True)


# ==========================================
# APPLICATION HEADER
# ==========================================





def show_header():

    st.markdown(
        """
        <div style="
            background: linear-gradient(110deg, #6d28d9, #4338ca);
            padding: 25px;
            border-radius: 18px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        ">
            <h1 style="color:white; margin:0; font-size:36px;">
                💰 Cloud Expense Tracker
            </h1>
            <p style="color:#e9d5ff; margin:8px 0 0 0;">
                Track your money. Manage your future.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
