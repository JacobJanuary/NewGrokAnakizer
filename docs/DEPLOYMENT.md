# Руководство по развертыванию

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
