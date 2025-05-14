# Machine Tools

# Machine Tools Database

Пакет для работы с базой данных станков и их технических требований.

## Установка

### Вариант 1: Poetry (рекомендуется)
```bash
poetry add git+https://github.com/sad-engineer/machine_tools.git#postgresql
```

### Вариант 2: pip
```bash
pip install git+https://github.com/sad-engineer/machine_tools.git#postgresql
```

## Инициализация базы данных

После установки пакета выполните:

```bash
# Вариант 1: Используя команду machine-tools
machine-tools init

# Вариант 2: Через Python модуль
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

## Требования

- Python 3.9+
- PostgreSQL 12+
- SQLAlchemy
- Pandas
- Alembic
- Click (для CLI)

