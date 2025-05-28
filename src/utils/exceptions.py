"""
Расширенные исключения для Crypto News Analyzer.
Включают контекстную информацию, коды ошибок и возможности восстановления.
"""

import sys
import traceback
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime
import logging

"""
Исправление: добавляем недостающие коды ошибок и исправляем существующие.
Замените только класс ErrorCode в src/utils/exceptions.py
"""


class ErrorCode(Enum):
    """Коды ошибок для категоризации проблем."""

    # Конфигурация (1000-1099)
    CONFIG_MISSING_ENV_VAR = 1001
    CONFIG_INVALID_VALUE = 1002
    CONFIG_FILE_NOT_FOUND = 1003
    CONFIG_PARSE_ERROR = 1004

    # База данных (1100-1199)
    DB_CONNECTION_FAILED = 1101
    DB_QUERY_FAILED = 1102
    DB_TRANSACTION_FAILED = 1103
    DB_SCHEMA_ERROR = 1104
    DB_TIMEOUT = 1105
    DB_CONSTRAINT_VIOLATION = 1106

    # Grok API (1200-1299)
    GROK_AUTH_FAILED = 1201
    GROK_RATE_LIMITED = 1202
    GROK_QUOTA_EXCEEDED = 1203
    GROK_INVALID_RESPONSE = 1204
    GROK_JSON_PARSE_ERROR = 1205
    GROK_MODEL_ERROR = 1206
    GROK_NETWORK_ERROR = 1207
    GROK_TIMEOUT = 1208  # ИСПРАВЛЕНИЕ: добавляем отсутствующий код
    GROK_CONNECTION_ERROR = 1209  # ДОПОЛНИТЕЛЬНО: для ошибок соединения

    # Telegram (1300-1399)
    TELEGRAM_AUTH_FAILED = 1301
    TELEGRAM_CHAT_NOT_FOUND = 1302
    TELEGRAM_MESSAGE_TOO_LONG = 1303
    TELEGRAM_RATE_LIMITED = 1304
    TELEGRAM_BOT_BLOCKED = 1305
    TELEGRAM_NETWORK_ERROR = 1306
    TELEGRAM_TIMEOUT = 1307  # ДОПОЛНИТЕЛЬНО: для таймаутов Telegram

    # Валидация (1400-1499)
    VALIDATION_INVALID_DATA = 1401
    VALIDATION_MISSING_FIELD = 1402
    VALIDATION_TYPE_ERROR = 1403
    VALIDATION_RANGE_ERROR = 1404

    # Обработка (1500-1599)
    PROCESSING_INSUFFICIENT_DATA = 1501
    PROCESSING_TIMEOUT = 1502
    PROCESSING_MEMORY_ERROR = 1503
    PROCESSING_THREAD_ERROR = 1504

    # Общие ошибки (1900-1999)
    UNKNOWN_ERROR = 1999


class ErrorSeverity(Enum):
    """Уровни серьезности ошибок."""

    LOW = "low"          # Незначительные ошибки, система продолжает работу
    MEDIUM = "medium"    # Умеренные ошибки, частичная потеря функциональности
    HIGH = "high"        # Серьезные ошибки, значительная потеря функциональности
    CRITICAL = "critical"  # Критические ошибки, полная остановка системы


