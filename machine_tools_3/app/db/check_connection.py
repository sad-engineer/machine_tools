#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os

from sqlalchemy import inspect

from machine_tools_3.app.db.session import engine


def check_connection():
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("Подключение успешно!")
        print("Список таблиц в базе данных:", tables)
    except Exception as e:
        print("Ошибка подключения к базе данных:")
        print(e)


if __name__ == "__main__":
    check_connection()
