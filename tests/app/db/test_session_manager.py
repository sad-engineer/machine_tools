#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
import unittest
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from machine_tools.app.config import get_settings
from machine_tools.app.db.session_manager import session_manager
from machine_tools.app.models import Base

# Устанавливаем путь к тестовым настройкам
os.environ["MACHINE_TOOLS_ENV"] = str(Path(__file__).parent.parent.parent / "settings" / "test.env")
settings = get_settings()


class TestSessionManager(unittest.TestCase):
    """Тесты для SessionManager"""

    @classmethod
    def setUpClass(cls):
        """Подготовка тестовой БД"""
        # Создаем движок с тестовой БД
        session_manager.engine = create_engine(settings.DATABASE_URL)
        session_manager.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=session_manager.engine)
        # Создаем таблицы
        Base.metadata.create_all(session_manager.engine)

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.session = session_manager.get_session()

    def tearDown(self):
        """Очистка после каждого теста"""
        # Удаляем тестовую таблицу, если она существует
        try:
            self.session.execute(text("DROP TABLE IF EXISTS test"))
            self.session.commit()
        except Exception:
            self.session.rollback()
        # Закрываем сессию
        session_manager.close_session()

    @classmethod
    def tearDownClass(cls):
        """Очистка БД после всех тестов"""
        Base.metadata.drop_all(session_manager.engine)

    def test_01_get_session(self):
        """Тест получения сессии"""
        self.assertIsInstance(self.session, Session)

    def test_02_get_db(self):
        """Тест получения сессии через контекстный менеджер"""
        with session_manager.get_db() as session:
            self.assertIsInstance(session, Session)
            # Проверяем, что сессия работает
            result = session.execute(text("SELECT 1")).scalar()
            self.assertEqual(result, 1)

    def test_03_close_session(self):
        """Тест закрытия сессии"""
        # Получаем сессию
        default_session = session_manager.get_session()
        # Проверяем, что сессия создана
        self.assertIsNotNone(session_manager._default_session)
        self.assertIsNotNone(default_session)
        # Закрываем сессию
        session_manager.close_session()
        # Проверяем, что сессия закрыта
        self.assertIsNone(session_manager._default_session)
        # Проверяем, ссылку на сессию
        self.assertIsNotNone(default_session)
        del default_session
        with self.assertRaises(NameError):
            print(default_session)

    def test_04_session_isolation(self):
        """Тест изоляции сессий"""
        with session_manager.get_db("1") as session1:
            with session_manager.get_db("2") as session2:
                self.assertIsNot(session1, session2)
                # Проверяем, что сессии независимы
                session1.execute(text("CREATE TABLE test (id INTEGER)"))
                with self.assertRaises(Exception):
                    session2.execute(text("SELECT * FROM test"))

    def test_05_transaction_rollback(self):
        """Тест отката транзакции"""
        with session_manager.get_db() as session:
            session.execute(text("CREATE TABLE test (id INTEGER)"))
            session.execute(text("INSERT INTO test VALUES (1)"))
            session.rollback()
            # Проверяем, что таблица не создана
            with self.assertRaises(Exception):
                session.execute(text("SELECT * FROM test"))

    def test_06_transaction_commit(self):
        """Тест коммита транзакции"""
        with session_manager.get_db() as session:
            session.execute(text("CREATE TABLE test (id INTEGER)"))
            session.execute(text("INSERT INTO test VALUES (1)"))
            session.commit()
            # Проверяем, что данные сохранились
            result = session.execute(text("SELECT * FROM test")).fetchall()
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], 1)


if __name__ == "__main__":
    unittest.main()
