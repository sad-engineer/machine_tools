#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from machine_tools_3.app.models.machine import Machine, Base
from machine_tools_3.app.db.session import engine


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
    # Создать таблицы, если их нет
    Base.metadata.create_all(engine)

    # Путь к папке с CSV
    base_dir = os.path.dirname(__file__)
    csv_dir = os.path.join(base_dir, "..", "resources", "tables_csv")
    csv_dir = os.path.abspath(csv_dir)

    # Сессия
    Session = sessionmaker(bind=engine)
    session = Session()

    # Проверка, есть ли уже данные
    if session.query(Machine).first():
        print("Данные уже есть, инициализация не требуется.")
        session.close()
        return

    # Импорт основной таблицы (пример для machine_tools_1.csv)
    main_csv = os.path.join(csv_dir, "machine_tools.csv")
    if os.path.exists(main_csv):
        df = pd.read_csv(main_csv)
        for _, row in df.iterrows():
            machine = Machine(
                name=str(row['Станок']),
                group=safe_float(row['Группа']),
                type=safe_float(row['Тип']),
                power=safe_float(row['Мощность']),
                efficiency=str(row['КПД']),
                accuracy=str(row['Точность']),
                automation=str(row['Автоматизация']),
                specialization=str(row['Специализация']),
                weight=safe_float(row['Масса']),
                weight_class=str(row['Классификация_по_массе']),
                length=safe_int(row['Длина']),
                width=safe_int(row['Ширина']),
                height=safe_int(row['Высота']),
                overall_diameter=str(row['Габаритный_диаметр']),
                city=str(row['Город']),
                manufacturer=str(row['Производитель']),
                machine_type=str(row['Тип_станка']),
            )
            session.add(machine)
        session.commit()
        print(f"Загружено {len(df)} записей из machine_tools.csv")
    else:
        print("Файл machine_tools.csv не найден!")

    session.close()
    print("Инициализация БД завершена.")


# Для запуска как скрипт:
if __name__ == "__main__":
    init_db_from_csv()
