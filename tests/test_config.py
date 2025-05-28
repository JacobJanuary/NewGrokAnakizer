"""
Тесты для модуля конфигурации.
"""

import unittest
from unittest.mock import patch, Mock
import os
import pytest

from src.config.config_manager import ConfigManager, ConfigError


class TestConfigManager(unittest.TestCase):
    """Тесты менеджера конфигурации."""

    @patch.dict('os.environ', {
        'XAI_API_KEY': 'test_key',
        'DB_HOST': 'localhost',
        'DB_USER': 'user',
        'DB_PASSWORD': 'pass',
        'DB_NAME': 'test_db',
        'TELEGRAM_BOT_TOKEN': 'test_token',
        'TELEGRAM_CHANNEL_ID': 'test_channel'
    })
    def test_valid_config(self):
        """Тест валидной конфигурации."""
        config_manager = ConfigManager()

        # Тест конфигурации БД
        db_config = config_manager.get_database_config()
        self.assertEqual(db_config.host, 'localhost')
        self.assertEqual(db_config.user, 'user')
        self.assertEqual(db_config.password, 'pass')
        self.assertEqual(db_config.database, 'test_db')
        self.assertEqual(db_config.port, 3306)

        # Тест конфигурации Telegram
        tg_config = config_manager.get_telegram_config()
        self.assertEqual(tg_config.bot_token, 'test_token')
        self.assertEqual(tg_config.channel_id, 'test_channel')

        # Тест конфигурации Grok
        grok_config = config_manager.get_grok_config()
        self.assertEqual(grok_config.api_key, 'test_key')
        self.assertEqual(grok_config.model_name, 'grok-3')
        self.assertTrue(grok_config.use_web_search)

    @patch.dict('os.environ', {}, clear=True)
    def test_missing_config(self):
        """Тест отсутствующей конфигурации."""
        with self.assertRaises(ConfigError):
            ConfigManager()

    @patch.dict('os.environ', {
        'XAI_API_KEY': 'test_key',
        'DB_HOST': 'localhost',
        'DB_USER': 'user',
        'DB_PASSWORD': 'pass',
        'DB_NAME': 'test_db',
        'TELEGRAM_BOT_TOKEN': 'test_token',
        'TELEGRAM_CHANNEL_ID': 'test_channel',
        'GROK_TEMPERATURE': '0.5',
        'TWEET_LIMIT': '50'
    })
    def test_custom_config_values(self):
        """Тест кастомных значений конфигурации."""
        config_manager = ConfigManager()

        grok_config = config_manager.get_grok_config()
        self.assertEqual(grok_config.temperature, 0.5)

        app_config = config_manager.get_app_config()
        self.assertEqual(app_config.tweet_limit, 50)

