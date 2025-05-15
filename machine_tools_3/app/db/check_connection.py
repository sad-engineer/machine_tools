#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import psycopg2
from sqlalchemy import text

from machine_tools_3.app.core.config import get_settings

settings = get_settings()


def check_connection():
    """
    Проверяет подключение к серверу PostgreSQL.
    """
    try:
        # Пробуем подключиться к postgres
        conn = psycopg2.connect(
            dbname="postgres",  # Подключаемся к системной БД postgres
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
        )

        # Получаем информацию о подключении
        print(f"Подключение к PostgreSQL на {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}...")

        # Проверяем подключение
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"Версия PostgreSQL: {version}")

        conn.close()
        print("✅ Подключение установлено успешно")
        return True

    except Exception as e:
        print("❌ Ошибка подключения к PostgreSQL!")
        print(f"Детали ошибки: {str(e)}")
        print("\nУбедитесь, что:")
        print("1. Сервер PostgreSQL запущен")
        print("2. Настройки подключения корректны")
        print("3. Пользователь имеет права доступа")
        return False


if __name__ == "__main__":
    check_connection()
