#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Текстовые константы для модуля базы данных.
"""

SUCCESS_CONNECTION = "Подключение установлено успешно!"
SUCCESS_DATABASE_CHECK = "Проверка базы данных завершена!"
SUCCESS_TABLES_CHECK = "Проверка таблиц завершена!"

ERROR_CONNECTION = "Ошибка подключения к PostgreSQL!"
ERROR_DATABASE_CHECK = "Ошибка при проверке базы данных!"
ERROR_TABLES_CHECK = "Ошибка при проверке таблиц!"

STATUS_OK = "[OK]"
STATUS_MISSING = "[MISSING]"
STATUS_ERROR = "[ERROR]"

INFO_TESTING_CONNECTION = "Тестирование подключения к PostgreSQL..."
INFO_CHECKING_DATABASE = "Проверка базы данных..."
INFO_CHECKING_TABLES = "Проверка таблиц..."

HELP_CONNECTION = """
Убедитесь, что:
1. Сервер PostgreSQL запущен
2. Настройки подключения корректны
3. Пользователь имеет права доступа к серверу PostgreSQL
"""

HELP_DATABASE = """
Убедитесь, что:
1. Проверка подключения проходит корректно (см. команду "check-connection")
2. База данных создана 

PS: Для создания базы перед первым использованием необходимо выполнить "machine_tools init"
"""

HELP_TABLES = """
Убедитесь, что:
1. Проверка подключения проходит корректно (см. команду "check-connection")
2. При первом использовании: Таблицы созданы перед первым использованием (см. команду "init")
3. Проверка подключения к базе данных проходит корректно (см. команду "check-database")
"""

CREATE_DB_COMMAND = "python -m machine_tools.app.db.init_db"
DATABASE_NOT_FOUND = "База данных не найдена!"

ERROR_POSTGRES_SERVER = "ОШИБКА: Сервер PostgreSQL не запущен!"
START_POSTGRES_COMMAND = "Запустите сервер командой: pg_ctl start -D <путь_к_данным>"
CREATING_DATABASE = "Создаю базу данных {db_name}..."
DATABASE_CREATED_SUCCESS = "База данных создана успешно!"
DATABASE_ALREADY_EXISTS = "База данных {db_name} уже существует."
ERROR_CREATING_DATABASE = "ОШИБКА при создании базы данных: {error}"
CREATING_TABLES = "Создаю таблицы..."
TABLES_CREATED_SUCCESS = "Таблицы созданы успешно!"
ERROR_INIT_DB = "ОШИБКА при инициализации БД: {error}"
INIT_DB_SUCCESS = "Инициализация БД завершена успешно!"

IMPORTING_DATA = "Импортирую данные из machine_tools.csv..."
LOADED_RECORDS = "Загружено {count} записей из machine_tools.csv"
ERROR_FILE_NOT_FOUND = "ОШИБКА: Файл machine_tools.csv не найден!"
TECHNICAL_REQUIREMENTS_ALREADY_IMPORTED = "Технические требования уже импортированы, инициализация не требуется."

TECHNICAL_REQUIREMENTS_ALREADY_EXIST = "Технические требования уже импортированы, пропускаю."
IMPORTING_TECHNICAL_CHARACTERISTICS = "Импортирую технические характеристики"
MACHINE_NOT_FOUND = "Станок {machine_name} не найден, пропуск."
TECHNICAL_REQUIREMENTS_IMPORT_COMPLETED = "Импорт технических требований завершён."

DB_INFO_FORMAT = "    - {field}: {value}"
DB_STATUS_FORMAT = "  База данных: {status}"
ERROR_DETAILS_FORMAT = "Детали ошибки: {error}"
POSTGRES_VERSION_FORMAT = "Версия PostgreSQL: {version}"
