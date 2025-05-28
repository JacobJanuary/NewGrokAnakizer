import sys
import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.config_manager import ConfigManager
from database.database_manager import DatabaseManager
from analyzer.grok_analyzer import GrokAnalyzer
from publisher.telegram_publisher import TelegramPublisher
from utils.logger import setup_logger


class SystemMonitor:
    """Монитор состояния системы."""
    
    def __init__(self):
        """Инициализация монитора."""
        self.config_manager = ConfigManager()
        self.logger = setup_logger(__name__, log_level="INFO")
        
        # Инициализация компонентов
        self.db_manager = DatabaseManager(self.config_manager.get_database_config())
        self.grok_analyzer = GrokAnalyzer(self.config_manager.get_grok_config())
        self.telegram_publisher = TelegramPublisher(self.config_manager.get_telegram_config())
    
    def get_system_health(self) -> Dict[str, Any]:
        """
        Проверка состояния всех компонентов системы.
        
        Returns:
            Словарь с результатами проверки
        """
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "components": {}
        }
        
        # Проверка базы данных
        try:
            db_healthy = self.db_manager.test_connection()
            health_status["components"]["database"] = {
                "status": "healthy" if db_healthy else "unhealthy",
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            health_status["components"]["database"] = {
                "status": "error",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
            health_status["overall_status"] = "unhealthy"
        
        # Проверка Grok API
        try:
            grok_healthy = self.grok_analyzer.test_connection()
            health_status["components"]["grok_api"] = {
                "status": "healthy" if grok_healthy else "unhealthy",
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            health_status["components"]["grok_api"] = {
                "status": "error",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
            health_status["overall_status"] = "unhealthy"
        
        return health_status
    
    async def get_telegram_status(self) -> Dict[str, Any]:
        """Проверка состояния Telegram бота."""
        try:
            bot_info = await self.telegram_publisher.get_bot_info()
            test_result = await self.telegram_publisher.send_test_message()
            
            return {
                "status": "healthy" if test_result else "unhealthy",
                "bot_info": bot_info,
                "test_message_sent": test_result,
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
    
    def get_processing_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """
        Получение статистики обработки за указанный период.
        
        Args:
            hours: Период в часах
            
        Returns:
            Статистика обработки
        """
        try:
            stats = self.db_manager.get_analysis_statistics(hours)
            return stats
        except Exception as e:
            self.logger.error(f"Failed to get processing statistics: {e}")
            return {"error": str(e)}
    
    def get_log_analysis(self, hours: int = 24) -> Dict[str, Any]:
        """
        Анализ логов за указанный период.
        
        Args:
            hours: Период в часах
            
        Returns:
            Результаты анализа логов
        """
        log_file = self.config_manager.get_app_config().log_file
        
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            error_count = 0
            warning_count = 0
            info_count = 0
            recent_errors = []
            
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        # Простой парсинг времени из лога
                        time_str = line.split(' - ')[0]
                        log_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S,%f')
                        
                        if log_time >= cutoff_time:
                            if 'ERROR' in line:
                                error_count += 1
                                recent_errors.append(line.strip())
                            elif 'WARNING' in line:
                                warning_count += 1
                            elif 'INFO' in line:
                                info_count += 1
                    except:
                        continue
            
            return {
                "period_hours": hours,
                "error_count": error_count,
                "warning_count": warning_count,
                "info_count": info_count,
                "recent_errors": recent_errors[-10:],  # Последние 10 ошибок
                "total_entries": error_count + warning_count + info_count
            }
            
        except FileNotFoundError:
            return {"error": f"Log file not found: {log_file}"}
        except Exception as e:
            return {"error": f"Failed to analyze logs: {e}"}
    
    async def generate_full_report(self) -> Dict[str, Any]:
        """
        Генерация полного отчета о состоянии системы.
        
        Returns:
            Полный отчет
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "system_health": self.get_system_health(),
            "telegram_status": await self.get_telegram_status(),
            "processing_stats_24h": self.get_processing_statistics(24),
            "processing_stats_7d": self.get_processing_statistics(24 * 7),
            "log_analysis_24h": self.get_log_analysis(24),
            "log_analysis_7d": self.get_log_analysis(24 * 7)
        }
        
        return report
    
    def print_health_summary(self, health_data: Dict[str, Any]) -> None:
        """Печать краткого отчета о здоровье системы."""
        print(f"\n=== System Health Report ===")
        print(f"Generated: {health_data.get('generated_at', 'Unknown')}")
        print(f"Overall Status: {health_data.get('system_health', {}).get('overall_status', 'Unknown').upper()}")
        
        print(f"\n--- Component Status ---")
        components = health_data.get('system_health', {}).get('components', {})
        for name, info in components.items():
            status = info.get('status', 'unknown').upper()
            print(f"{name}: {status}")
            if 'error' in info:
                print(f"  Error: {info['error']}")
        
        # Telegram статус
        telegram_status = health_data.get('telegram_status', {})
        print(f"\nTelegram Bot: {telegram_status.get('status', 'unknown').upper()}")
        
        # Статистика обработки за 24 часа
        stats_24h = health_data.get('processing_stats_24h', {})
        if 'general' in stats_24h:
            general = stats_24h['general']
            print(f"\n--- Processing Stats (24h) ---")
            print(f"Total processed: {general.get('total_processed', 0)}")
            print(f"Valuable tweets: {general.get('valuable', 0)}")
            print(f"Spam/Flood: {general.get('spam', 0) + general.get('flood', 0)}")
        
        # Анализ логов
        log_analysis = health_data.get('log_analysis_24h', {})
        if 'error_count' in log_analysis:
            print(f"\n--- Log Analysis (24h) ---")
            print(f"Errors: {log_analysis.get('error_count', 0)}")
            print(f"Warnings: {log_analysis.get('warning_count', 0)}")
            print(f"Total entries: {log_analysis.get('total_entries', 0)}")
        
        print("=" * 30)
    
    async def send_report_to_telegram(self, report: Dict[str, Any]) -> bool:
        """
        Отправка отчета в Telegram.
        
        Args:
            report: Данные отчета
            
        Returns:
            True если отправлено успешно
        """
        try:
            # Формируем краткое сообщение
            system_health = report.get('system_health', {})
            overall_status = system_health.get('overall_status', 'unknown')
            
            message_parts = [
                f"*🔍 Отчет о системе* ({datetime.now().strftime('%H:%M')})",
                f"Статус: {'✅' if overall_status == 'healthy' else '❌'} {overall_status.upper()}",
                ""
            ]
            
            # Компоненты
            components = system_health.get('components', {})
            for name, info in components.items():
                status_emoji = "✅" if info.get('status') == 'healthy' else "❌"
                message_parts.append(f"{status_emoji} {name.replace('_', ' ').title()}")
            
            # Статистика за 24 часа
            stats = report.get('processing_stats_24h', {})
            if 'general' in stats:
                general = stats['general']
                message_parts.extend([
                    "",
                    "*📊 Статистика (24ч):*",
                    f"Обработано: {general.get('total_processed', 0)}",
                    f"Ценных: {general.get('valuable', 0)}",
                    f"Спам/Шум: {general.get('spam', 0) + general.get('flood', 0)}"
                ])
            
            # Ошибки
            log_analysis = report.get('log_analysis_24h', {})
            if log_analysis.get('error_count', 0) > 0:
                message_parts.extend([
                    "",
                    f"⚠️ Ошибок за 24ч: {log_analysis['error_count']}"
                ])
            
            message = "\n".join(message_parts)
            
            # Экранируем для Markdown V2
            escaped_message = self.telegram_publisher._escape_markdown_v2(message)
            
            await self.telegram_publisher.bot.send_message(
                chat_id=self.telegram_publisher.config.channel_id,
                text=escaped_message,
                parse_mode="MarkdownV2"
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send report to Telegram: {e}")
            return False


async def main():
    """Главная функция мониторинга."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Crypto News Analyzer System Monitor')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--telegram', action='store_true', help='Send report to Telegram')
    parser.add_argument('--hours', type=int, default=24, help='Hours to analyze (default: 24)')
    parser.add_argument('--full', action='store_true', help='Generate full report')
    
    args = parser.parse_args()
    
    monitor = SystemMonitor()
    
    try:
        if args.full:
            # Полный отчет
            report = await monitor.generate_full_report()
            
            if args.json:
                print(json.dumps(report, indent=2, ensure_ascii=False))
            else:
                monitor.print_health_summary(report)
            
            if args.telegram:
                success = await monitor.send_report_to_telegram(report)
                if success:
                    print("✅ Report sent to Telegram")
                else:
                    print("❌ Failed to send report to Telegram")
        
        else:
            # Быстрая проверка
            health = monitor.get_system_health()
            
            if args.json:
                print(json.dumps(health, indent=2, ensure_ascii=False))
            else:
                print(f"System Status: {health['overall_status'].upper()}")
                for name, info in health['components'].items():
                    status = info['status']
                    print(f"  {name}: {status}")
    
    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user")
    except Exception as e:
        print(f"Monitoring failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))