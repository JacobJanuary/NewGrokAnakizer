"""
Публикатор результатов анализа в Telegram.
"""

import asyncio
from typing import List, Dict, Tuple

import telegram
from telegram.error import TelegramError

from ..config.config_manager import TelegramConfig
from ..database.models import Tweet, TweetAnalysis, TweetType
from ..utils.exceptions import TelegramError as CustomTelegramError
from ..utils.logger import get_logger


class TelegramPublisher:
    """Публикатор результатов в Telegram."""

    MAX_MESSAGE_LENGTH = 4096

    def __init__(self, config: TelegramConfig) -> None:
        """
        Инициализация публикатора Telegram.

        Args:
            config: Конфигурация Telegram
        """
        self.config = config
        self.logger = get_logger(__name__)

        self.bot = telegram.Bot(token=config.bot_token)
        self.emojis = self._get_emoji_mapping()
        self.categories = self._get_categories()

    def _get_emoji_mapping(self) -> Dict[str, str]:
        """Получение маппинга эмодзи."""
        return {
            # Общие категории
            "Новости": "📢",
            "Слухи": "❓",
            "инсайды": "🔍",
            "технический анализ": "📊",
            "торговые идеи": "💰",
            "прогнозы": "🔮",
            "обучение": "📚",
            # Контекстные эмодзи
            "рост": "📈",
            "падение": "📉",
            "биткоин": "₿",
            "btc": "₿",
            "bitcoin": "₿",
            "ethereum": "Ξ",
            "eth": "Ξ",
            "партнерство": "🤝",
            "запуск": "🚀",
            "листинг": "📋",
            "регулирование": "⚖️",
            "взлом": "🔓",
            "безопасность": "🔒",
            "закон": "📜",
            "суд": "⚖️",
            "предупреждение": "⚠️",
            "опасность": "🚨",
            "инвестиции": "💵",
            "доход": "💸",
            "кошелек": "👛",
            "новая функция": "✨",
            "обновление": "🔄",
            "успех": "✅",
            "провал": "❌",
            "внимание": "👀",
            "важно": "‼️",
            "инновации": "💡",
            "платежи": "💳",
            "nft": "🖼️",
            "defi": "🏦",
            "майнинг": "⛏️",
            "staking": "🥩",
            "комиссия": "💲",
            "халвинг": "✂️",
            "токен": "🪙",
            "ликвидность": "💧",
            "волатильность": "🎢"
        }

    def _get_categories(self) -> List[Tuple[str, List[str], str]]:
        """Получение категорий для группировки."""
        return [
            ("📰 Новости", [TweetType.TRUE_NEWS.value], "Новости"),
            ("🗣️ Слухи", [TweetType.FAKE_NEWS.value], "Слухи"),
            ("🔍 Инсайд", [TweetType.INSIDE.value], "инсайды"),
            ("📚 Учеба", [TweetType.TUTORIAL.value], "обучение"),
            ("📊 Аналитика и трейдинг", [TweetType.ANALYTICS.value, TweetType.TRADING.value], "технический анализ"),
            ("🌐 Другое", [TweetType.OTHERS.value], "Другое")
        ]

    def _escape_markdown_v2(self, text: str) -> str:
        """
        Экранирование символов для Markdown V2.

        Args:
            text: Исходный текст

        Returns:
            Экранированный текст
        """
        reserved_chars = r'_*[]()~`>#-+=|{.}!'
        for char in reserved_chars:
            text = text.replace(char, f'\\{char}')
        return text

    def _get_emoji_for_content(self, title: str, description: str, category_emoji: str) -> str:
        """
        Получение эмодзи для контента на основе ключевых слов.

        Args:
            title: Заголовок
            description: Описание
            category_emoji: Базовый эмодзи категории

        Returns:
            Подходящий эмодзи
        """
        combined_text = (title + " " + description).lower()

        # Ищем контекстные эмодзи, исключая категориальные
        excluded_keys = [
            "Новости", "Слухи", "инсайды", "технический анализ",
            "торговые идеи", "прогнозы", "обучение"
        ]

        for key, emoji in self.emojis.items():
            if key in combined_text and key not in excluded_keys:
                return emoji

        return category_emoji

    def _filter_valuable_tweets(self, tweets: List[Tweet], results: List[TweetAnalysis]) -> List[Tuple[Tweet, TweetAnalysis]]:
        """
        Фильтрация ценных твитов для публикации.

        Args:
            tweets: Список твитов
            results: Список результатов анализа

        Returns:
            Список пар (твит, анализ) для публикации
        """
        valuable_items = []

        for tweet, analysis in zip(tweets, results):
            if analysis.is_valuable:
                valuable_items.append((tweet, analysis))

        self.logger.info(f"Found {len(valuable_items)} valuable tweets out of {len(tweets)}")
        return valuable_items

    def _group_by_categories(self, items: List[Tuple[Tweet, TweetAnalysis]]) -> Dict[str, List[Tuple[Tweet, TweetAnalysis]]]:
        """
        Группировка элементов по категориям.

        Args:
            items: Список пар (твит, анализ)

        Returns:
            Словарь с группировкой по категориям
        """
        grouped = {}

        for category_name, category_types, _ in self.categories:
            category_items = [
                (tweet, analysis) for tweet, analysis in items
                if analysis.type in category_types
            ]
            if category_items:
                grouped[category_name] = category_items

        return grouped

    def _format_message_content(self, grouped_items: Dict[str, List[Tuple[Tweet, TweetAnalysis]]]) -> List[str]:
        """
        Форматирование содержимого сообщений.

        Args:
            grouped_items: Группированные элементы

        Returns:
            Список строк для формирования сообщений
        """
        content = ["*Криптоанализ твитов* 🌟\n"]

        for category_name, category_types, category_emoji_key in self.categories:
            if category_name not in grouped_items:
                continue

            content.append(f"*{category_name}*\n")

            for tweet, analysis in grouped_items[category_name]:
                # Экранируем символы
                title = self._escape_markdown_v2(analysis.title)
                description = self._escape_markdown_v2(analysis.description)
                url = self._escape_markdown_v2(tweet.url)

                # Получаем эмодзи
                base_emoji = self.emojis.get(category_emoji_key, "📢")
                emoji = self._get_emoji_for_content(analysis.title, analysis.description, base_emoji)

                # Формируем строку твита
                tweet_text = f"*{title} {emoji}*\n{description}\n[Источник]({url})\n"
                content.append(tweet_text)

            content.append("\n")

        return content

    def _split_into_messages(self, content: List[str]) -> List[str]:
        """
        Разбиение контента на сообщения с учетом лимита Telegram.

        Args:
            content: Список строк контента

        Returns:
            Список готовых сообщений
        """
        messages = []
        current_message = ["*Криптоанализ твитов* 🌟\n"]
        current_length = len(current_message[0])

        for line in content[1:]:  # Пропускаем заголовок
            line_length = len(line)

            # Проверяем, поместится ли строка в текущее сообщение
            if current_length + line_length > self.MAX_MESSAGE_LENGTH:
                # Сохраняем текущее сообщение
                if len(current_message) > 1:  # Есть контент кроме заголовка
                    messages.append("".join(current_message))

                # Начинаем новое сообщение
                current_message = []
                current_length = 0

                # Если это заголовок категории, начинаем с него
                if line.startswith("*") and not line.startswith("*Криптоанализ"):
                    current_message.append(line)
                    current_length = line_length
                else:
                    # Для твитов добавляем минимальный контекст
                    if current_message:  # Уже есть заголовок категории
                        current_message.append(line)
                        current_length += line_length
                    else:
                        # Добавляем общий заголовок и твит
                        header = "*Криптоанализ твитов* 🌟\n"
                        current_message.append(header)
                        current_message.append(line)
                        current_length = len(header) + line_length
            else:
                current_message.append(line)
                current_length += line_length

        # Добавляем последнее сообщение
        if len(current_message) > 1:
            messages.append("".join(current_message))

        return messages

    async def publish_analysis(self, tweets: List[Tweet], results: List[TweetAnalysis]) -> None:
        """
        Публикация результатов анализа в Telegram.

        Args:
            tweets: Список твитов
            results: Список результатов анализа

        Raises:
            CustomTelegramError: При ошибке отправки
        """
        if len(tweets) != len(results):
            raise ValueError("Number of tweets and results must match")

        try:
            # Фильтруем ценные твиты
            valuable_items = self._filter_valuable_tweets(tweets, results)

            if not valuable_items:
                self.logger.info("No valuable tweets to publish")
                return

            # Группируем по категориям
            grouped_items = self._group_by_categories(valuable_items)

            # Форматируем контент
            content = self._format_message_content(grouped_items)

            # Разбиваем на сообщения
            messages = self._split_into_messages(content)

            if not messages:
                self.logger.warning("No messages generated for publishing")
                return

            # Отправляем сообщения
            await self._send_messages(messages)

        except Exception as e:
            self.logger.error(f"Error in publish_analysis: {e}")
            raise CustomTelegramError(f"Failed to publish analysis: {e}")

    async def _send_messages(self, messages: List[str]) -> None:
        """
        Отправка сообщений в Telegram канал.

        Args:
            messages: Список сообщений для отправки

        Raises:
            CustomTelegramError: При ошибке отправки
        """
        successful_sends = 0

        for i, message in enumerate(messages, 1):
            try:
                await self.bot.send_message(
                    chat_id=self.config.channel_id,
                    text=message,
                    parse_mode="MarkdownV2",
                    disable_web_page_preview=True
                )

                successful_sends += 1
                self.logger.info(f"Successfully sent message {i}/{len(messages)}")

                # Небольшая задержка между сообщениями
                if i < len(messages):
                    await asyncio.sleep(1)

            except TelegramError as e:
                self.logger.error(f"Failed to send message {i}/{len(messages)}: {e}")

                # Для некоторых ошибок прерываем отправку
                if "chat not found" in str(e).lower() or "bot was blocked" in str(e).lower():
                    raise CustomTelegramError(f"Critical Telegram error: {e}")

        if successful_sends == 0:
            raise CustomTelegramError("Failed to send any messages")

        self.logger.info(f"Successfully sent {successful_sends}/{len(messages)} messages")

    async def send_test_message(self) -> bool:
        """
        Отправка тестового сообщения.

        Returns:
            True если сообщение отправлено успешно
        """
        try:
            test_message = "*Тест криптоанализатора* 🧪\nСистема работает корректно\\!"

            await self.bot.send_message(
                chat_id=self.config.channel_id,
                text=test_message,
                parse_mode="MarkdownV2"
            )

            self.logger.info("Test message sent successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send test message: {e}")
            return False

    async def get_bot_info(self) -> Dict[str, str]:
        """
        Получение информации о боте.

        Returns:
            Словарь с информацией о боте
        """
        try:
            bot_info = await self.bot.get_me()
            return {
                "id": str(bot_info.id),
                "username": bot_info.username or "N/A",
                "first_name": bot_info.first_name or "N/A",
                "is_bot": str(bot_info.is_bot)
            }
        except Exception as e:
            self.logger.error(f"Failed to get bot info: {e}")
            return {}

    def format_statistics_message(self, stats: Dict) -> str:
        """
        Форматирование сообщения со статистикой.

        Args:
            stats: Словарь со статистикой

        Returns:
            Отформатированное сообщение
        """
        if not stats:
            return "*Статистика недоступна* ❌"

        general = stats.get('general', {})
        by_type = stats.get('by_type', [])
        period = stats.get('period_hours', 24)

        message_parts = [
            f"*📊 Статистика за {period}ч*\n",
            f"Обработано: {general.get('total_processed', 0)}",
            f"Ценных: {general.get('valuable', 0)}",
            f"Спам: {general.get('spam', 0)}",
            f"Шум: {general.get('flood', 0)}",
            f"Дубли: {general.get('duplicates', 0)}\n"
        ]

        if by_type:
            message_parts.append("*По типам:*")
            for item in by_type[:5]:  # Топ 5
                type_name = item['type']
                count = item['count']
                message_parts.append(f"• {type_name}: {count}")

        message = "\n".join(message_parts)
        return self._escape_markdown_v2(message)