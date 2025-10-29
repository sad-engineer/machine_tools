#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import text

from machine_tools.app.db.session_manager import session_manager


def show_technical_requirements():
    """Показывает все технические требования в базе данных"""
    try:
        with session_manager.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM technical_requirements"))
            columns = result.keys()

            # Выводим заголовки
            header = " | ".join(columns)
            print(header)
            print("-" * len(header))

            # Выводим данные
            for row in result:
                row_str = " | ".join(str(value) if value is not None else "NULL" for value in row)
                print(row_str)

    except Exception as e:
        print(f"Ошибка при получении технических требований: {e}")
        raise


if __name__ == "__main__":
    show_technical_requirements()
