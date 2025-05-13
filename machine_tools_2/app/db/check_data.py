from sqlalchemy import text

from machine_tools_2.app.db.session import engine


def show_machines():
    with engine.connect() as connection:
        # Получаем все записи из таблицы machines
        result = connection.execute(text("SELECT * FROM machines"))

        # Получаем названия колонок
        columns = result.keys()

        print("\nСодержимое таблицы machines:")
        print("-" * 100)

        # Выводим заголовки колонок
        print(" | ".join(columns))
        print("-" * 100)

        # Выводим данные
        for row in result:
            print(" | ".join(str(value) for value in row))

        print("-" * 100)


if __name__ == "__main__":
    show_machines()
