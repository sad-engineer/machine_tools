#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import text

from machine_tools_3.app.db.session_manager import session_manager


def show_technical_requirements():
    """Показывает все технические требования в базе данных"""
    with session_manager.engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM technical_requirements"))
        columns = result.keys()
        print(" | ".join(columns))
        print("-" * 80)
        for row in result:
            print(" | ".join(str(value) for value in row))


if __name__ == "__main__":
    show_technical_requirements()
