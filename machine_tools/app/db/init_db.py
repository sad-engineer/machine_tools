#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
import sys

import chardet
import pandas as pd
import psycopg2

from machine_tools.app.config import get_settings
from machine_tools.app.db.session_manager import session_manager
from machine_tools.app.models import Base, Machine, TechnicalRequirement

settings = get_settings()


def check_postgres_server():
    """Проверяет, запущен ли сервер PostgreSQL"""
    try:
        # Пробуем подключиться к postgres
        conn = psycopg2.connect(
            dbname="postgres",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )
        conn.close()
        return True
    except psycopg2.OperationalError:
        print("ОШИБКА: Сервер PostgreSQL не запущен!")
        print("Запустите сервер командой: pg_ctl start -D <путь_к_данным>")
        return False


def create_database():
    """Создает базу данных, если она не существует"""
    try:
        # Подключаемся к postgres для создания БД
        conn = psycopg2.connect(
            dbname="postgres",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Проверяем существование БД
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{settings.POSTGRES_DB}'")
        exists = cur.fetchone()

        if not exists:
            print(f"Создаю базу данных {settings.POSTGRES_DB}...")
            # Создаем БД с кодировкой UTF-8
            cur.execute(
                f"CREATE DATABASE {settings.POSTGRES_DB} WITH ENCODING 'UTF8' LC_COLLATE='ru_RU.UTF-8' LC_CTYPE='ru_RU.UTF-8' TEMPLATE=template0"
            )
            print("База данных создана успешно!")
        else:
            print(f"База данных {settings.POSTGRES_DB} уже существует.")

        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"ОШИБКА при создании базы данных: {str(e)}")
        return False


def safe_int(val):
    try:
        if pd.isna(val) or val is None:
            return None
        return int(float(val))
    except (ValueError, TypeError):
        return None


def safe_float(val):
    try:
        if pd.isna(val) or val is None:
            return None
        return float(val)
    except (ValueError, TypeError):
        return None


def init_db_from_csv():
    """Инициализирует базу данных и импортирует данные"""
    # Проверяем сервер
    if not check_postgres_server():
        sys.exit(1)

    # Создаем БД
    if not create_database():
        sys.exit(1)

    try:
        # Создаем таблицы
        print("Создаю таблицы...")
        Base.metadata.create_all(session_manager.engine)
        print("Таблицы созданы успешно!")

        # Путь к папке с CSV
        base_dir = os.path.dirname(__file__)
        csv_dir = os.path.join(base_dir, "..", "resources", "tables_csv")
        csv_dir = os.path.abspath(csv_dir)

        # Используем SessionManager для получения сессии
        with session_manager.get_db() as session:
            # Проверяем только технические требования
            if not session.query(TechnicalRequirement).first():
                # Импорт основной таблицы
                main_csv = os.path.join(csv_dir, "machine_tools.csv")
                if os.path.exists(main_csv):
                    print("Импортирую данные из machine_tools.csv...")
                    df = pd.read_csv(main_csv)
                    for _, row in df.iterrows():
                        machine = Machine(
                            name=str(row["name"]),
                            group=safe_float(row["group"]),
                            type=safe_float(row["type"]),
                            power=safe_float(row["power"]),
                            efficiency=str(row["efficiency"]),
                            accuracy=str(row["accuracy"]),
                            automation=str(row["automation"]),
                            specialization=str(row["specialization"]),
                            weight=safe_float(row["weight"]),
                            weight_class=str(row["weight_class"]),
                            length=safe_int(row["length"]),
                            width=safe_int(row["width"]),
                            height=safe_int(row["height"]),
                            overall_diameter=str(row["overall_diameter"]),
                            city=str(row["city"]),
                            manufacturer=str(row["manufacturer"]),
                            machine_type=str(row["machine_type"]),
                        )
                        session.add(machine)
                    session.commit()
                    print(f"Загружено {len(df)} записей из machine_tools.csv")
                else:
                    print("ОШИБКА: Файл machine_tools.csv не найден!")
            else:
                print("Технические требования уже импортированы, инициализация не требуется.")

        print("Инициализация БД завершена успешно!")

        # Импортируем технические требования
        import_technical_requirements()

    except Exception as e:
        print(f"ОШИБКА при инициализации БД: {str(e)}")
        sys.exit(1)


def import_technical_requirements():
    """Импортирует технические требования из CSV файлов"""
    base_dir = os.path.dirname(__file__)
    csv_dir = os.path.join(base_dir, "..", "resources", "tables_csv")
    csv_dir = os.path.abspath(csv_dir)

    # Используем SessionManager для получения сессии
    with session_manager.get_db() as session:
        # Проверка, есть ли уже данные
        if session.query(TechnicalRequirement).first():
            print("Технические требования уже импортированы, пропускаю.")
            return

        print(f"Импортирую технические характеристики")
        # Импорт всех CSV-файлов с требованиями
        for filename in os.listdir(csv_dir):
            if filename.endswith(".csv") and filename != "machine_tools.csv":
                # Определяем кодировку файла
                file_path = os.path.join(csv_dir, filename)
                with open(file_path, "rb") as file:
                    raw_data = file.read()
                    result = chardet.detect(raw_data)
                    encoding = result["encoding"]

                # Читаем CSV с определенной кодировкой
                df = pd.read_csv(file_path, encoding=encoding)

                # Получаем имя станка из последнего столбца
                machine_name = df.columns[-1]

                # Проверяем, существует ли станок
                machine = session.query(Machine).filter(Machine.name == machine_name).first()
                if not machine:
                    print(f"Станок {machine_name} не найден, пропускаю.")
                    print(filename)
                    continue

                # Импортируем каждое требование
                for _, row in df.iterrows():
                    requirement = str(row["Наименование параметра"])
                    value = str(row[machine_name]) if not pd.isna(row[machine_name]) else None

                    if requirement and requirement.strip():  # Пропускаем пустые строки
                        req = TechnicalRequirement(
                            machine_name=machine_name,
                            requirement=requirement,
                            value=value,
                        )
                        session.add(req)

                session.commit()

    print("Импорт технических требований завершён.")


# Для запуска как скрипт:
if __name__ == "__main__":
    init_db_from_csv()
