#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from contextlib import contextmanager
from typing import Dict, Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from machine_tools.app.config import get_settings


class SessionManager:
    """
    Singleton для управления сессиями БД.
    """

    _instance = None
    _default_session: Optional[Session] = None
    _sessions: Dict[str, Session] = {}
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    @property
    def engine(self):
        """Ленивая инициализация engine"""
        if self._engine is None:
            settings = get_settings()  # Вызываем только когда нужно
            self._engine = create_engine(settings.DATABASE_URL)
        return self._engine

    @property
    def SessionLocal(self):
        """Ленивая инициализация SessionLocal"""
        if self._SessionLocal is None:
            self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self._SessionLocal

    @classmethod
    def get_session(cls, session_id: str = None) -> Session:
        """
        Получает сессию БД.

        Args:
            session_id (str, optional): Идентификатор сессии.
                Если None, возвращает дефолтную сессию.

        Returns:
            Session: Сессия БД
        """
        if session_id is None:
            if cls._default_session is None:
                cls._default_session = cls().SessionLocal()
            return cls._default_session
        else:
            if session_id not in cls._sessions:
                cls._sessions[session_id] = cls().SessionLocal()
            return cls._sessions[session_id]

    @classmethod
    def close_session(cls, session_id: str = None):
        """
        Закрывает сессию БД.

        Args:
            session_id (str, optional): Идентификатор сессии.
                Если None, закрывает дефолтную сессию.
        """
        if session_id is None:
            if cls._default_session is not None:
                cls._default_session.close()
                cls._default_session = None
        else:
            if session_id in cls._sessions:
                cls._sessions[session_id].close()
                del cls._sessions[session_id]

    @classmethod
    @contextmanager
    def get_db(cls, session_id: str = None) -> Generator[Session, None, None]:
        """
        Контекстный менеджер для работы с сессией БД.

        Args:
            session_id (str, optional): Идентификатор сессии.
                Если None, использует дефолтную сессию.

        Yields:
            Session: Сессия БД
        """
        try:
            session = cls.get_session(session_id)
            yield session
        finally:
            cls.close_session(session_id)


session_manager = SessionManager()

get_session = session_manager.get_session
close_session = session_manager.close_session
get_db = session_manager.get_db
