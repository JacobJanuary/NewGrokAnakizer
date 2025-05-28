"""
Публикатор результатов анализа в Telegram.
"""

import asyncio
from typing import List, Dict
import telegram
from telegram.error import TelegramError


class TelegramPublisher:
    """Публикатор результатов в Telegram."""

    MAX_MESSAGE_LENGTH = 4096

    def __init__(self, config) -> None:
        """Инициализация публикатора Telegram."""
        self.config = config
        self.bot = telegram.Bot(token=config.bot_token)
        self.emojis = self._get_emoji_mapping()

    def _get_emoji_mapping(self) -> Dict[str, str]:
        """Получение маппинга эмодзи."""
        return {
            "Новости": "📢",
            "биткоин": "₿",
            "bitcoin": "₿",
            "ethereum": "Ξ",
        }

    def _escape_markdown_v2(self, text: str) -> str:
        """Экранирование символов для Markdown V2."""
        reserved_chars = r'_*[]()~`>#-+=|{.}!'
        for char in reserved_chars:
            text = text.replace(char, f'\\{char}')
        return text

    async def publish_analysis(self, tweets: List, results: List) -> None:
        """Публикация результатов анализа в Telegram."""
        print(f"Publishing analysis of {len(tweets)} tweets to Telegram")
        # TODO: Добавить полную реализацию

    async def send_test_message(self) -> bool:
        """Отправка тестового сообщения."""
        try:
            test_message = "*Тест криптоанализатора* 🧪\\nСистема работает\!"

            await self.bot.send_message(
                chat_id=self.config.channel_id,
                text=test_message,
                parse_mode="MarkdownV2"
            )

            print("Test message sent successfully")
            return True

        except Exception as e:
            print(f"Failed to send test message: {e}")
            return False
