#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import inspect, text

from machine_tools_3.app.db.session_manager import session_manager


def check_connection():
    """
    Проверяет подключение к базе данных.
    Использует SessionManager для получения движка БД.
    """
    try:
        # Получаем движок из SessionManager
        engine = session_manager.engine
        inspector = inspect(engine)

        # Получаем информацию о подключении
        db_name = inspector.engine.url.database
        db_host = inspector.engine.url.host
        db_port = inspector.engine.url.port

        print(f"Подключение к БД {db_name} на {db_host}:{db_port}...")

        # Проверяем подключение
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()

        print("✅ Подключение установлено успешно")

    except Exception as e:
        print("❌ Ошибка подключения к базе данных!")
        print(f"Детали ошибки: {str(e)}")
        print("\nУбедитесь, что:")
        print("1. Сервер PostgreSQL запущен")
        print("2. База данных создана")
        print("3. Настройки подключения корректны")
        print("4. Пользователь имеет права доступа")


if __name__ == "__main__":
    check_connection()
