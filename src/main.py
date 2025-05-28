"""
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
