# `machine_tools`

`machine_tools` - модуль работы с базой данных станков.

Материал демонстрационный, показывает навыки работы.
Проект устарел, показывает предыдущий взгляд на способы решения проблемы доступа и обработки информации к БД 

## Установка
```bash
pip install git+https://github.com/sad-engineer/machine_tools.git
```

## Клонирование проекта
```bash
git clone https://github.com/sad-engineer/machine_tools.git
cd machine_tools_old
```

## Подготовка базы данных
База данных устанавливается вместе с пакетом, и настройка не требуется. Пакет поддерживает базу данных SQLite.


## Использование

Пример использования:

```python
from machine_tools_old import MachineToolsContainer as Container

# Создаем креатор
creator = Container().creator()

# Получение параметров станка по имени
result = creator.by_name("16К20Ф3")
# Получение параметров станка, заданного по умолчанию. Доступ по типу процесса
result = creator.default(type_processing="Фрезерование")

# Получение списка всех станков 
lister = Container().lister()
result = lister("all")

# Получение списка станков по типу и группе
result = lister.by_type_and_group(machine_type=1, group=1)
```

## Структура проекта
```
machine_tools/
├── machine_tools/
│ ├── init.py
│ ├── main.py
│ ├── fun.py                # Основные функции работы со станками
│ ├── find.py               # Функции поиска и фильтрации данных
│ ├── download_from_xls.py  # Импорт данных из Excel
│ ├── logger_settings.py    # Настройки логирования
│ ├── data/
│ │ ├── init.py
│ │ └── machine_tools.db    # База данных станков
│ ├── logs/
│ │ └── log.log             # Файл логов
│ └── obj/                  # Основные классы и объекты
│ ├── init.py
│ ├── constants.py          # Константы проекта
│ ├── containers.py         # Контейнеры зависимостей
│ ├── creators.py           # Создание объектов
│ ├── entities.py           # Сущности предметной области
│ ├── exceptions.py         # Пользовательские исключения
│ ├── fields_types.py       # Типы полей
│ ├── finders.py            # Поиск в базе данных
│ ├── listers.py            # Списки и перечисления
│ └── machine_tool_class.py # Основной класс станка
├── README.md 
├── poetry.lock 
├── pyproject.toml 
└── setup.cfg 
```

## Требования

- Python 3.9 или выше
- pandas 2.0.3+
- dependency-injector 4.41.0+
- pydantic 2.11.3+
- service-for-my-projects 
- Poetry

## Установка зависимостей

Для установки зависимостей проекта используйте Poetry:

1. Установите Poetry, если он еще не установлен:
```sh
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/MacOS
curl -sSL https://install.python-poetry.org | python3 -
```

2. Установите зависимости проекта:
```sh
# Перейдите в директорию проекта
cd machine_tools_old

# Установите зависимости
poetry install

# Активируйте виртуальное окружение
poetry shell
```

3. Альтернативная установка через pip:
```sh
# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

## Вклад в проект

1. Создайте форк проекта
2. Создайте ветку для ваших изменений
3. Внесите изменения
4. Отправьте pull request

Пожалуйста, убедитесь, что ваши изменения:
- Сопровождаются тестами
- Следуют существующему стилю кода
- Обновляют документацию при необходимости




После установки пакета
init-machine-tools-db
