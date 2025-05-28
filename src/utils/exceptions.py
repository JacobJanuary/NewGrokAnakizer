"""
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