class CryptoAnalyzerError(Exception):
    """
    Базовый класс исключений для анализатора с расширенной функциональностью.

    Attributes:
        code: Код ошибки из ErrorCode
        severity: Уровень серьезности ошибки
        context: Дополнительная контекстная информация
        original_error: Исходное исключение (если есть)
        timestamp: Время возникновения ошибки
        suggestions: Предложения по исправлению
        retry_possible: Возможность повторной попытки
    """

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None,
        suggestions: Optional[List[str]] = None,
        retry_possible: bool = False
    ):
        """
        Инициализация расширенного исключения.

        Args:
            message: Основное сообщение об ошибке
            code: Код ошибки для категоризации
            severity: Уровень серьезности
            context: Дополнительная информация о контексте
            original_error: Исходное исключение
            suggestions: Предложения по исправлению
            retry_possible: Можно ли повторить операцию
        """
        super().__init__(message)

        self.code = code
        self.severity = severity
        self.context = context or {}
        self.original_error = original_error
        self.timestamp = datetime.now()
        self.suggestions = suggestions or []
        self.retry_possible = retry_possible

        # Информация о месте ошибки
        self.traceback_info = self._get_traceback_info()

    def _get_traceback_info(self) -> Dict[str, str]:
        """Получение информации о трассировке стека."""
        frame = sys._getframe(2)  # Поднимаемся на 2 уровня выше
        return {
            'filename': frame.f_code.co_filename,
            'function': frame.f_code.co_name,
            'line_number': frame.f_lineno
        }

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование исключения в словарь для логирования."""
        return {
            'error_type': self.__class__.__name__,
            'message': str(self),
            'code': self.code.value,
            'code_name': self.code.name,
            'severity': self.severity.value,
            'timestamp': self.timestamp.isoformat(),
            'context': self.context,
            'suggestions': self.suggestions,
            'retry_possible': self.retry_possible,
            'traceback': {
                'filename': self.traceback_info['filename'],
                'function': self.traceback_info['function'],
                'line_number': self.traceback_info['line_number']
            },
            'original_error': str(self.original_error) if self.original_error else None
        }

    def log_error(self, logger: logging.Logger) -> None:
        """Логирование ошибки с полной информацией."""
        error_dict = self.to_dict()

        log_message = (
            f"[{self.code.name}] {str(self)} "
            f"(Severity: {self.severity.value})"
        )

        if self.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message, extra={'error_details': error_dict})
        elif self.severity == ErrorSeverity.HIGH:
            logger.error(log_message, extra={'error_details': error_dict})
        elif self.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message, extra={'error_details': error_dict})
        else:
            logger.info(log_message, extra={'error_details': error_dict})

    def get_user_message(self) -> str:
        """Получение пользовательского сообщения об ошибке."""
        base_message = str(self)

        if self.suggestions:
            suggestions_text = "\n".join([f"• {s}" for s in self.suggestions])
            base_message += f"\n\nПредложения по исправлению:\n{suggestions_text}"

        if self.retry_possible:
            base_message += "\n\n🔄 Операцию можно повторить."

        return base_message

    def __str__(self) -> str:
        """Строковое представление ошибки."""
        base_str = super().__str__()
        return f"{base_str} [Code: {self.code.value}]"


class ConfigError(CryptoAnalyzerError):
    """Ошибки конфигурации с автоматическими предложениями."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.CONFIG_INVALID_VALUE,
        missing_vars: Optional[List[str]] = None,
        invalid_values: Optional[Dict[str, str]] = None,
        **kwargs
    ):
        """
        Инициализация ошибки конфигурации.

        Args:
            message: Сообщение об ошибке
            code: Код ошибки конфигурации
            missing_vars: Список отсутствующих переменных
            invalid_values: Словарь невалидных значений
        """
        context = kwargs.get('context', {})
        suggestions = kwargs.get('suggestions', [])

        # Автоматические контекст и предложения
        if missing_vars:
            context['missing_variables'] = missing_vars
            suggestions.extend([
                f"Добавьте переменную {var} в .env файл" for var in missing_vars
            ])
            suggestions.append("Проверьте файл config/.env.example для примера")

        if invalid_values:
            context['invalid_values'] = invalid_values
            suggestions.extend([
                f"Исправьте значение {key}: {value}" for key, value in invalid_values.items()
            ])

        kwargs.update({
            'code': code,
            'severity': ErrorSeverity.HIGH,
            'context': context,
            'suggestions': suggestions,
            'retry_possible': True
        })

        super().__init__(message, **kwargs)


