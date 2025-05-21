#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import text

from machine_tools.app.db.session_manager import session_manager


def show_unique_values(column_name: str) -> None:
    """
    Показывает уникальные значения для указанной колонки.

    Args:
        column_name (str): Название колонки для получения уникальных значений
    """
    with session_manager.engine.connect() as connection:
        query = text(f"SELECT DISTINCT {column_name} FROM machine_tools ORDER BY {column_name}")
        result = connection.execute(query)

        print(f"\nУникальные значения для колонки '{column_name}':")
        print("-" * 50)
        for row in result:
            print(row[0])


def show_all_unique_values() -> None:
    """Показывает уникальные значения для всех колонок таблицы"""
    with session_manager.engine.connect() as connection:
        # Получаем список всех колонок
        result = connection.execute(text("SELECT * FROM machine_tools LIMIT 1"))
        columns = result.keys()

        # Для каждой колонки получаем уникальные значения
        for column in columns:
            show_unique_values(column)


if __name__ == "__main__":
    # Пример использования для конкретной колонки
    show_unique_values("accuracy")

# Пример использования для всех колонок
# show_all_unique_values()
