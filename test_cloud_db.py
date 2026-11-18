
from database import get_connection

connection = get_connection()

if connection:
    cursor = connection.cursor()

    for table in ["users", "expenses", "income"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count}")

    cursor.close()
    connection.close()
