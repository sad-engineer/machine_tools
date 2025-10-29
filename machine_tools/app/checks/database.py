#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Dict, Optional, Tuple

import psycopg2

from machine_tools.app.config import get_settings
from machine_tools.app.constants import CHECK_DATABASE_EXISTS, DATABASE_NOT_FOUND, GET_DATABASE_INFO, HELP_DATABASE


def check_database_exists() -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Проверяет существование базы данных machine_tools.

    Returns:
        Tuple[bool, Optional[str], Optional[Dict]]: (существует, сообщение об ошибке, информация о БД)
    """
    try:
        settings = get_settings()
        conn = psycopg2.connect(
            dbname="postgres",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

        with conn.cursor() as cur:
            cur.execute(CHECK_DATABASE_EXISTS, (settings.POSTGRES_DB,))

            exists = cur.fetchone()[0]

            if exists:
                cur.execute(GET_DATABASE_INFO, (settings.POSTGRES_DB,))

                db_info = cur.fetchone()
                db_data = (
                    {'name': db_info[0], 'encoding': db_info[1], 'collate': db_info[2], 'ctype': db_info[3]}
                    if db_info
                    else None
                )

                return True, None, db_data
            else:
                return False, f"{DATABASE_NOT_FOUND} {settings.POSTGRES_DB}", None

        conn.close()

    except Exception as e:
        return False, str(e), None
