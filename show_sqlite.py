import sqlite3

# Путь к базе данных
db_path = r"machine_tools\data\machine_tools.db"

# Подключение к базе
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получить список таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Таблицы в базе данных:", [t[0] for t in tables])

# Например, посмотреть содержимое таблицы machines
table_name = "machine_tools_1"  # замени на нужную таблицу
cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]
print(" | ".join(columns))
print("-" * 80)
for row in rows:
    print(" | ".join(str(value) for value in row))

conn.close()