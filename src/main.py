"""
Главный модуль Crypto News Analyzer.
"""

import asyncio
import sys
import time
from datetime import datetime
from typing import Optional

from .config.config_manager import ConfigManager
from .database.database_manager import DatabaseManager
from .analyzer.grok_analyzer import GrokAnalyzer
from .publisher.telegram_publisher import TelegramPublisher
from .database.models import AnalysisStats
from .utils.exceptions import (
    ConfigError, DatabaseError, GrokAPIError,
    TelegramError as CustomTelegramError
)
from .utils.logger import setup_logger, get_logger


class CryptoNewsAnalyzer:
    """Главный класс анализатора криптоновостей."""

    def __init__(self, config_file: Optional[str] = None) -> None:
        """
        Инициализация анализатора.

        Args:
            config_file: Путь к файлу конфигурации .env
        """
        # Загружаем конфигурацию
        self.config_manager = ConfigManager(config_file)

        # Настраиваем логирование
        app_config = self.config_manager.get_app_config()
        self.logger = setup_logger(
            name=__name__,
            log_file=app_config.log_file,
            log_level=app_config.log_level
        )

        # Инициализируем компоненты
        self.db_manager = DatabaseManager(self.config_manager.get_database_config())
        self.grok_analyzer = GrokAnalyzer(self.config_manager.get_grok_config())
        self.telegram_publisher = TelegramPublisher(self.config_manager.get_telegram_config())

        self.app_config = app_config

        self.logger.info("CryptoNewsAnalyzer initialized successfully")

    async def run_analysis(self, force_run: bool = False) -> AnalysisStats:
        """
        Основной цикл анализа.

        Args:
            force_run: Принудительный запуск даже при недостатке твитов

        Returns:
            Статистика выполнения

        Raises:
            Exception: При критических ошибках
        """
        start_time = time.time()
        stats = AnalysisStats(
            total_tweets=0,
            processed_tweets=0,
            valuable_tweets=0,
            spam_tweets=0,
            flood_tweets=0,
            duplicate_tweets=0,
            error_count=0,
            processing_time=0.0
        )

        try:
            self.logger.info("Starting crypto news analysis...")

            # Получаем твиты
            tweets, total_found = self.db_manager.get_recent_tweets(
                hours=self.app_config.tweet_fetch_hours,
                limit=self.app_config.tweet_limit
            )

            stats.total_tweets = total_found

            # Проверяем достаточность твитов
            if not tweets:
                self.logger.info("No new tweets found")
                return stats

            if len(tweets) < self.app_config.min_tweets_threshold and not force_run:
                self.logger.warning(f"Only {len(tweets)} tweets found, less than threshold {self.app_config.min_tweets_threshold}")
                return stats

            self.logger.info(f"Processing {len(tweets)} tweets")

            # Помечаем твиты как обрабатываемые
            tweet_ids = [tweet.id for tweet in tweets]
            self.db_manager.mark_tweets_as_processing(tweet_ids)

            # Анализируем твиты
            results = self.grok_analyzer.analyze_tweets(tweets)
            stats.processed_tweets = len(results)

            # Подсчитываем статистику
            for result in results:
                if result.type == "isSpam":
                    stats.spam_tweets += 1
                elif result.type == "isFlood":
                    stats.flood_tweets += 1
                elif result.type == "alreadyPosted":
                    stats.duplicate_tweets += 1
                elif result.is_valuable:
                    stats.valuable_tweets += 1

            # Сохраняем результаты
            self.db_manager.save_analysis_results(tweets, results)

            # Публикуем в Telegram если есть ценные твиты
            if stats.valuable_tweets > 0:
                await self.telegram_publisher.publish_analysis(tweets, results)
                self.logger.info(f"Published {stats.valuable_tweets} valuable tweets")
            else:
                self.logger.info("No valuable tweets to publish")

            stats.processing_time = time.time() - start_time

            self.logger.info(f"Analysis completed successfully in {stats.processing_time:.2f}s")
            self._log_stats(stats)

            return stats

        except Exception as e:
            stats.error_count = 1
            stats.processing_time = time.time() - start_time
            self.logger.error(f"Critical error in run_analysis: {e}")
            raise

    def _log_stats(self, stats: AnalysisStats) -> None:
        """Логирование статистики."""
        self.logger.info(f"=== Analysis Statistics ===")
        self.logger.info(f"Total tweets found: {stats.total_tweets}")
        self.logger.info(f"Processed tweets: {stats.processed_tweets}")
        self.logger.info(f"Valuable tweets: {stats.valuable_tweets}")
        self.logger.info(f"Spam tweets: {stats.spam_tweets}")
        self.logger.info(f"Flood tweets: {stats.flood_tweets}")
        self.logger.info(f"Duplicate tweets: {stats.duplicate_tweets}")
        self.logger.info(f"Success rate: {stats.success_rate:.1f}%")
        self.logger.info(f"Valuable rate: {stats.valuable_rate:.1f}%")
        self.logger.info(f"Processing time: {stats.processing_time:.2f}s")
        self.logger.info("=" * 30)

    async def test_components(self) -> bool:
        """
        Тестирование всех компонентов системы.

        Returns:
            True если все компоненты работают
        """
        self.logger.info("Testing system components...")

        # Тест базы данных
        if not self.db_manager.test_connection():
            self.logger.error("Database connection test failed")
            return False
        self.logger.info("✓ Database connection OK")

        # Тест Grok API
        if not self.grok_analyzer.test_connection():
            self.logger.error("Grok API connection test failed")
            return False
        self.logger.info("✓ Grok API connection OK")

        # Тест Telegram
        if not await self.telegram_publisher.send_test_message():
            self.logger.error("Telegram test message failed")
            return False
        self.logger.info("✓ Telegram bot OK")

        self.logger.info("All components tested successfully")
        return True

    async def send_statistics(self, hours: int = 24) -> None:
        """
        Отправка статистики в Telegram.

        Args:
            hours: Период для статистики
        """
        try:
            stats = self.db_manager.get_analysis_statistics(hours)
            message = self.telegram_publisher.format_statistics_message(stats)

            await self.telegram_publisher.bot.send_message(
                chat_id=self.telegram_publisher.config.channel_id,
                text=message,
                parse_mode="MarkdownV2"
            )

            self.logger.info(f"Statistics for {hours}h sent to Telegram")
        except Exception as e:
            self.logger.error(f"Failed to send statistics: {e}")

    def cleanup_old_data(self, days: int = 30) -> None:
        """
        Очистка старых данных.

        Args:
            days: Количество дней для хранения
        """
        try:
            deleted_count = self.db_manager.cleanup_old_data(days)
            self.logger.info(f"Cleaned up {deleted_count} old records (older than {days} days)")
        except Exception as e:
            self.logger.error(f"Failed to cleanup old data: {e}")


async def main() -> None:
    """
    Главная функция запуска анализатора.

    Raises:
        SystemExit: При критических ошибках конфигурации
    """
    try:
        # Проверяем аргументы командной строки
        force_run = "--force" in sys.argv
        test_mode = "--test" in sys.argv
        send_stats = "--stats" in sys.argv
        cleanup = "--cleanup" in sys.argv

        # Инициализируем анализатор
        analyzer = CryptoNewsAnalyzer()

        if test_mode:
            # Режим тестирования
            success = await analyzer.test_components()
            sys.exit(0 if success else 1)

        if send_stats:
            # Отправка статистики
            await analyzer.send_statistics()
            return

        if cleanup:
            # Очистка старых данных
            analyzer.cleanup_old_data()
            return

        # Основной режим работы
        stats = await analyzer.run_analysis(force_run=force_run)

        # Проверяем успешность выполнения
        if stats.error_count > 0:
            sys.exit(1)

    except ConfigError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except DatabaseError as e:
        print(f"Database error: {e}")
        sys.exit(1)
    except GrokAPIError as e:
        print(f"Grok API error: {e}")
        sys.exit(1)
    except CustomTelegramError as e:
        print(f"Telegram error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())