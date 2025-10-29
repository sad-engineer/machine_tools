#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
import sys

import chardet
import pandas as pd
import psycopg2

from machine_tools.app.checks.connection import check_connection
from machine_tools.app.config import get_settings
from machine_tools.app.constants import (
    CHECK_DATABASE_EXISTS_SIMPLE,
    CREATE_DATABASE_WITH_ENCODING,
    CREATING_DATABASE,
    CREATING_TABLES,
    DATABASE_ALREADY_EXISTS,
    DATABASE_CREATED_SUCCESS,
    ERROR_CREATING_DATABASE,
    ERROR_FILE_NOT_FOUND,
    ERROR_INIT_DB,
    ERROR_POSTGRES_SERVER,
    IMPORTING_DATA,
    IMPORTING_TECHNICAL_CHARACTERISTICS,
    INIT_DB_SUCCESS,
    LOADED_RECORDS,
    MACHINE_NOT_FOUND,
    START_POSTGRES_COMMAND,
    TABLES_CREATED_SUCCESS,
    TECHNICAL_REQUIREMENTS_ALREADY_EXIST,
    TECHNICAL_REQUIREMENTS_ALREADY_IMPORTED,
    TECHNICAL_REQUIREMENTS_IMPORT_COMPLETED,
)
from machine_tools.app.db.session_manager import session_manager
from machine_tools.app.models import Base, Machine, TechnicalRequirement


def create_database():
    """Создает базу данных, если она не существует"""
    try:
        settings = get_settings()
        conn = psycopg2.connect(
            dbname="postgres",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(CHECK_DATABASE_EXISTS_SIMPLE.format(db_name=settings.POSTGRES_DB))
        exists = cur.fetchone()

        if not exists:
            print(CREATING_DATABASE.format(db_name=settings.POSTGRES_DB))
            cur.execute(
                CREATE_DATABASE_WITH_ENCODING.format(
                    db_name=settings.POSTGRES_DB,
                    owner=settings.POSTGRES_USER
                )
            )
            print(DATABASE_CREATED_SUCCESS)
        else:
            print(DATABASE_ALREADY_EXISTS.format(db_name=settings.POSTGRES_DB))

        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(ERROR_CREATING_DATABASE.format(error=str(e)))
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
    success, error_msg = check_connection()
    if not success:
        print(ERROR_POSTGRES_SERVER)
        print(START_POSTGRES_COMMAND)
        sys.exit(1)

    if not create_database():
        sys.exit(1)

    try:
        print(CREATING_TABLES)
        Base.metadata.create_all(session_manager.engine)
        print(TABLES_CREATED_SUCCESS)

        base_dir = os.path.dirname(__file__)
        csv_dir = os.path.join(base_dir, "..", "resources", "tables_csv")
        csv_dir = os.path.abspath(csv_dir)

        with session_manager.get_db() as session:
            if not session.query(TechnicalRequirement).first():
                main_csv = os.path.join(csv_dir, "machine_tools.csv")
                if os.path.exists(main_csv):
                    print(IMPORTING_DATA)
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
                    print(LOADED_RECORDS.format(count=len(df)))
                else:
                    print(ERROR_FILE_NOT_FOUND)
            else:
                print(TECHNICAL_REQUIREMENTS_ALREADY_IMPORTED)

        print(INIT_DB_SUCCESS)

        import_technical_requirements()

    except Exception as e:
        print(ERROR_INIT_DB.format(error=str(e)))
        sys.exit(1)


def import_technical_requirements():
    """Импортирует технические требования из CSV файлов"""
    base_dir = os.path.dirname(__file__)
    csv_dir = os.path.join(base_dir, "..", "resources", "tables_csv")
    csv_dir = os.path.abspath(csv_dir)

    with session_manager.get_db() as session:
        if session.query(TechnicalRequirement).first():
            print(TECHNICAL_REQUIREMENTS_ALREADY_EXIST)
            return

        print(IMPORTING_TECHNICAL_CHARACTERISTICS)
        for filename in os.listdir(csv_dir):
            if filename.endswith(".csv") and filename != "machine_tools.csv":
                file_path = os.path.join(csv_dir, filename)
                with open(file_path, "rb") as file:
                    raw_data = file.read()
                    result = chardet.detect(raw_data)
                    encoding = result["encoding"]

                df = pd.read_csv(file_path, encoding=encoding)
                machine_name = df.columns[-1]
                machine = session.query(Machine).filter(Machine.name == machine_name).first()
                if not machine:
                    print(MACHINE_NOT_FOUND.format(machine_name=machine_name))
                    print(filename)
                    continue

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

    print(TECHNICAL_REQUIREMENTS_IMPORT_COMPLETED)


if __name__ == "__main__":
    init_db_from_csv()
