"""
Скрипт настройки базы данных для Crypto News Analyzer.
"""

import sys
import os
import mysql.connector
from mysql.connector import Error as MySQLError

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.config_manager import ConfigManager
from utils.logger import setup_logger


def create_database_and_user():
    """Создание базы данных и пользователя."""
    logger = setup_logger(__name__)

    try:
        config_manager = ConfigManager()
        db_config = config_manager.get_database_config()

        # Подключение к MySQL как root
        root_password = input("Enter MySQL root password: ")

        connection = mysql.connector.connect(
            host=db_config.host,
            port=db_config.port,
            user='root',
            password=root_password
        )

        cursor = connection.cursor()

        # Создание базы данных
        logger.info(f"Creating database '{db_config.database}'...")
        cursor.execute(f"""
            CREATE DATABASE IF NOT EXISTS {db_config.database} 
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)

        # Создание пользователя
        logger.info(f"Creating user '{db_config.user}'...")
        cursor.execute(f"""
            CREATE USER IF NOT EXISTS '{db_config.user}'@'%' 
            IDENTIFIED BY '{db_config.password}'
        """)

        # Предоставление прав
        logger.info("Granting privileges...")
        cursor.execute(f"""
            GRANT ALL PRIVILEGES ON {db_config.database}.* 
            TO '{db_config.user}'@'%'
        """)

        cursor.execute("FLUSH PRIVILEGES")

        logger.info("Database and user created successfully!")

        cursor.close()
        connection.close()

        return True

    except MySQLError as e:
        logger.error(f"MySQL error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error: {e}")
        return False


def create_tables():
    """Создание таблиц в базе данных."""
    logger = setup_logger(__name__)

    try:
        config_manager = ConfigManager()
        db_config = config_manager.get_database_config()

        connection = mysql.connector.connect(
            host=db_config.host,
            port=db_config.port,
            user=db_config.user,
            password=db_config.password,
            database=db_config.database
        )

        cursor = connection.cursor()

        # Создание таблицы твитов
        logger.info("Creating tweets table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                url VARCHAR(500) NOT NULL UNIQUE,
                tweet_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                isGrok BOOLEAN DEFAULT NULL,
                
                INDEX idx_created_at (created_at),
                INDEX idx_is_grok (isGrok),
                INDEX idx_created_grok (created_at, isGrok)
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)

        # Создание таблицы анализа
        logger.info("Creating tweet_analysis table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweet_analysis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                url VARCHAR(500) NOT NULL,
                type VARCHAR(50) NOT NULL,
                title VARCHAR(200) DEFAULT '',
                description TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                INDEX idx_created_at (created_at),
                INDEX idx_type (type),
                INDEX idx_url (url),
                INDEX idx_created_type (created_at, type)
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """)

        # Создание события для автоочистки
        logger.info("Creating cleanup event...")
        cursor.execute("SET GLOBAL event_scheduler = ON")

        cursor.execute("""
            CREATE EVENT IF NOT EXISTS cleanup_old_analysis
            ON SCHEDULE EVERY 1 DAY
            STARTS CURRENT_TIMESTAMP
            DO
            DELETE FROM tweet_analysis WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY)
        """)

        connection.commit()
        logger.info("Tables created successfully!")

        cursor.close()
        connection.close()

        return True

    except MySQLError as e:
        logger.error(f"MySQL error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error: {e}")
        return False


def test_connection():
    """Тестирование подключения к базе данных."""
    logger = setup_logger(__name__)

    try:
        config_manager = ConfigManager()
        db_config = config_manager.get_database_config()

        connection = mysql.connector.connect(
            host=db_config.host,
            port=db_config.port,
            user=db_config.user,
            password=db_config.password,
            database=db_config.database
        )

        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        if result[0] == 1:
            logger.info("✅ Database connection test successful!")

            # Проверяем таблицы
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            logger.info(f"Found tables: {[table[0] for table in tables]}")

            cursor.close()
            connection.close()
            return True
        else:
            logger.error("❌ Database connection test failed!")
            return False

    except MySQLError as e:
        logger.error(f"❌ MySQL error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


def main():
    """Главная функция настройки БД."""
    import argparse

    parser = argparse.ArgumentParser(description='Database setup for Crypto News Analyzer')
    parser.add_argument('--create-db', action='store_true', help='Create database and user')
    parser.add_argument('--create-tables', action='store_true', help='Create tables')
    parser.add_argument('--test', action='store_true', help='Test database connection')
    parser.add_argument('--all', action='store_true', help='Perform all setup steps')

    args = parser.parse_args()

    if not any([args.create_db, args.create_tables, args.test, args.all]):
        parser.print_help()
        return 1

    success = True

    if args.all or args.create_db:
        print("=== Creating Database and User ===")
        if not create_database_and_user():
            success = False

    if args.all or args.create_tables:
        print("\n=== Creating Tables ===")
        if not create_tables():
            success = False

    if args.all or args.test:
        print("\n=== Testing Connection ===")
        if not test_connection():
            success = False

    if success:
        print("\n✅ Database setup completed successfully!")
        return 0
    else:
        print("\n❌ Database setup failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())