class DatabaseError(CryptoAnalyzerError):
    """Ошибки базы данных с диагностической информацией."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.DB_CONNECTION_FAILED,
        query: Optional[str] = None,
        params: Optional[tuple] = None,
        connection_info: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Инициализация ошибки базы данных.

        Args:
            message: Сообщение об ошибке
            code: Код ошибки БД
            query: SQL запрос (если есть)
            params: Параметры запроса
            connection_info: Информация о подключении
        """
        context = kwargs.get('context', {})
        suggestions = kwargs.get('suggestions', [])

        # Добавляем диагностическую информацию
        if query:
            context['query'] = query[:200] + '...' if len(query) > 200 else query
        if params:
            context['params'] = str(params)[:100] + '...' if len(str(params)) > 100 else str(params)
        if connection_info:
            context['connection'] = connection_info

        # Автоматические предложения по коду ошибки
        if code == ErrorCode.DB_CONNECTION_FAILED:
            suggestions.extend([
                "Проверьте, что MySQL сервер запущен",
                "Убедитесь в правильности параметров подключения в .env",
                "Проверьте права пользователя базы данных",
                "Убедитесь, что порт 3306 доступен"
            ])
        elif code == ErrorCode.DB_QUERY_FAILED:
            suggestions.extend([
                "Проверьте синтаксис SQL запроса",
                "Убедитесь в существовании таблиц и столбцов",
                "Проверьте права на выполнение операции"
            ])
        elif code == ErrorCode.DB_TIMEOUT:
            suggestions.extend([
                "Увеличьте timeout в настройках подключения",
                "Оптимизируйте медленные запросы",
                "Проверьте загрузку сервера БД"
            ])

        kwargs.update({
            'code': code,
            'severity': ErrorSeverity.HIGH,
            'context': context,
            'suggestions': suggestions,
            'retry_possible': code != ErrorCode.DB_SCHEMA_ERROR
        })

        super().__init__(message, **kwargs)


class GrokAPIError(CryptoAnalyzerError):
    """Ошибки Grok API с анализом ответов."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.GROK_INVALID_RESPONSE,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Инициализация ошибки Grok API.

        Args:
            message: Сообщение об ошибке
            code: Код ошибки API
            status_code: HTTP статус код
            response_data: Данные ответа API
            request_data: Данные запроса
        """
        context = kwargs.get('context', {})
        suggestions = kwargs.get('suggestions', [])

        # Добавляем информацию о запросе/ответе
        if status_code:
            context['http_status'] = status_code
        if response_data:
            context['response'] = str(response_data)[:500] + '...' if len(str(response_data)) > 500 else response_data
        if request_data:
            # Скрываем API ключ в логах
            safe_request = request_data.copy()
            if 'api_key' in safe_request:
                safe_request['api_key'] = '***HIDDEN***'
            context['request'] = safe_request

        # Специфичные предложения по кодам ошибок
        if code == ErrorCode.GROK_AUTH_FAILED:
            suggestions.extend([
                "Проверьте правильность XAI_API_KEY в .env файле",
                "Убедитесь, что API ключ не истек",
                "Проверьте остаток кредитов на console.x.ai"
            ])
        elif code == ErrorCode.GROK_RATE_LIMITED:
            suggestions.extend([
                "Уменьшите частоту запросов к API",
                "Реализуйте exponential backoff",
                "Проверьте лимиты на console.x.ai"
            ])
        elif code == ErrorCode.GROK_QUOTA_EXCEEDED:
            suggestions.extend([
                "Пополните баланс кредитов xAI",
                "Уменьшите количество токенов в запросах",
                "Оптимизируйте системный промпт"
            ])
        elif code == ErrorCode.GROK_JSON_PARSE_ERROR:
            suggestions.extend([
                "Обновите системный промпт для принуждения к JSON",
                "Добавьте response_format: json_object в запрос",
                "Реализуйте парсинг JSON из смешанного текста"
            ])

        # Определяем возможность повтора
        retry_possible = code in [
            ErrorCode.GROK_RATE_LIMITED,
            ErrorCode.GROK_NETWORK_ERROR,
            ErrorCode.GROK_TIMEOUT
        ]

        kwargs.update({
            'code': code,
            'severity': ErrorSeverity.MEDIUM if retry_possible else ErrorSeverity.HIGH,
            'context': context,
            'suggestions': suggestions,
            'retry_possible': retry_possible
        })

        super().__init__(message, **kwargs)


