
import streamlit as st
import bcrypt
from database import get_connection


# Register a new user
def register_user(name, email, password):

    connection = get_connection()

    if connection is None:
        return False, "Database connection failed."

    cursor = None

    try:
        cursor = connection.cursor()

        # Check whether email already exists
        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )

        if cursor.fetchone():
            return False, "Email already registered."

        # Hash the password
        password_bytes = password.encode("utf-8")
        hashed_password = bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt()
        )

        # Insert user into database
        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (name, email, hashed_password.decode("utf-8"))
        )

        connection.commit()

        return True, "Account created successfully!"

    except Exception as e:
        connection.rollback()
        return False, f"Registration error: {e}"

    finally:
        if cursor:
            cursor.close()
        connection.close()


# Login an existing user
def login_user(email, password):

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        if user is None:
            return None

        password_bytes = password.encode("utf-8")
        stored_hash = user["password_hash"].encode("utf-8")

        if bcrypt.checkpw(password_bytes, stored_hash):
            return user

        return None

    finally:
        cursor.close()
        connection.close()


# Display successful login message
def show_login_success(user):

    st.markdown(
        f"""
        <h3 style="color: black;">
            Successfully logged in as {user['name']}!
        </h3>
        """,
        unsafe_allow_html=True
    )

    # Saving quote in black
    st.markdown(
        """
        <h4 style="color: black;">
            Do not save what is left after spending,
            but spend what is left after saving.
        </h4>
        """,
        unsafe_allow_html=True
    )
