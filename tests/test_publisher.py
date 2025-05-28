"""
Тесты для модуля публикации в Telegram.
"""

import unittest
from unittest.mock import Mock, patch, AsyncMock
import pytest

from src.publisher.telegram_publisher import TelegramPublisher
from src.config.config_manager import TelegramConfig
from src.database.models import Tweet, TweetAnalysis
from src.utils.exceptions import TelegramError as CustomTelegramError


class TestTelegramPublisher(unittest.TestCase):
    """Тесты публикатора Telegram."""

    def setUp(self):
        """Настройка тестов."""
        self.telegram_config = TelegramConfig(
            bot_token="test_token",
            channel_id="test_channel"
        )
        self.publisher = TelegramPublisher(self.telegram_config)

    def test_escape_markdown_v2(self):
        """Тест экранирования Markdown V2."""
        test_cases = [
            ("Test_text", "Test\\_text"),
            ("Text*with*stars", "Text\\*with\\*stars"),
            ("Text[with]brackets", "Text\\[with\\]brackets"),
            ("Text(with)parens", "Text\\(with\\)parens"),
            ("Normal text", "Normal text")
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.publisher._escape_markdown_v2(input_text)
                self.assertEqual(result, expected)

    def test_get_emoji_for_content(self):
        """Тест получения эмодзи для контента."""
        test_cases = [
            ("bitcoin рост", "BTC растет сегодня", "📢", "₿"),
            ("ethereum падение", "ETH снижается", "📢", "Ξ"),
            ("новая функция", "Обновление протокола", "📢", "✨"),
            ("обычный текст", "Простое описание", "📢", "📢")
        ]

        for title, description, default_emoji, expected in test_cases:
            with self.subTest(title=title):
                result = self.publisher._get_emoji_for_content(title, description, default_emoji)
                self.assertEqual(result, expected)

    def test_filter_valuable_tweets(self):
        """Тест фильтрации ценных твитов."""
        tweets = [
            Tweet(id=1, url="https://twitter.com/test1", text="News tweet"),
            Tweet(id=2, url="https://twitter.com/test2", text="Spam tweet"),
            Tweet(id=3, url="https://twitter.com/test3", text="Analysis tweet")
        ]

        results = [
            TweetAnalysis(type="trueNews", title="Новость", description="Описание новости"),
            TweetAnalysis(type="isSpam", title="", description=""),
            TweetAnalysis(type="analitics", title="Анализ", description="Технический анализ")
        ]

        valuable_items = self.publisher._filter_valuable_tweets(tweets, results)

        self.assertEqual(len(valuable_items), 2)  # Только новость и анализ
        self.assertEqual(valuable_items[0][1].type, "trueNews")
        self.assertEqual(valuable_items[1][1].type, "analitics")

    def test_split_into_messages_single_message(self):
        """Тест разбиения на сообщения - одно сообщение."""
        content = [
            "*Криптоанализ твитов* 🌟\n",
            "*📰 Новости*\n",
            "*Новость BTC ₿*\nBitcoin вырос на 5%. Рынок радуется.\n[Источник](https://twitter.com/test)\n",
            "\n"
        ]

        messages = self.publisher._split_into_messages(content)

        self.assertEqual(len(messages), 1)
        self.assertIn("Криптоанализ твитов", messages[0])
        self.assertIn("Новость BTC", messages[0])

    @pytest.mark.asyncio
    async def test_send_test_message_success(self):
        """Тест отправки тестового сообщения."""
        # Мокаем бота
        self.publisher.bot = AsyncMock()
        self.publisher.bot.send_message = AsyncMock()

        result = await self.publisher.send_test_message()

        self.assertTrue(result)
        self.publisher.bot.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_test_message_failure(self):
        """Тест неудачной отправки тестового сообщения."""
        # Мокаем бота с исключением
        self.publisher.bot = AsyncMock()
        self.publisher.bot.send_message = AsyncMock(side_effect=Exception("Send failed"))

        result = await self.publisher.send_test_message()

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()