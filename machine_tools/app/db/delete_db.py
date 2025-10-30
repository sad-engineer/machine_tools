#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import psycopg2

from machine_tools.app.config import get_settings
from machine_tools.app.db.session_manager import session_manager


def delete_database() -> bool:
    """Удаляет базу данных, завершая активные подключения."""
    try:
        try:
            session_manager.close_session()
        except Exception:
            pass
        try:
            session_manager.engine.dispose()
        except Exception:
            pass

        settings = get_settings()
        conn = psycopg2.connect(
            dbname="postgres",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(
            """
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = %s
              AND pid <> pg_backend_pid();
            """,
            (settings.POSTGRES_DB,)
        )

        cur.execute(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB};")

        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Ошибка удаления базы данных: {e}")
        return False