class TelegramError(CryptoAnalyzerError):
    """Ошибки Telegram API с диагностикой."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.TELEGRAM_NETWORK_ERROR,
        telegram_error_code: Optional[int] = None,
        chat_info: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Инициализация ошибки Telegram.

        Args:
            message: Сообщение об ошибке
            code: Код ошибки Telegram
            telegram_error_code: Код ошибки от Telegram API
            chat_info: Информация о чате
        """
        context = kwargs.get('context', {})
        suggestions = kwargs.get('suggestions', [])

        # Добавляем Telegram-специфичную информацию
        if telegram_error_code:
            context['telegram_error_code'] = telegram_error_code
        if chat_info:
            context['chat_info'] = chat_info

        # Предложения по кодам ошибок
        if code == ErrorCode.TELEGRAM_AUTH_FAILED:
            suggestions.extend([
                "Проверьте правильность TELEGRAM_BOT_TOKEN",
                "Убедитесь, что бот не заблокирован",
                "Создайте нового бота через @BotFather"
            ])
        elif code == ErrorCode.TELEGRAM_CHAT_NOT_FOUND:
            suggestions.extend([
                "Проверьте правильность TELEGRAM_CHANNEL_ID",
                "Убедитесь, что бот добавлен в канал как администратор",
                "Отправьте любое сообщение в канал для активации"
            ])
        elif code == ErrorCode.TELEGRAM_MESSAGE_TOO_LONG:
            suggestions.extend([
                "Разбейте сообщение на несколько частей",
                "Сократите описания твитов",
                "Оптимизируйте форматирование сообщений"
            ])
        elif code == ErrorCode.TELEGRAM_BOT_BLOCKED:
            suggestions.extend([
                "Пользователь заблокировал бота",
                "Проверьте настройки приватности канала",
                "Создайте нового бота и обновите токен"
            ])

        kwargs.update({
            'code': code,
            'severity': ErrorSeverity.MEDIUM,
            'context': context,
            'suggestions': suggestions,
            'retry_possible': code != ErrorCode.TELEGRAM_BOT_BLOCKED
        })

        super().__init__(message, **kwargs)


