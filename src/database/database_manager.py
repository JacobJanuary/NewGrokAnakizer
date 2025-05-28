"""
Менеджер базы данных для Crypto News Analyzer.
"""

from typing import List, Tuple
from contextlib import contextmanager
from datetime import datetime
import mysql.connector
from mysql.connector import Error as MySQLError


class DatabaseManager:
    """Менеджер базы данных."""

    def __init__(self, config) -> None:
        """Инициализация менеджера базы данных."""
        self.config = config

    @contextmanager
    def _get_connection(self):
        """Контекстный менеджер для подключения к БД."""
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                port=self.config.port,
                autocommit=False,
                use_unicode=True,
                charset='utf8mb4'
            )
            yield connection
        except MySQLError as e:
            print(f"Database connection error: {e}")
            raise Exception(f"Failed to connect to database: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()

    def get_recent_tweets(self, hours: int = 8, limit: int = 100) -> Tuple[List, int]:
        """Получение недавних твитов."""
        # TODO: Добавить полную реализацию
        print(f"Getting recent tweets for {hours} hours, limit {limit}")
        return [], 0

    def save_analysis_results(self, tweets: List, results: List) -> None:
        """Сохранение результатов анализа."""
        # TODO: Добавить полную реализацию
        print(f"Saving {len(results)} analysis results")

    def test_connection(self) -> bool:
        """Тестирование подключения к БД."""
        try:
            with self._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                return result[0] == 1
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
