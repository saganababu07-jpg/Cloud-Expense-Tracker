
from database import get_connection

connection = get_connection()

if connection:
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            category VARCHAR(100) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            description VARCHAR(255),
            expense_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            income_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            source VARCHAR(100) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            income_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    connection.commit()

    cursor.execute("SHOW TABLES")
    print("Cloud database tables:")

    for table in cursor.fetchall():
        print(table[0])

    cursor.close()
    connection.close()

    print("SUCCESS! All tables created in Aiven.")
