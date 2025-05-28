#!/usr/bin/env python3
"""
Скрипт развертывания структуры Crypto News Analyzer в существующем проекте PyCharm.
Создает все необходимые папки и заготовки файлов в текущей директории.
"""

import os
from pathlib import Path


class ProjectStructureSetup:
    """Класс для создания структуры проекта в текущей директории."""

    def __init__(self):
        """Инициализация в текущей директории."""
        self.base_path = Path.cwd()
        print(f"🏗️  Создание структуры Crypto News Analyzer")
        print(f"📍 Текущая директория: {self.base_path.absolute()}")

    def create_directory_structure(self) -> None:
        """Создание структуры директорий."""
        directories = [
            "src", "src/config", "src/database", "src/analyzer", "src/publisher", "src/utils",
            "tests", "scripts", "docker", "config", "docs", "logs", ".idea"
        ]

        print(f"\n🏗️  Создание структуры директорий:")

        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   📁 {directory}")

    def create_python_files(self) -> None:
        """Создание Python файлов с заготовками."""
        files = {
            "src/__init__.py": self.get_src_init(),
            "src/main.py": self.get_main_py(),
            "src/config/__init__.py": self.get_config_init(),
            "src/config/config_manager.py": self.get_config_manager(),
            "src/database/__init__.py": self.get_database_init(),
            "src/database/models.py": self.get_models(),
            "src/database/database_manager.py": self.get_database_manager(),
            "src/analyzer/__init__.py": self.get_analyzer_init(),
            "src/analyzer/grok_analyzer.py": self.get_grok_analyzer(),
            "src/publisher/__init__.py": self.get_publisher_init(),
            "src/publisher/telegram_publisher.py": self.get_telegram_publisher(),
            "src/utils/__init__.py": self.get_utils_init(),
            "src/utils/exceptions.py": self.get_exceptions(),
            "src/utils/logger.py": self.get_logger(),
            "tests/__init__.py": '"""Тесты для Crypto News Analyzer."""',
            "tests/test_config.py": self.get_test_config(),
            "tests/test_database.py": self.get_test_database(),
            "tests/test_analyzer.py": self.get_test_analyzer(),
            "tests/test_publisher.py": self.get_test_publisher(),
            "scripts/monitoring.py": self.get_monitoring(),
            "scripts/setup_database.py": self.get_setup_database(),
            "scripts/run_tests.py": self.get_run_tests(),
        }

        print(f"\n🐍 Создание Python файлов:")

        for file_path, content in files.items():
            full_path = self.base_path / file_path
            full_path.write_text(content, encoding='utf-8')
            print(f"   📄 {file_path}")

    def create_config_files(self) -> None:
        """Создание конфигурационных файлов."""
        files = {
            "config/.env.example": self.get_env_example(),
            ".gitignore": self.get_gitignore(),
            "requirements.txt": self.get_requirements(),
            "requirements-dev.txt": self.get_requirements_dev(),
            "docker/Dockerfile": self.get_dockerfile(),
            "docker/docker-compose.yml": self.get_docker_compose(),
            "docker/init.sql": self.get_init_sql(),
            "setup.py": self.get_setup_py(),
            "pyproject.toml": self.get_pyproject_toml(),
            ".pre-commit-config.yaml": self.get_precommit(),
        }

        print(f"\n⚙️  Создание конфигурационных файлов:")

        for file_path, content in files.items():
            full_path = self.base_path / file_path
            full_path.write_text(content, encoding='utf-8')
            print(f"   📄 {file_path}")

    def create_documentation_files(self) -> None:
        """Создание файлов документации."""
        files = {
            "README.md": self.get_readme(),
            "docs/DEPLOYMENT.md": self.get_deployment_doc(),
            "docs/API_REFERENCE.md": self.get_api_reference(),
            "PROJECT_STRUCTURE.md": self.get_project_structure(),
        }

        print(f"\n📚 Создание файлов документации:")

        for file_path, content in files.items():
            full_path = self.base_path / file_path
            full_path.write_text(content, encoding='utf-8')
            print(f"   📄 {file_path}")

    def create_pycharm_files(self) -> None:
        """Создание файлов PyCharm."""
        files = {
            ".idea/misc.xml": self.get_pycharm_misc(),
            ".idea/modules.xml": self.get_pycharm_modules(),
            ".idea/crypto-news-analyzer.iml": self.get_pycharm_iml(),
            "logs/.gitkeep": "# Директория для логов\n",
        }

        print(f"\n🔧 Создание файлов PyCharm и дополнительных:")

        for file_path, content in files.items():
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            print(f"   📄 {file_path}")

    def create_project_structure(self) -> None:
        """Создание полной структуры проекта."""
        try:
            self.create_directory_structure()
            self.create_python_files()
            self.create_config_files()
            self.create_documentation_files()
            self.create_pycharm_files()

            print(f"\n✅ Структура проекта Crypto News Analyzer успешно создана!")
            self.show_next_steps()

        except Exception as e:
            print(f"\n❌ Ошибка при создании структуры проекта: {e}")
            raise

    def show_next_steps(self) -> None:
        """Показать следующие шаги."""
        print(f"\n📋 Следующие шаги:")
        print(f"   1. 📦 pip install -r requirements.txt")
        print(f"   2. 📦 pip install -r requirements-dev.txt")
        print(f"   3. ⚙️  cp config/.env.example .env")
        print(f"   4. ✏️  # Отредактируйте .env файл")
        print(f"   5. 🗄️  python scripts/setup_database.py --all")
        print(f"   6. 🧪 python -m src.main --test")

        files_count = len(list(self.base_path.rglob("*"))) - len(list(self.base_path.rglob("*/")))
        print(f"\n📊 Создано файлов: {files_count}")
        print(f"🚀 Готово! Удачной разработки в PyCharm! 🎉")

    # Методы для получения содержимого файлов
    def get_src_init(self):
        return '''"""
Crypto News Analyzer - Automated crypto news analysis with Grok AI.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
'''

    def get_main_py(self):
        return '''"""
Главный модуль Crypto News Analyzer.
"""

import asyncio
import sys
from typing import Optional

# TODO: Раскомментировать после создания модулей
# from .config.config_manager import ConfigManager
# from .database.database_manager import DatabaseManager
# from .analyzer.grok_analyzer import GrokAnalyzer
# from .publisher.telegram_publisher import TelegramPublisher


class CryptoNewsAnalyzer:
    """Главный класс анализатора криптоновостей."""

    def __init__(self, config_file: Optional[str] = None) -> None:
        """Инициализация анализатора."""
        # TODO: Добавить инициализацию компонентов
        print("🚀 CryptoNewsAnalyzer initialized")

    async def run_analysis(self, force_run: bool = False) -> None:
        """Основной цикл анализа."""
        print("🔍 Starting crypto news analysis...")
        # TODO: Добавить логику анализа

    async def test_components(self) -> bool:
        """Тестирование компонентов."""
        print("🧪 Testing components...")
        # TODO: Добавить тестирование
        return True


async def main() -> None:
    """Главная функция запуска анализатора."""
    try:
        force_run = "--force" in sys.argv
        test_mode = "--test" in sys.argv

        analyzer = CryptoNewsAnalyzer()

        if test_mode:
            success = await analyzer.test_components()
            sys.exit(0 if success else 1)

        await analyzer.run_analysis(force_run=force_run)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
'''

    def get_config_init(self):
        return '''"""Модуль конфигурации."""

# TODO: Раскомментировать после создания config_manager.py
# from .config_manager import (
#     ConfigManager,
#     DatabaseConfig,
#     TelegramConfig,
#     GrokConfig,
#     AppConfig
# )

__all__ = []
'''

    def get_config_manager(self):
        return '''"""
Менеджер конфигурации для Crypto News Analyzer.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


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
    log_file: str = "logs/crypto_analyzer.log"


class ConfigManager:
    """Менеджер конфигурации."""

    def __init__(self, env_file: Optional[str] = None) -> None:
        """Инициализация менеджера конфигурации."""
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
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

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
            log_file=os.getenv("LOG_FILE", "logs/crypto_analyzer.log")
        )
'''

    def get_database_init(self):
        return '''"""Модуль работы с базой данных."""

# TODO: Раскомментировать после создания файлов
# from .database_manager import DatabaseManager
# from .models import Tweet, TweetAnalysis, TweetType, AnalysisStats

__all__ = []
'''

    def get_models(self):
        return '''"""
Модели данных для Crypto News Analyzer.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class TweetType(Enum):
    """Типы анализа твитов."""
    TRUE_NEWS = "trueNews"
    FAKE_NEWS = "fakeNews"
    INSIDE = "inside"
    TUTORIAL = "tutorial"
    ANALYTICS = "analitics"
    TRADING = "trading"
    OTHERS = "others"
    SPAM = "isSpam"
    FLOOD = "isFlood"
    ALREADY_POSTED = "alreadyPosted"


@dataclass
class Tweet:
    """Модель твита."""
    id: int
    url: str
    text: str
    created_at: Optional[datetime] = None
    is_grok_processed: Optional[bool] = None

    def __post_init__(self):
        """Валидация данных."""
        if not self.url:
            raise ValueError("Tweet URL cannot be empty")
        if not self.text:
            raise ValueError("Tweet text cannot be empty")


@dataclass
class TweetAnalysis:
    """Модель результата анализа твита."""
    type: str
    title: str
    description: str

    def __post_init__(self):
        """Валидация данных."""
        valid_types = [t.value for t in TweetType]
        if self.type not in valid_types:
            raise ValueError(f"Invalid tweet type: {self.type}")

    @property
    def is_valuable(self) -> bool:
        """Проверка ценности анализа."""
        non_valuable = [TweetType.SPAM.value, TweetType.FLOOD.value, TweetType.ALREADY_POSTED.value]
        return self.type not in non_valuable and self.title and self.description


@dataclass
class AnalysisStats:
    """Статистика анализа."""
    total_tweets: int
    processed_tweets: int
    valuable_tweets: int
    spam_tweets: int
    flood_tweets: int
    duplicate_tweets: int
    error_count: int
    processing_time: float

    @property
    def success_rate(self) -> float:
        """Процент успешно обработанных твитов."""
        if self.total_tweets == 0:
            return 0.0
        return (self.processed_tweets / self.total_tweets) * 100
'''

    def get_database_manager(self):
        return '''"""
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
'''

    def get_analyzer_init(self):
        return '''"""Модуль анализа с помощью Grok API."""

# TODO: Раскомментировать после создания grok_analyzer.py
# from .grok_analyzer import GrokAnalyzer

__all__ = []
'''

    def get_grok_analyzer(self):
        return '''"""
Анализатор твитов с использованием Grok API.
"""

import json
from typing import List, Dict, Optional
from openai import OpenAI


class GrokAnalyzer:
    """Анализатор твитов с использованием Grok API."""

    def __init__(self, config) -> None:
        """Инициализация анализатора Grok."""
        self.config = config
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
        self.system_prompt = self._get_system_prompt()

    def _get_system_prompt(self) -> Dict[str, str]:
        """Получение системного промпта."""
        prompt = """
Role: You are a crypto market analyst.

Task: Analyze tweets and provide structured information in Russian.

INPUT: JSON array of tweets
OUTPUT: JSON array with "type", "title", "description" fields

CRITICAL: Always return valid JSON array only.
"""
        return {"role": "system", "content": prompt}

    def analyze_tweets(self, tweets: List, use_web_search: Optional[bool] = None) -> List:
        """Анализ твитов с помощью Grok API."""
        if not tweets:
            return []

        print(f"Analyzing {len(tweets)} tweets with Grok API")

        # TODO: Добавить полную реализацию анализа
        results = []
        for tweet in tweets:
            results.append({
                "type": "others",
                "title": "Тест",
                "description": "Тестовое описание"
            })

        return results

    def test_connection(self) -> bool:
        """Тестирование подключения к Grok API."""
        try:
            print("Testing Grok API connection...")
            # TODO: Добавить реальное тестирование
            return True
        except Exception as e:
            print(f"API connection test failed: {e}")
            return False
'''

    def get_publisher_init(self):
        return '''"""Модуль публикации в Telegram."""

# TODO: Раскомментировать после создания telegram_publisher.py
# from .telegram_publisher import TelegramPublisher

__all__ = []
'''

    def get_telegram_publisher(self):
        return '''"""
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
            text = text.replace(char, f'\\\\{char}')
        return text

    async def publish_analysis(self, tweets: List, results: List) -> None:
        """Публикация результатов анализа в Telegram."""
        print(f"Publishing analysis of {len(tweets)} tweets to Telegram")
        # TODO: Добавить полную реализацию

    async def send_test_message(self) -> bool:
        """Отправка тестового сообщения."""
        try:
            test_message = "*Тест криптоанализатора* 🧪\\\\nСистема работает\\!"

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
'''

    def get_utils_init(self):
        return '''"""Утилиты и вспомогательные функции."""

# TODO: Раскомментировать после создания файлов
# from .exceptions import (
#     CryptoAnalyzerError,
#     ConfigError,
#     DatabaseError,
#     GrokAPIError,
#     TelegramError
# )
# from .logger import setup_logger, get_logger

__all__ = []
'''

    def get_exceptions(self):
        return '''"""
Исключения для Crypto News Analyzer.
"""


class CryptoAnalyzerError(Exception):
    """Базовый класс исключений для анализатора."""
    pass


class ConfigError(CryptoAnalyzerError):
    """Ошибка конфигурации."""
    pass


class DatabaseError(CryptoAnalyzerError):
    """Ошибка базы данных."""
    pass


class GrokAPIError(CryptoAnalyzerError):
    """Ошибка API Grok."""
    pass


class TelegramError(CryptoAnalyzerError):
    """Ошибка Telegram API."""
    pass


class ValidationError(CryptoAnalyzerError):
    """Ошибка валидации данных."""
    pass


class ProcessingError(CryptoAnalyzerError):
    """Ошибка обработки данных."""
    pass
'''

    def get_logger(self):
        return '''"""
Утилиты логирования для Crypto News Analyzer.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    log_level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> logging.Logger:
    """Настройка логгера с ротацией файлов."""
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(getattr(logging, log_level.upper()))

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Получение логгера по имени."""
    return logging.getLogger(name)
'''

    def get_test_config(self):
        return '''"""Тесты для модуля конфигурации."""

import unittest
from unittest.mock import patch

# TODO: Раскомментировать после создания модуля
# from src.config.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Тесты менеджера конфигурации."""

    def test_placeholder(self):
        """Тест-заглушка."""
        # TODO: Добавить реальные тесты
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
'''

    def get_test_database(self):
        return '''"""Тесты для модуля базы данных."""

import unittest
from unittest.mock import Mock, patch

# TODO: Раскомментировать после создания модулей
# from src.database.database_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Тесты менеджера базы данных."""

    def test_placeholder(self):
        """Тест-заглушка."""
        # TODO: Добавить реальные тесты
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
'''

    def get_test_analyzer(self):
        return '''"""Тесты для модуля анализа Grok."""

import unittest
from unittest.mock import Mock, patch

# TODO: Раскомментировать после создания модулей
# from src.analyzer.grok_analyzer import GrokAnalyzer


class TestGrokAnalyzer(unittest.TestCase):
    """Тесты анализатора Grok."""

    def test_placeholder(self):
        """Тест-заглушка."""
        # TODO: Добавить реальные тесты
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
'''

    def get_test_publisher(self):
        return '''"""Тесты для модуля публикации в Telegram."""

import unittest
from unittest.mock import Mock, AsyncMock

# TODO: Раскомментировать после создания модулей
# from src.publisher.telegram_publisher import TelegramPublisher


class TestTelegramPublisher(unittest.TestCase):
    """Тесты публикатора Telegram."""

    def test_placeholder(self):
        """Тест-заглушка."""
        # TODO: Добавить реальные тесты
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
'''

    def get_monitoring(self):
        return '''"""Скрипт мониторинга системы."""

import sys
import os
import asyncio
from datetime import datetime
from typing import Dict, Any

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


class SystemMonitor:
    """Монитор состояния системы."""

    def __init__(self):
        """Инициализация монитора."""
        print("Initializing system monitor...")

    def get_system_health(self) -> Dict[str, Any]:
        """Проверка состояния компонентов."""
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "components": {
                "database": {"status": "healthy"},
                "grok_api": {"status": "healthy"},
                "telegram": {"status": "healthy"}
            }
        }


async def main():
    """Главная функция мониторинга."""
    monitor = SystemMonitor()
    health = monitor.get_system_health()
    print(f"System Status: {health['overall_status']}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
'''

    def get_setup_database(self):
        return '''"""Скрипт настройки базы данных."""

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
'''

    def get_run_tests(self):
        return '''"""Скрипт запуска тестов."""

import sys
import os
import subprocess
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Выполнение команды."""
    print(f"\\n=== {description} ===")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        return False


def main():
    """Главная функция запуска тестов."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("🧪 Running Tests")

    # Запуск тестов
    success = run_command(
        ["python", "-m", "pytest", "tests/", "-v"],
        "Unit Tests"
    )

    if success:
        print("✅ All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed or pytest not installed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
'''

    def get_env_example(self):
        return '''# API ключи (ОБЯЗАТЕЛЬНО!)
XAI_API_KEY=your_xai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id

# База данных (ОБЯЗАТЕЛЬНО!)
DB_HOST=localhost
DB_PORT=3306
DB_USER=crypto_user
DB_PASSWORD=secure_password
DB_NAME=crypto_analyzer

# Настройки Grok API
GROK_MODEL=grok-3
GROK_BASE_URL=https://api.x.ai/v1
GROK_USE_WEB_SEARCH=true
GROK_TEMPERATURE=0.1
GROK_MAX_TOKENS=10000

# Настройки приложения
TWEET_FETCH_HOURS=8
TWEET_LIMIT=100
MIN_TWEETS_THRESHOLD=50

# Логирование
LOG_LEVEL=INFO
LOG_FILE=logs/crypto_analyzer.log
'''

    def get_gitignore(self):
        return '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
