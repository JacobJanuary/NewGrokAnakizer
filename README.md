# Crypto News Analyzer

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
