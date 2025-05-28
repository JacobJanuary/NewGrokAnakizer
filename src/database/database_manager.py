"""
Менеджер базы данных для Crypto News Analyzer.
"""

from typing import List, Tuple, Optional
from contextlib import contextmanager
from datetime import datetime

import mysql.connector
from mysql.connector import Error as MySQLError

from ..config.config_manager import DatabaseConfig
from ..database.models import Tweet, TweetAnalysis
from ..utils.exceptions import DatabaseError
from ..utils.logger import get_logger


class DatabaseManager:
    """Менеджер базы данных."""

    def __init__(self, config: DatabaseConfig) -> None:
        """
        Инициализация менеджера базы данных.

        Args:
            config: Конфигурация базы данных
        """
        self.config = config
        self.logger = get_logger(__name__)

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
            self.logger.error(f"Database connection error: {e}")
            raise DatabaseError(f"Failed to connect to database: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()

    def get_recent_tweets(self, hours: int = 8, limit: int = 100) -> Tuple[List[Tweet], int]:
        """
        Получение недавних твитов из базы данных.

        Args:
            hours: Количество часов для поиска твитов
            limit: Максимальное количество твитов

        Returns:
            Tuple из списка твитов и общего количества найденных твитов

        Raises:
            DatabaseError: При ошибке работы с базой данных
        """
        with self._get_connection() as connection:
            try:
                cursor = connection.cursor()

                # Сначала получаем общее количество
                count_query = """
                    SELECT COUNT(*) 
                    FROM tweets 
                    WHERE created_at >= NOW() - INTERVAL %s HOUR 
                    AND isGrok IS NULL
                    AND tweet_text IS NOT NULL
                    AND TRIM(tweet_text) != ''
                    AND LENGTH(TRIM(tweet_text)) >= 10
                    AND tweet_text NOT LIKE 'RT @%'
                """
                cursor.execute(count_query, (hours,))
                total_count = cursor.fetchone()[0]

                # Получаем неанализированные твиты
                # Добавьте фильтры в SQL запрос:
                query = """
                        SELECT id, url, tweet_text, created_at
                        FROM tweets
                        WHERE created_at >= NOW() - INTERVAL %s HOUR
                          AND isGrok IS NULL
                          AND tweet_text IS NOT NULL
                          AND TRIM(tweet_text) != ''
                    AND LENGTH(TRIM(tweet_text)) >= 10
                    AND tweet_text NOT LIKE 'RT @%'
                        ORDER BY created_at DESC
                            LIMIT %s \
                        """

                cursor.execute(query, (hours, limit))
                rows = cursor.fetchall()

                self.logger.info(f"Found {len(rows)} new tweets out of {total_count} total")

                # Преобразуем в объекты Tweet
                tweets = []
                for tweet_id, url, tweet_text, created_at in rows:
                    tweets.append(Tweet(
                        id=tweet_id,
                        url=url,
                        text=tweet_text,
                        created_at=created_at
                    ))

                cursor.close()
                return tweets, total_count

            except MySQLError as e:
                self.logger.error(f"Database error in get_recent_tweets: {e}")
                raise DatabaseError(f"Failed to get tweets: {e}")

    def mark_tweets_as_processing(self, tweet_ids: List[int]) -> None:
        """
        Помечаем твиты как обрабатываемые.

        Args:
            tweet_ids: Список ID твитов

        Raises:
            DatabaseError: При ошибке обновления
        """
        if not tweet_ids:
            return

        with self._get_connection() as connection:
            try:
                cursor = connection.cursor()

                # Используем один запрос для всех ID
                placeholders = ','.join(['%s'] * len(tweet_ids))
                update_query = f"UPDATE tweets SET isGrok = TRUE WHERE id IN ({placeholders})"

                cursor.execute(update_query, tweet_ids)
                connection.commit()

                self.logger.info(f"Marked {len(tweet_ids)} tweets as processing")
                cursor.close()

            except MySQLError as e:
                connection.rollback()
                self.logger.error(f"Database error in mark_tweets_as_processing: {e}")
                raise DatabaseError(f"Failed to mark tweets as processing: {e}")

    def save_analysis_results(self, tweets: List[Tweet], results: List[TweetAnalysis]) -> None:
        """
        Сохранение результатов анализа в базу данных.

        Args:
            tweets: Список твитов
            results: Список результатов анализа

        Raises:
            DatabaseError: При ошибке сохранения
        """
        if len(tweets) != len(results):
            raise ValueError("Number of tweets and results must match")

        with self._get_connection() as connection:
            try:
                cursor = connection.cursor()

                insert_query = """
                    INSERT INTO tweet_analysis (url, type, title, description, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """

                current_time = datetime.now()
                batch_data = []

                for tweet, analysis in zip(tweets, results):
                    batch_data.append((
                        tweet.url,
                        analysis.type,
                        analysis.title,
                        analysis.description,
                        current_time
                    ))

                # Batch insert для лучшей производительности
                cursor.executemany(insert_query, batch_data)
                connection.commit()

                self.logger.info(f"Successfully saved {len(results)} analysis results")
                cursor.close()

            except MySQLError as e:
                connection.rollback()
                self.logger.error(f"Database error in save_analysis_results: {e}")
                raise DatabaseError(f"Failed to save analysis results: {e}")

    def get_analysis_statistics(self, hours: int = 24) -> dict:
        """
        Получение статистики анализа.

        Args:
            hours: Период для анализа в часах

        Returns:
            Словарь со статистикой
        """
        with self._get_connection() as connection:
            try:
                cursor = connection.cursor(dictionary=True)

                # Общая статистика
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_processed,
                        COUNT(CASE WHEN type NOT IN ('isSpam', 'isFlood', 'alreadyPosted') THEN 1 END) as valuable,
                        COUNT(CASE WHEN type = 'isSpam' THEN 1 END) as spam,
                        COUNT(CASE WHEN type = 'isFlood' THEN 1 END) as flood,
                        COUNT(CASE WHEN type = 'alreadyPosted' THEN 1 END) as duplicates
                    FROM tweet_analysis 
                    WHERE created_at >= NOW() - INTERVAL %s HOUR
                """, (hours,))

                general_stats = cursor.fetchone()

                # Статистика по типам
                cursor.execute("""
                    SELECT type, COUNT(*) as count
                    FROM tweet_analysis 
                    WHERE created_at >= NOW() - INTERVAL %s HOUR
                    GROUP BY type
                    ORDER BY count DESC
                """, (hours,))

                type_stats = cursor.fetchall()

                cursor.close()

                return {
                    'general': general_stats,
                    'by_type': type_stats,
                    'period_hours': hours
                }

            except MySQLError as e:
                self.logger.error(f"Database error in get_analysis_statistics: {e}")
                return {}

    def cleanup_old_data(self, days: int = 30) -> int:
        """
        Очистка старых данных анализа.

        Args:
            days: Количество дней для хранения данных

        Returns:
            Количество удаленных записей
        """
        with self._get_connection() as connection:
            try:
                cursor = connection.cursor()

                delete_query = """
                    DELETE FROM tweet_analysis 
                    WHERE created_at < NOW() - INTERVAL %s DAY
                """

                cursor.execute(delete_query, (days,))
                deleted_count = cursor.rowcount
                connection.commit()

                self.logger.info(f"Cleaned up {deleted_count} old analysis records")
                cursor.close()

                return deleted_count

            except MySQLError as e:
                connection.rollback()
                self.logger.error(f"Database error in cleanup_old_data: {e}")
                raise DatabaseError(f"Failed to cleanup old data: {e}")

    def test_connection(self) -> bool:
        """
        Тестирование подключения к базе данных.

        Returns:
            True если подключение успешно
        """
        try:
            with self._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                return result[0] == 1
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False