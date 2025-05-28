"""Скрипт настройки базы данных."""

import sys
import mysql.connector
from mysql.connector import Error as MySQLError


def create_database_and_user():
    """Создание базы данных и пользователя."""
    try:
        root_password = input("Enter MySQL root password: ")

        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password=root_password
        )

        cursor = connection.cursor()

        print("Creating database...")
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS crypto_analyzer 
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)

        print("Creating user...")
        cursor.execute("""
            CREATE USER IF NOT EXISTS 'crypto_user'@'%' 
            IDENTIFIED BY 'secure_password'
        """)

        print("Granting privileges...")
        cursor.execute("""
            GRANT ALL PRIVILEGES ON crypto_analyzer.* 
            TO 'crypto_user'@'%'
        """)

        cursor.execute("FLUSH PRIVILEGES")
        print("✅ Database setup completed!")

        cursor.close()
        connection.close()
        return True

    except MySQLError as e:
        print(f"❌ MySQL error: {e}")
        return False


def main():
    """Главная функция."""
    print("=== Database Setup ===")
    success = create_database_and_user()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
