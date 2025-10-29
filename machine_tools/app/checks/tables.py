#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Optional, Tuple

import psycopg2

from machine_tools.app.config import get_settings
from machine_tools.app.constants import GET_TABLES_LIST, HELP_TABLES


def check_tables_exist() -> Tuple[bool, Optional[str], Optional[List[str]]]:
    """
    Проверяет существование таблиц в базе данных machine_tools.

    Returns:
        Tuple[bool, Optional[str], Optional[List[str]]]: (таблицы существуют, сообщение об ошибке, список таблиц)
    """
    try:
        settings = get_settings()
        conn = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

        with conn.cursor() as cur:
            cur.execute(GET_TABLES_LIST)

            tables = [row[0] for row in cur.fetchall()]
            return True, None, tables

        conn.close()

    except Exception as e:
        return False, str(e), None


def get_tables_error_help() -> str:
    """Возвращает справочную информацию при ошибках таблиц."""
    return HELP_TABLES