class ValidationError(CryptoAnalyzerError):
    """Ошибки валидации данных с детальной информацией."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.VALIDATION_INVALID_DATA,
        field_name: Optional[str] = None,
        invalid_value: Optional[Any] = None,
        expected_type: Optional[type] = None,
        **kwargs
    ):
        """
        Инициализация ошибки валидации.

        Args:
            message: Сообщение об ошибке
            code: Код ошибки валидации
            field_name: Имя поля с ошибкой
            invalid_value: Невалидное значение
            expected_type: Ожидаемый тип данных
        """
        context = kwargs.get('context', {})
        suggestions = kwargs.get('suggestions', [])

        # Добавляем информацию о валидации
        if field_name:
            context['field_name'] = field_name
        if invalid_value is not None:
            context['invalid_value'] = str(invalid_value)[:100]
        if expected_type:
            context['expected_type'] = expected_type.__name__

        # Автоматические предложения
        if field_name and expected_type:
            suggestions.append(f"Поле '{field_name}' должно быть типа {expected_type.__name__}")
        if invalid_value is not None:
            suggestions.append(f"Получено значение: {invalid_value}")

        kwargs.update({
            'code': code,
            'severity': ErrorSeverity.LOW,
            'context': context,
            'suggestions': suggestions,
            'retry_possible': True
        })

        super().__init__(message, **kwargs)


class ProcessingError(CryptoAnalyzerError):
    """Ошибки обработки данных с метриками производительности."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.PROCESSING_TIMEOUT,
        processing_time: Optional[float] = None,
        data_size: Optional[int] = None,
        memory_usage: Optional[int] = None,
        **kwargs
    ):
        """
        Инициализация ошибки обработки.

        Args:
            message: Сообщение об ошибке
            code: Код ошибки обработки
            processing_time: Время обработки в секундах
            data_size: Размер обрабатываемых данных
            memory_usage: Использование памяти в байтах
        """
        context = kwargs.get('context', {})
        suggestions = kwargs.get('suggestions', [])

        # Добавляем метрики производительности
        if processing_time is not None:
            context['processing_time_seconds'] = processing_time
        if data_size is not None:
            context['data_size'] = data_size
        if memory_usage is not None:
            context['memory_usage_bytes'] = memory_usage

        # Предложения по оптимизации
        if code == ErrorCode.PROCESSING_TIMEOUT:
            suggestions.extend([
                "Увеличьте timeout для обработки",
                "Разбейте данные на меньшие батчи",
                "Оптимизируйте алгоритм обработки"
            ])
        elif code == ErrorCode.PROCESSING_MEMORY_ERROR:
            suggestions.extend([
                "Уменьшите размер батча данных",
                "Используйте генераторы вместо списков",
                "Очищайте неиспользуемые объекты"
            ])
        elif code == ErrorCode.PROCESSING_INSUFFICIENT_DATA:
            suggestions.extend([
                "Проверьте источники данных",
                "Увеличьте период сбора данных",
                "Используйте флаг --force для принудительного запуска"
            ])

        kwargs.update({
            'code': code,
            'severity': ErrorSeverity.MEDIUM,
            'context': context,
            'suggestions': suggestions,
            'retry_possible': code != ErrorCode.PROCESSING_MEMORY_ERROR
        })

        super().__init__(message, **kwargs)


# Утилитарные функции для работы с исключениями
def handle_exception(
    error: Exception,
    logger: logging.Logger,
    context: Optional[Dict[str, Any]] = None
) -> CryptoAnalyzerError:
    """
    Обработка и конвертация обычных исключений в CryptoAnalyzerError.

    Args:
        error: Исходное исключение
        logger: Логгер для записи ошибки
        context: Дополнительный контекст

    Returns:
        Конвертированное исключение CryptoAnalyzerError
    """
    if isinstance(error, CryptoAnalyzerError):
        error.log_error(logger)
        return error

    # Конвертируем стандартные исключения
    if isinstance(error, ValueError):
        converted = ValidationError(
            str(error),
            code=ErrorCode.VALIDATION_INVALID_DATA,
            original_error=error,
            context=context
        )
    elif isinstance(error, ConnectionError):
        converted = DatabaseError(
            str(error),
            code=ErrorCode.DB_CONNECTION_FAILED,
            original_error=error,
            context=context
        )
    elif isinstance(error, TimeoutError):
        converted = ProcessingError(
            str(error),
            code=ErrorCode.PROCESSING_TIMEOUT,
            original_error=error,
            context=context
        )
    else:
        converted = CryptoAnalyzerError(
            str(error),
            code=ErrorCode.UNKNOWN_ERROR,
            original_error=error,
            context=context
        )

    converted.log_error(logger)
    return converted


def create_error_summary(errors: List[CryptoAnalyzerError]) -> Dict[str, Any]:
    """
    Создание сводки по ошибкам для отчетности.

    Args:
        errors: Список ошибок

    Returns:
        Сводка по ошибкам
    """
    if not errors:
        return {"total": 0, "by_severity": {}, "by_code": {}, "retry_possible": 0}

    summary = {
        "total": len(errors),
        "by_severity": {},
        "by_code": {},
        "retry_possible": sum(1 for e in errors if e.retry_possible),
        "timespan": {
            "first_error": min(e.timestamp for e in errors).isoformat(),
            "last_error": max(e.timestamp for e in errors).isoformat()
        }
    }

    # Группировка по серьезности
    for error in errors:
        severity = error.severity.value
        summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1

    # Группировка по кодам
    for error in errors:
        code = error.code.name
        summary["by_code"][code] = summary["by_code"].get(code, 0) + 1

    return summary