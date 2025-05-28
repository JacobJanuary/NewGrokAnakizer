"""
Тесты для модуля базы данных.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import pytest

from src.database.database_manager import DatabaseManager
from src.database.models import Tweet, TweetAnalysis, TweetType
from src.config.config_manager import DatabaseConfig
from src.utils.exceptions import DatabaseError


class TestDatabaseManager(unittest.TestCase):
    """Тесты менеджера базы данных."""

    def setUp(self):
        """Настройка тестов."""
        self.db_config = DatabaseConfig(
            host="localhost",
            user="test_user",
            password="test_pass",
            database="test_db"
        )
        self.db_manager = DatabaseManager(self.db_config)

    @patch('src.database.database_manager.mysql.connector.connect')
    def test_get_connection_success(self, mock_connect):
        """Тест успешного подключения к БД."""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        with self.db_manager._get_connection() as conn:
            self.assertEqual(conn, mock_connection)

        mock_connect.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.database.database_manager.mysql.connector.connect')
    def test_get_connection_failure(self, mock_connect):
        """Тест неудачного подключения к БД."""
        mock_connect.side_effect = Exception("Connection failed")

        with self.assertRaises(DatabaseError):
            with self.db_manager._get_connection():
                pass

    @patch('src.database.database_manager.mysql.connector.connect')
    def test_get_recent_tweets(self, mock_connect):
        """Тест получения недавних твитов."""
        # Настройка мока
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Данные для теста
        mock_cursor.fetchone.return_value = (5,)  # Общее количество
        mock_cursor.fetchall.return_value = [
            (1, "https://twitter.com/test1", "Test tweet 1", datetime.now()),
            (2, "https://twitter.com/test2", "Test tweet 2", datetime.now())
        ]

        # Выполнение теста
        tweets, total_count = self.db_manager.get_recent_tweets(hours=8, limit=100)

        # Проверки
        self.assertEqual(len(tweets), 2)
        self.assertEqual(total_count, 5)
        self.assertIsInstance(tweets[0], Tweet)
        self.assertEqual(tweets[0].url, "https://twitter.com/test1")

    @patch('src.database.database_manager.mysql.connector.connect')
    def test_save_analysis_results(self, mock_connect):
        """Тест сохранения результатов анализа."""
        # Настройка мока
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Тестовые данные
        tweets = [
            Tweet(id=1, url="https://twitter.com/test1", text="Test tweet 1"),
            Tweet(id=2, url="https://twitter.com/test2", text="Test tweet 2")
        ]
        results = [
            TweetAnalysis(type="trueNews", title="Новость", description="Описание новости"),
            TweetAnalysis(type="isSpam", title="", description="")
        ]

        # Выполнение теста
        self.db_manager.save_analysis_results(tweets, results)

        # Проверки
        mock_cursor.executemany.assert_called_once()
        mock_connection.commit.assert_called_once()


class TestModels(unittest.TestCase):
    """Тесты моделей данных."""

    def test_tweet_creation(self):
        """Тест создания твита."""
        tweet = Tweet(
            id=1,
            url="https://twitter.com/test",
            text="Test tweet"
        )

        self.assertEqual(tweet.id, 1)
        self.assertEqual(tweet.url, "https://twitter.com/test")
        self.assertEqual(tweet.text, "Test tweet")

    def test_tweet_validation(self):
        """Тест валидации твита."""
        with self.assertRaises(ValueError):
            Tweet(id=1, url="", text="Test tweet")  # Пустой URL

        with self.assertRaises(ValueError):
            Tweet(id=1, url="https://twitter.com/test", text="")  # Пустой текст

    def test_tweet_analysis_creation(self):
        """Тест создания анализа твита."""
        analysis = TweetAnalysis(
            type="trueNews",
            title="Тест",
            description="Тестовое описание"
        )

        self.assertEqual(analysis.type, "trueNews")
        self.assertEqual(analysis.title, "Тест")
        self.assertTrue(analysis.is_valuable)
        self.assertEqual(analysis.category, "news")

    def test_tweet_analysis_validation(self):
        """Тест валидации анализа твита."""
        with self.assertRaises(ValueError):
            TweetAnalysis(type="invalid_type", title="Тест", description="Описание")

    def test_spam_analysis_not_valuable(self):
        """Тест что спам не является ценным."""
        analysis = TweetAnalysis(type="isSpam", title="", description="")
        self.assertFalse(analysis.is_valuable)
