#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
import pandas as pd
from sqlalchemy import text
from machine_tools.app.db.session_manager import session_manager


# Создаем директорию для экспорта, если её нет
export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database_backups')
os.makedirs(export_dir, exist_ok=True)


# Экспортируем таблицу machine_tools
with session_manager.engine.connect() as connection:
    result = connection.execute(text("""
        SELECT 
            id, name, "group", "type", power, efficiency, accuracy, 
            automation, software_control, specialization, weight, 
            weight_class, "length", width, height, overall_diameter, 
            city, manufacturer, machine_type, created_at, updated_at
        FROM machine_tools
        ORDER BY id
    """))
    df_machines = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Сохраняем в CSV с правильной кодировкой
    machines_path = os.path.join(export_dir, 'machine_tools.csv')
    df_machines.to_csv(machines_path, index=False, encoding='utf-8-sig')
    print(f"Сохранено в: {machines_path}")

# Экспортируем таблицу technical_requirements
with session_manager.engine.connect() as connection:
    result = connection.execute(text("""
        SELECT 
            id, machine_name, requirement, value
        FROM technical_requirements
        ORDER BY machine_name, id
    """))
    df_requirements = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Сохраняем в CSV с правильной кодировкой
    requirements_path = os.path.join(export_dir, 'technical_requirements.csv')
    df_requirements.to_csv(requirements_path, index=False, encoding='utf-8-sig')
    print(f"Сохранено в: {requirements_path}")

print("Экспорт завершен!")
