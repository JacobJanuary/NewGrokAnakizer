"""
Менеджер конфигурации для Crypto News Analyzer.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

from ..utils.exceptions import ConfigError


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных."""
    host: str
    user: str
    password: str
    database: str
    port: int = 3306


@dataclass
class TelegramConfig:
    """Конфигурация Telegram."""
    bot_token: str
    channel_id: str


@dataclass
class GrokConfig:
    """Конфигурация Grok API."""
    api_key: str
    model_name: str = "grok-3"
    base_url: str = "https://api.x.ai/v1"
    use_web_search: bool = True
    temperature: float = 0.1
    max_tokens: int = 10000


@dataclass
class AppConfig:
    """Основная конфигурация приложения."""
    tweet_fetch_hours: int = 8
    tweet_limit: int = 100
    min_tweets_threshold: int = 50
    log_level: str = "INFO"
    log_file: str = "crypto_analyzer.log"


class ConfigManager:
    """Менеджер конфигурации."""

    def __init__(self, env_file: Optional[str] = None) -> None:
        """
        Инициализация менеджера конфигурации.

        Args:
            env_file: Путь к файлу .env (по умолчанию .env)
        """
        load_dotenv(env_file)
        self._validate_environment()

    def _validate_environment(self) -> None:
        """Проверка переменных окружения."""
        required_vars = [
            "XAI_API_KEY", "DB_HOST", "DB_USER", "DB_PASSWORD",
            "DB_NAME", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHANNEL_ID"
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ConfigError(f"Missing environment variables: {', '.join(missing_vars)}")

    def get_database_config(self) -> DatabaseConfig:
        """Получение конфигурации базы данных."""
        return DatabaseConfig(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", "3306"))
        )

    def get_telegram_config(self) -> TelegramConfig:
        """Получение конфигурации Telegram."""
        return TelegramConfig(
            bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            channel_id=os.getenv("TELEGRAM_CHANNEL_ID")
        )

    def get_grok_config(self) -> GrokConfig:
        """Получение конфигурации Grok API."""
        return GrokConfig(
            api_key=os.getenv("XAI_API_KEY"),
            model_name=os.getenv("GROK_MODEL", "grok-3"),
            base_url=os.getenv("GROK_BASE_URL", "https://api.x.ai/v1"),
            use_web_search=os.getenv("GROK_USE_WEB_SEARCH", "true").lower() == "true",
            temperature=float(os.getenv("GROK_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("GROK_MAX_TOKENS", "10000"))
        )

    def get_app_config(self) -> AppConfig:
        """Получение конфигурации приложения."""
        return AppConfig(
            tweet_fetch_hours=int(os.getenv("TWEET_FETCH_HOURS", "8")),
            tweet_limit=int(os.getenv("TWEET_LIMIT", "100")),
            min_tweets_threshold=int(os.getenv("MIN_TWEETS_THRESHOLD", "50")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE", "crypto_analyzer.log")
        )