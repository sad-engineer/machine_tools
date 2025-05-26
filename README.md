# Machine Tools

[![Tests](https://github.com/KorenykAN/machine_tools/actions/workflows/tests.yml/badge.svg)](https://github.com/KorenykAN/machine_tools/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/KorenykAN/machine_tools/branch/main/graph/badge.svg)](https://codecov.io/gh/KorenykAN/machine_tools)

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
python -m machine_tools.app.db.init_db
```

## Структура проекта
```
machine_tools/
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

### Пример 1: Получение информации о станке

```python
from machine_tools_old import get_machine_info

# Получаем информацию о станке
machine_info = get_machine_info("16К20")

if machine_info:
    print(f"Станок: {machine_info['name']}")
    print(f"Тип: {machine_info['machine_type']}")
    print(f"Мощность: {machine_info['power']} кВт")
    print(f"Точность: {machine_info['accuracy']}")
    print(f"Автоматизация: {machine_info['automation']}")

    print("\nГабариты:")
    print(f"Длина: {machine_info['dimensions']['length']} мм")
    print(f"Ширина: {machine_info['dimensions']['width']} мм")
    print(f"Высота: {machine_info['dimensions']['height']} мм")

    print("\nТехнические требования:")
    for req, value in machine_info['technical_requirements'].items():
        print(f"{req}: {value}")
else:
    print("Станок не найден")
```

### Пример 2: Получение списка станков

```python
from machine_tools_old import Machine, Session

# Создаем сессию
session = Session()

# Получаем все станки
machines = session.query(Machine).all()

# Выводим информацию
for machine in machines:
    print(f"Станок: {machine.name}")
    print(f"Мощность: {machine.power}")
    print(f"Тип: {machine.machine_type}")
    print("---")

# Закрываем сессию
session.close()
```

### Пример 3: Поиск станков по параметрам

```python
from machine_tools_old import Machine, Session

session = Session()

# Поиск по мощности
powerful_machines = session.query(Machine).filter(Machine.power > 10).all()

# Поиск по типу
lathes = session.query(Machine).filter(Machine.machine_type == "Токарный").all()

# Поиск по нескольким параметрам
specific_machines = session.query(Machine).filter(
    Machine.power > 5,
    Machine.automation == "Автоматизированный"
).all()

session.close()
```

### Пример 4: Работа с техническими требованиями

```python
from machine_tools_old import Machine, TechnicalRequirement, Session

session = Session()

# Получаем станок
machine = session.query(Machine).filter(Machine.name == "16К20").first()

if machine:
    # Получаем все требования для станка
    requirements = session.query(TechnicalRequirement).filter(
        TechnicalRequirement.machine_name == machine.name
    ).all()

    # Выводим требования
    for req in requirements:
        print(f"{req.requirement}: {req.value}")

session.close()
```

## Требования

- Python 3.9+
- PostgreSQL 12+
- SQLAlchemy
- Pandas
- Alembic
- Click (для CLI)