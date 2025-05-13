from sqlalchemy import inspect

from machine_tools_2.app.db.session import engine


def list_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("\nСписок таблиц в базе данных:")
    print("-" * 30)
    for table in tables:
        print(f"Таблица: {table}")
        # Получаем информацию о колонках
        columns = inspector.get_columns(table)
        print("Колонки:")
        for column in columns:
            print(f"  - {column['name']}: {column['type']}")
        print("-" * 30)


if __name__ == "__main__":
    list_tables()
