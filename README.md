# Machine Tools

| | |
| --- | --- |
| Testing | [![CI - Test](https://github.com/sad-engineer/machine_tools/actions/workflows/python-tests.yml/badge.svg)](https://github.com/sad-engineer/machine_tools/actions/workflows/python-tests.yml) |

# Machine Tools Database

Пакет для работы с базой данных станков и их технических требований.

## Графический интерфейс

Для удобной работы с базой данных доступно отдельное GUI приложение:

[![Machine Tools GUI](https://img.shields.io/badge/Machine%20Tools-GUI%20Application-blue?style=for-the-badge)](https://github.com/sad-engineer/machine_tools_gui_kivi)

Приложение предоставляет удобный интерфейс для:
- Просмотра и редактирования данных о станках
- Фильтрации и поиска станков
- Управления техническими требованиями
- Экспорта и импорта данных

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

База данных содержится в пакете, но перед использованием, необходимо инициализировать эту базу.

После установки пакета выполните:

```bash
# Вариант 1: Используя команду machine_tools
machine_tools init

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

### Пример 1: Поиск имен станков
```python
from machine_tools import Finder

limit = ...     # Количество имен в выдаче
with Finder(limit = limit) as finder: 
    print("Все станки:", finder.find_all())

    name: str = ...     # Строка для поиска
    print("Поиск по содержанию строки в имени:", finder.find_by_name(name))

    print("Поиск по совпадению мощности:", finder.find_by_power(power))
    print("Поиск по диапазону мощности:", finder.find_by_power(min_power=min_power, max_power=max_power))

    efficiency: float = ...     # КПД для поиска
    print("Поиск по КПД:", finder.find_by_efficiency(efficiency))
    print("Поиск по диапазону КПД:", finder.find_by_efficiency(min_efficiency=min_efficiency, max_efficiency=max_efficiency))
    
    accuracy: Accuracy = ...     # Класс точности для поиска
    print("Поиск по классу точности:", finder.find_by_accuracy(accuracy))

    automation: Automation = ...     # Уровень автоматизации для поиска
    print("Поиск по уровню автоматизации:", finder.find_by_automation(automation))

    specialization: Specialization = ...     # Специализация для поиска
    print("Поиск по специализации:", finder.find_by_specialization(specialization))

    software_control: SoftwareControl = ...     # Наличие системы управления для поиска
    print("Поиск по наличию системы управления:", finder.find_by_software_control(software_control))

    group: Union[int, List[int]] = ...     # Группа станка, 1...9
    print("Поиск по группе:", finder.find_by_group(group))
    print("Поиск по нескольким группам:", finder.find_by_group([1, 2, 3]))

    type: Union[int, List[int]] = ...     # Тип станка, 0...9
    print("Поиск по типу:", finder.find_by_type(type))  
    print("Поиск по нескольким типам:", finder.find_by_type([0, 1, 2]))
```

### Пример 2: Получение информации о станке

```python
from machine_tools import Finder, ListMachineInfoFormatter

with Finder() as finder:
    finder.set_formatter(ListMachineInfoFormatter())
    # получение информации о станках
    machines = finder.find_all()

    # получение информации о станке по имени
    machines = finder.find_by_name(name="16К20Ф3", exact_match=True)
    if len(machines) == 1:
        machine_info = machines[0]
        if machine_info:
            print(f"Станок: {machine_info.name}")
            print(f"Тип: {machine_info.machine_type}")
            print(f"Мощность: {machine_info.power} кВт")
            print(f"Точность: {machine_info.accuracy}")
            print(f"Автоматизация: {machine_info.automation}")
            print("\nГабариты:")
            print(f"Длина: {machine_info.dimensions.length} мм")
            print(f"Ширина: {machine_info.dimensions.width} мм")
            print(f"Высота: {machine_info.dimensions.height} мм")
            print("\nТехнические требования:")
            for req, value in machine_info.technical_requirements.items():
                print(f"{req}: {value}")
        else:
            print("Станок не найден")

    #  Поддерживает все фильтрации и сортировки
    machines = finder.find_by_power(min_power=10.0, order_by_power=True, descending=True)
    print(machines)
```

### Пример 3: Написание кастомного финдера

```python
from machine_tools import ListNameFormatter, MachineFormatter, SoftwareControl
from machine_tools.app.db.query_builder import QueryBuilder
from machine_tools.app.db.session_manager import Session, session_manager


class MachineFinderForOperations:
    """
    Кастомный поисковик для поиска имен станков по операциям.
    """
    def __init__(
        self,
        session: Optional[Session] = None,
        formatter: Optional[MachineFormatter] = None,
    ):
        pass
```

## Требования

- Python 3.9+
- PostgreSQL 12+
- SQLAlchemy
- Pandas
- Alembic
- Click (для CLI)