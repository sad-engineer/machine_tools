import sqlite3
import pandas as pd
import os
import re

db_path = '../machine_tools/data/machine_tools.db'
export_dir = 'app/resources/tables_csv'
os.makedirs(export_dir, exist_ok=True)

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

# Экспорт основной таблицы
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM machine_tools_1", conn)
df.to_csv(os.path.join(export_dir, 'machine_tools_1.csv'), index=False, encoding='utf-8')
print("Экспортирована таблица: machine_tools_1")

# Получаем список всех таблиц
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
table_names = [row['name'] for row in tables.to_dict(orient='records')]

# Экспорт остальных таблиц (кроме служебных)
for table in table_names:
    if table == 'machine_tools_1':
        continue
    df = pd.read_sql_query(f"SELECT * FROM '{table}'", conn)
    safe_table = clean_filename(table)
    df.to_csv(os.path.join(export_dir, f"{safe_table}.csv"), index=False, encoding='utf-8')
    print(f"Экспортирована таблица: {table}")

conn.close()
print("Экспорт завершён!")