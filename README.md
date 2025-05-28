# Crypto News Analyzer

Автоматизированная система анализа криптовалютных новостей с использованием Grok AI и публикацией в Telegram.

## 🚀 Возможности

- **Интеллектуальный анализ**: Использует Grok 3 API для анализа твитов и новостей
- **Веб-поиск в реальном времени**: Поддержка Live Search API для актуальной информации
- **Автоматическая классификация**: Разделение на новости, слухи, аналитику, спам и т.д.
- **Публикация в Telegram**: Красивое оформление результатов с эмодзи и ссылками
- **Мониторинг и логирование**: Подробные логи и система мониторинга
- **Масштабируемость**: Docker-контейнеризация и автоматизация

## 📋 Системные требования

- Python 3.9+
- MySQL 8.0+ (или MariaDB 10.6+)
- API ключ xAI Grok
- Telegram Bot Token

## ⚡ Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-username/crypto-news-analyzer.git
cd crypto-news-analyzer
```

### 2. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### 3. Конфигурация
```bash
cp config/.env.example .env
# Отредактируйте .env файл со своими API ключами
```

### 4. Настройка базы данных
```bash
python scripts/setup_database.py --all
```

### 5. Тестирование
```bash
python -m src.main --test
```

### 6. Запуск
```bash
python -m src.main
```

## 🐳 Docker развертывание

```bash
# Настройка конфигурации
cp config/.env.example .env
# Отредактируйте .env

# Запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f crypto-analyzer
```

## 📚 Документация

- **[Руководство по развертыванию](DEPLOYMENT.md)** - Полная инструкция по установке и настройке
- **[API Reference](docs/API_REFERENCE.md)** - Документация по API
- **Примеры использования** в директории `docs/`

## 🛠 Архитектура

```
src/
├── config/          # Управление конфигурацией
├── database/        # Работа с базой данных
├── analyzer/        # Анализ с помощью Grok API
├── publisher/       # Публикация в Telegram
├── utils/           # Утилиты и исключения
└── main.py          # Главный модуль
```

## 🔧 Конфигурация

Основные переменные окружения:

```bash
# API ключи
XAI_API_KEY=your_xai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHANNEL_ID=your_channel_id

# База данных
DB_HOST=localhost
DB_USER=crypto_user
DB_PASSWORD=secure_password
DB_NAME=crypto_analyzer

# Настройки анализа
GROK_MODEL=grok-3
GROK_USE_WEB_SEARCH=true
TWEET_LIMIT=100
```

## 📊 Мониторинг

```bash
# Проверка здоровья системы
python scripts/monitoring.py --full

# Отправка статистики в Telegram
python scripts/monitoring.py --telegram

# Просмотр логов
tail -f logs/crypto_analyzer.log
```

## 🔄 Автоматизация

### Cron (Linux/macOS)
```bash
# Каждые 2 часа
0 */2 * * * cd /path/to/project && python -m src.main

# Ежедневная статистика
0 18 * * * cd /path/to/project && python -m src.main --stats
```

### Systemd Service
```bash
sudo cp scripts/crypto-analyzer.service /etc/systemd/system/
sudo systemctl enable crypto-analyzer.timer
sudo systemctl start crypto-analyzer.timer
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
python scripts/run_tests.py

# Только unit тесты
python -m pytest tests/

# Тесты с покрытием
python -m pytest tests/ --cov=src
```

## 🚨 Устранение неполадок

### Частые проблемы:

1. **Ошибка JSON парсинга** - Обновите промпт или уменьшите количество твитов
2. **Превышение лимитов API** - Проверьте остаток кредитов xAI
3. **Ошибки Telegram** - Убедитесь, что бот добавлен в канал как администратор
4. **Проблемы с БД** - Проверьте подключение и права пользователя

Подробное руководство в [DEPLOYMENT.md](DEPLOYMENT.md)

## 📈 Производительность

- **Скорость анализа**: ~50-100 твитов за 10-20 секунд
- **Точность классификации**: ~85-90% (зависит от качества промпта)
- **Потребление памяти**: ~100-200 MB
- **Нагрузка на API**: Оптимизированные batch-запросы с retry логикой

## 🔐 Безопасность

- Все API ключи хранятся в переменных окружения
- Параметризованные SQL запросы для защиты от инъекций
- Логирование без чувствительных данных
- Docker контейнеры с непривилегированными пользователями

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Внесите изменения с тестами
4. Commit изменения (`git commit -m 'Add amazing feature'`)
5. Push в branch (`git push origin feature/amazing-feature`)
6. Создайте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. [LICENSE](LICENSE) файл.

## 📞 Поддержка

- **Issues**: [GitHub Issues](https://github.com/your-username/crypto-news-analyzer/issues)
- **Документация**: `docs/` директория
- **Примеры**: `examples/` директория