# Machine Tools

# Machine Tools Database

Пакет для работы с базой данных станков и их технических требований.

## Установка

### Вариант 1: Poetry (рекомендуется)

```bash
poetry add git+https://github.com/sad-engineer/machine_tools.git
```

### Вариант 2: pip

```bash
pip install git+https://github.com/sad-engineer/machine_tools.git
```

## Инициализация базы данных

После установки пакета выполните:

```bash
python -m machine_tools_3.app.db.init_db
```

## Структура проекта
```
machine_tools_3/
├── alembic/ # Миграции базы данных
├── app/
│ ├── db/ # Работа с базой данных
│ ├── models/ # Модели SQLAlchemy
│ └── resources/ # CSV-файлы с данными
├── tests/ # Тесты
├── pyproject.toml # Зависимости и метаданные
└── setup.cfg # Настройки установки
```

## Использование

После установки и инициализации БД вы можете:

1. **Проверить подключение к БД:**
```python
python -m machine_tools_3.app.db.check_connection
```

2. **Импортировать данные из CSV:**
```python
python -m machine_tools_3.app.db.init_db
```

## Требования

- Python 3.9+
- PostgreSQL 12+
- SQLAlchemy
- Pandas
- Alembic
