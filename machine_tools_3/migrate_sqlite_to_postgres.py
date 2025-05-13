#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import sys
sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from machine_tools_3.app.models.machine import Machine, Base
from machine_tools_3.app.db.session import engine as pg_engine
from datetime import datetime

# Подключение к SQLite (без encoding)
sqlite_engine = create_engine('sqlite:///../machine_tools/data/machine_tools.db')
sqlite_metadata = MetaData()
sqlite_metadata.reflect(bind=sqlite_engine)
sqlite_table = Table('machine_tools_1', sqlite_metadata, autoload_with=sqlite_engine)

# Сессия для PostgreSQL
PGSession = sessionmaker(bind=pg_engine)
pg_session = PGSession()

def safe_int(val):
    try:
        if val is None:
            return None
        return int(float(val))
    except (ValueError, TypeError):
        return None

def safe_float(val):
    try:
        if val is None:
            return None
        return float(val)
    except (ValueError, TypeError):
        return None

with sqlite_engine.connect() as conn:
    result = conn.execute(select(sqlite_table))
    rows = result.mappings().all()  # <-- теперь строки как словари

    for row in rows:
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
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        pg_session.add(machine)

    pg_session.commit()
    print(f"Перенесено {len(rows)} записей.")

pg_session.close()