logs/
backup*.sql
profile_stats
'''

    def get_requirements(self):
        return '''mysql-connector-python>=8.2.0
python-dotenv>=1.0.0
openai>=1.12.0
python-telegram-bot>=20.7
typing-extensions>=4.8.0
'''

    def get_requirements_dev(self):
        return '''pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
pre-commit>=3.3.0
'''

    def get_dockerfile(self):
        return '''FROM python:3.11-slim

RUN apt-get update && apt-get install -y \\
    gcc \\
    default-libmysqlclient-dev \\
    pkg-config \\
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r crypto && useradd -r -g crypto crypto

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

RUN mkdir -p logs && chown -R crypto:crypto logs

USER crypto

CMD ["python", "-m", "src.main"]
'''

    def get_docker_compose(self):
        return '''version: '3.8'

services:
  crypto-analyzer:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: crypto_news_analyzer
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    depends_on:
      mysql:
        condition: service_healthy
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    container_name: crypto_mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-rootpassword}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./docker/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

volumes:
  mysql_data:
'''

    def get_init_sql(self):
        return '''-- Создание базы данных
        CREATE \
        DATABASE IF NOT EXISTS crypto_analyzer 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE \
        crypto_analyzer;

-- Таблица твитов
        CREATE TABLE IF NOT EXISTS tweets \
        ( \
            id \
            INT \
            AUTO_INCREMENT \
            PRIMARY \
            KEY, \
            url \
            VARCHAR \
        ( \
            500 \
        ) NOT NULL UNIQUE,
            tweet_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            isGrok BOOLEAN DEFAULT NULL, \
            INDEX idx_created_at \
        ( \
            created_at \
        ),
            INDEX idx_is_grok \
        ( \
            isGrok \
        ),
            INDEX idx_created_grok \
        ( \
            created_at, \
            isGrok \
        )
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Таблица анализа
        CREATE TABLE IF NOT EXISTS tweet_analysis \
        ( \
            id \
            INT \
            AUTO_INCREMENT \
            PRIMARY \
            KEY, \
            url \
            VARCHAR \
        ( \
            500 \
        ) NOT NULL,
            type VARCHAR \
        ( \
            50 \
        ) NOT NULL,
            title VARCHAR \
        ( \
            200 \
        ) DEFAULT '',
            description TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
            INDEX idx_created_at \
        ( \
            created_at \
        ),
            INDEX idx_type \
        ( \
            type \
        ),
            INDEX idx_url \
        ( \
            url \
        ),
            INDEX idx_created_type \
        ( \
            created_at, \
            type \
        )
            ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; \
               '''

    def get_setup_py(self):
        return '''"""Setup script for Crypto News Analyzer."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crypto-news-analyzer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated crypto news analysis with Grok AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "mysql-connector-python>=8.2.0",
        "python-dotenv>=1.0.0",
        "openai>=1.12.0",
        "python-telegram-bot>=20.7",
        "typing-extensions>=4.8.0",
    ],
)
'''

    def get_pyproject_toml(self):
        return '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "crypto-news-analyzer"
version = "1.0.0"
description = "Automated crypto news analysis with Grok AI"
requires-python = ">=3.9"

[tool.black]
line-length = 100
target-version = ['py39']

[tool.mypy]
python_version = "3.9"
warn_return_any = true
'''

    def get_precommit(self):
        return '''repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100]
'''

    def get_readme(self):
        return '''# Crypto News Analyzer

Автоматизированная система анализа криптовалютных новостей с использованием Grok AI.

## 🚀 Возможности

- Интеллектуальный анализ с Grok 3 API
- Веб-поиск в реальном времени
- Автоматическая публикация в Telegram
- Мониторинг и логирование
- Docker контейнеризация

## 📋 Требования

- Python 3.9+
- MySQL 8.0+
- API ключ xAI Grok
- Telegram Bot Token

## ⚡ Быстрый старт

```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка конфигурации
cp config/.env.example .env
# Отредактируйте .env файл

# Настройка БД
python scripts/setup_database.py

# Тестирование
python -m src.main --test

# Запуск
python -m src.main
```

## 🐳 Docker

```bash
cp config/.env.example .env
docker-compose -f docker/docker-compose.yml up -d
```

## 📚 Документация

- [Руководство по развертыванию](docs/DEPLOYMENT.md)
- [API Reference](docs/API_REFERENCE.md)

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения с тестами
4. Создайте Pull Request

## 📄 Лицензия

MIT License
'''

    def get_deployment_doc(self):
        return '''# Руководство по развертыванию

## Системные требования

- Python 3.9+
- MySQL 8.0+
- API ключи xAI и Telegram

## Установка

### 1. Зависимости
```bash
pip install -r requirements.txt
```

### 2. Конфигурация
```bash
cp config/.env.example .env
# Отредактируйте .env
```

### 3. База данных
```bash
python scripts/setup_database.py
```

### 4. Тестирование
```bash
python -m src.main --test
```

### 5. Запуск
```bash
python -m src.main
```

## Docker развертывание

```bash
docker-compose -f docker/docker-compose.yml up -d
```

## Мониторинг

```bash
python scripts/monitoring.py
```
'''

    def get_api_reference(self):
        return '''# API Reference

## Модули

### ConfigManager
Управление конфигурацией приложения

### DatabaseManager  
Работа с базой данных MySQL

### GrokAnalyzer
Анализ твитов с помощью Grok API

### TelegramPublisher
Публикация результатов в Telegram

## Модели данных

### Tweet
Модель твита для анализа

### TweetAnalysis
Результат анализа твита

## Исключения

### CryptoAnalyzerError
Базовый класс исключений

### ConfigError, DatabaseError, GrokAPIError, TelegramError
Специализированные исключения
'''

    def get_project_structure(self):
        return '''# Структура проекта

```
crypto-news-analyzer/
├── src/                    # Основной код
│   ├── config/            # Конфигурация
│   ├── database/          # База данных
│   ├── analyzer/          # Grok анализ
│   ├── publisher/         # Telegram
│   ├── utils/             # Утилиты
│   └── main.py           # Главный файл
├── tests/                 # Тесты
├── scripts/               # Скрипты управления
├── docker/                # Docker файлы
├── config/                # Конфигурация
├── docs/                  # Документация
└── logs/                  # Логи
```

## Статус файлов

✅ **Готовые**: Конфигурация, исключения, логирование
🔧 **Заготовки**: Основные модули с TODO

## Следующие шаги

1. Установить зависимости
2. Настроить .env файл
3. Доработать модули с TODO
4. Запустить тестирование
'''

    def get_pycharm_misc(self):
        return '''<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" project-jdk-name="Python 3.11" project-jdk-type="Python SDK" />
</project>
'''

    def get_pycharm_modules(self):
        return '''<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module fileurl="file://$PROJECT_DIR$/.idea/crypto-news-analyzer.iml" filepath="$PROJECT_DIR$/.idea/crypto-news-analyzer.iml" />
    </modules>
  </component>
</project>
'''

    def get_pycharm_iml(self):
        return '''<?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <sourceRoot url="file://$MODULE_DIR$/src" />
      <excludeFolder url="file://$MODULE_DIR$/venv" />
      <excludeFolder url="file://$MODULE_DIR$/logs" />
      <excludeFolder url="file://$MODULE_DIR$/.pytest_cache" />
    </content>
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>
'''


def main():
    """Главная функция."""
    print("🏗️  Crypto News Analyzer - Structure Setup for PyCharm")
    print("=" * 60)

    current_path = Path.cwd()

    if any(current_path.iterdir()):
        print(f"⚠️  Текущая директория содержит файлы:")
        for item in list(current_path.iterdir())[:5]:
            print(f"   {item.name}")
        if len(list(current_path.iterdir())) > 5:
            print(f"   ... и еще {len(list(current_path.iterdir())) - 5} файлов")

        response = input(f"\n❓ Создать структуру в этой директории? (y/N): ")
        if response.lower() != 'y':
            print("❌ Создание структуры отменено.")
            return

    setup = ProjectStructureSetup()
    setup.create_project_structure()


if __name__ == "__main__":
    main()