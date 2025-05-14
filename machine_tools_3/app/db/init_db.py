#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
import sys

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from machine_tools_3.app.core.config import get_settings
from machine_tools_3.app.db.session import engine
from machine_tools_3.app.models.machine import Base, Machine
from machine_tools_3.app.models.technical_requirement import TechnicalRequirement

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
        cur.execute(
            f"SELECT 1 FROM pg_database WHERE datname = '{settings.POSTGRES_DB}'"
        )
        exists = cur.fetchone()

        if not exists:
            print(f"Создаю базу данных {settings.POSTGRES_DB}...")
            cur.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
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
        Base.metadata.create_all(engine)
        print("Таблицы созданы успешно!")

        # Путь к папке с CSV
        base_dir = os.path.dirname(__file__)
        csv_dir = os.path.join(base_dir, "..", "resources", "tables_csv")
        csv_dir = os.path.abspath(csv_dir)

        # Сессия
        Session = sessionmaker(bind=engine)
        session = Session()

        # Проверяем только технические требования
        if not session.query(TechnicalRequirement).first():
            # Импорт основной таблицы
            main_csv = os.path.join(csv_dir, "machine_tools.csv")
            if os.path.exists(main_csv):
                print("Импортирую данные из machine_tools.csv...")
                df = pd.read_csv(main_csv, encoding='cp1251')
                for _, row in df.iterrows():
                    machine = Machine(
                        name=str(row["Станок"]),
                        group=safe_float(row["Группа"]),
                        type=safe_float(row["Тип"]),
                        power=safe_float(row["Мощность"]),
                        efficiency=str(row["КПД"]),
                        accuracy=str(row["Точность"]),
                        automation=str(row["Автоматизация"]),
                        specialization=str(row["Специализация"]),
                        weight=safe_float(row["Масса"]),
                        weight_class=str(row["Классификация_по_массе"]),
                        length=safe_int(row["Длина"]),
                        width=safe_int(row["Ширина"]),
                        height=safe_int(row["Высота"]),
                        overall_diameter=str(row["Габаритный_диаметр"]),
                        city=str(row["Город"]),
                        manufacturer=str(row["Производитель"]),
                        machine_type=str(row["Тип_станка"]),
                    )
                    session.add(machine)
                session.commit()
                print(f"Загружено {len(df)} записей из machine_tools.csv")
            else:
                print("ОШИБКА: Файл machine_tools.csv не найден!")

            # Импортируем технические требования
            import_technical_requirements()
        else:
            print(
                "Технические требования уже импортированы, инициализация не требуется."
            )

        session.close()
        print("Инициализация БД завершена успешно!")

    except Exception as e:
        print(f"ОШИБКА при инициализации БД: {str(e)}")
        sys.exit(1)


def import_technical_requirements():
    """Импортирует технические требования из CSV файлов"""
    base_dir = os.path.dirname(__file__)
    csv_dir = os.path.join(base_dir, "..", "resources", "tables_csv")
    csv_dir = os.path.abspath(csv_dir)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Проверка, есть ли уже данные
    if session.query(TechnicalRequirement).first():
        print("Технические требования уже импортированы, пропускаю.")
        session.close()
        return

    # Импорт всех CSV-файлов с требованиями
    for filename in os.listdir(csv_dir):
        if filename.endswith(".csv") and filename != "machine_tools.csv":
            print(f"Импортирую данные из {filename}...")
            df = pd.read_csv(os.path.join(csv_dir, filename), encoding='cp1251')

            # Получаем имя станка из последнего столбца
            machine_name = df.columns[-1]

            # Проверяем, существует ли станок
            machine = (
                session.query(Machine).filter(Machine.name == machine_name).first()
            )
            if not machine:
                print(f"Станок {machine_name} не найден, пропускаю.")
                continue

            # Импортируем каждое требование
            for _, row in df.iterrows():
                requirement = str(row["Наименование параметра"])
                value = (
                    str(row[machine_name]) if not pd.isna(row[machine_name]) else None
                )

                if requirement and requirement.strip():  # Пропускаем пустые строки
                    req = TechnicalRequirement(
                        machine_name=machine_name, requirement=requirement, value=value
                    )
                    session.add(req)

            session.commit()
            print(f"Импортированы требования из {filename} для станка {machine_name}")

    session.close()
    print("Импорт технических требований завершён.")


# Для запуска как скрипт:
if __name__ == "__main__":
    init_db_from_csv()
