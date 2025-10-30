#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
import tempfile
import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import Session, sessionmaker

from machine_tools.app.db.session_manager import session_manager, SessionManager
from machine_tools.app.models import Base


class TestSessionManager(unittest.TestCase):
    """Тесты для SessionManager"""

    @classmethod
    def setUpClass(cls):
        """Подготовка тестовой БД (SQLite во временном файле)"""

        cls.db_path = os.path.join(tempfile.gettempdir(), "machine_tools_session_manager_test.db")
        try:
            if os.path.exists(cls.db_path):
                os.remove(cls.db_path)
        except Exception:
            pass

        session_manager._engine = create_engine(
            f"sqlite:///{cls.db_path}", poolclass=NullPool, connect_args={"check_same_thread": False}
        )
        session_manager._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=session_manager._engine)

        session_manager._default_session = None
        session_manager._sessions.clear()

        Base.metadata.create_all(session_manager._engine)

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.session = session_manager.get_session()

    def tearDown(self):
        """Очистка после каждого теста"""

        try:
            self.session.execute(text("DROP TABLE IF EXISTS test"))
            self.session.commit()
        except Exception:
            self.session.rollback()

        session_manager.close_session()

    @classmethod
    def tearDownClass(cls):
        """Очистка БД после всех тестов"""

        session_manager.close_session()

        if session_manager._engine is not None:
            Base.metadata.drop_all(session_manager._engine)
            session_manager._engine.dispose()

        try:
            if hasattr(cls, "db_path") and cls.db_path and os.path.exists(cls.db_path):
                os.remove(cls.db_path)
        except Exception:
            pass

    def test_01_get_session(self):
        """Тест получения сессии"""
        self.assertIsInstance(self.session, Session)

    def test_02_get_db(self):
        """Тест получения сессии через контекстный менеджер"""
        with session_manager.get_db() as session:
            self.assertIsInstance(session, Session)

            result = session.execute(text("SELECT 1")).scalar()
            self.assertEqual(result, 1)

    def test_03_close_session(self):
        """Тест закрытия сессии"""

        SessionManager._default_session = None

        default_session = session_manager.get_session()

        self.assertIsNotNone(SessionManager._default_session, "Сессия должна быть создана после get_session()")
        self.assertIsNotNone(default_session)
        self.assertIs(SessionManager._default_session, default_session, "Возвращенная сессия должна быть той же самой")

        session_manager.close_session()

        self.assertIsNone(SessionManager._default_session, "Сессия должна быть закрыта после close_session()")

        self.assertIsNotNone(default_session)
        del default_session
        with self.assertRaises(NameError):
            print(default_session)

    def test_04_session_isolation(self):
        """Тест изоляции сессий"""
        with session_manager.get_db("1") as session1:
            with session_manager.get_db("2") as session2:
                self.assertIsNot(session1, session2)

                session1.execute(text("CREATE TEMP TABLE test (id INTEGER)"))
                with self.assertRaises(Exception):
                    session2.execute(text("SELECT * FROM test"))

    def test_05_transaction_rollback(self):
        """Тест отката транзакции"""
        with session_manager.get_db() as session:

            session.execute(text("CREATE TABLE IF NOT EXISTS test (id INTEGER)"))
            session.commit()

            session.execute(text("INSERT INTO test VALUES (1)"))
            session.rollback()
            result = session.execute(text("SELECT * FROM test")).fetchall()
            self.assertEqual(len(result), 0)

    def test_06_transaction_commit(self):
        """Тест коммита транзакции"""
        with session_manager.get_db() as session:
            session.execute(text("CREATE TABLE test (id INTEGER)"))
            session.execute(text("INSERT INTO test VALUES (1)"))
            session.commit()

            result = session.execute(text("SELECT * FROM test")).fetchall()
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], 1)


if __name__ == "__main__":
    unittest.main()
