#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import text

from machine_tools_3.app.db.session import engine


def technical_requirements():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM technical_requirements"))
        columns = result.keys()
        print(" | ".join(columns))
        print("-" * 80)
        for row in result:
            print(" | ".join(str(value) for value in row))


if __name__ == "__main__":
    technical_requirements()
