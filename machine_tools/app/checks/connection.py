#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Optional, Tuple

import psycopg2

from machine_tools.app.config import get_settings
from machine_tools.app.constants import GET_POSTGRES_VERSION, HELP_CONNECTION, POSTGRES_VERSION_FORMAT


def check_connection() -> Tuple[bool, Optional[str]]:
    """
    Проверяет подключение к серверу PostgreSQL.

    Returns:
        Tuple[bool, Optional[str]]: (успех, сообщение об ошибке)
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
            cur.execute(GET_POSTGRES_VERSION)
            version = cur.fetchone()[0]

        conn.close()
        return True, POSTGRES_VERSION_FORMAT.format(version=version)

    except Exception as e:
        return False, str(e)
