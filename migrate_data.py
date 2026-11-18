
import mysql.connector
import streamlit as st

from database import get_connection

# Connect to LOCAL MySQL
local = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Saganababu007",
    database="expense_tracker",
    port=3306
)

# Connect to AIVEN CLOUD MYSQL
cloud = get_connection()

if cloud:
    local_cursor = local.cursor(dictionary=True)
    cloud_cursor = cloud.cursor()

    # Migrate users
    local_cursor.execute("SELECT * FROM users")
    users = local_cursor.fetchall()

    for user in users:
        cloud_cursor.execute("""
            INSERT IGNORE INTO users
            (user_id, name, email, password_hash, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            user["user_id"],
            user["name"],
            user["email"],
            user["password_hash"],
            user["created_at"]
        ))

    # Migrate expenses
    local_cursor.execute("SELECT * FROM expenses")
    expenses = local_cursor.fetchall()

    for expense in expenses:
        cloud_cursor.execute("""
            INSERT IGNORE INTO expenses
            (expense_id, user_id, category, amount,
             description, expense_date, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            expense["expense_id"],
            expense["user_id"],
            expense["category"],
            expense["amount"],
            expense["description"],
            expense["expense_date"],
            expense["created_at"]
        ))

    # Migrate income
    local_cursor.execute("SELECT * FROM income")
    incomes = local_cursor.fetchall()

    for income in incomes:
        cloud_cursor.execute("""
            INSERT IGNORE INTO income
            (income_id, user_id, source, amount, income_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            income["income_id"],
            income["user_id"],
            income["source"],
            income["amount"],
            income["income_date"]
        ))

    cloud.commit()

    print("Migration completed!")
    print("Users:", len(users))
    print("Expenses:", len(expenses))
    print("Income:", len(incomes))

    local_cursor.close()
    cloud_cursor.close()
    local.close()
    cloud.close()
