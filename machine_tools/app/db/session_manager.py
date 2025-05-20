#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from contextlib import contextmanager
from typing import Dict, Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from machine_tools.app.config import get_settings

settings = get_settings()


class SessionManager:
    """
    Singleton для управления сессиями БД.
    """

    _instance = None
    _default_session: Optional[Session] = None
    _sessions: Dict[str, Session] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            # Создаем движок БД
            cls._instance.engine = create_engine(settings.DATABASE_URL)
            # Создаем фабрику сессий
            cls._instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)
        return cls._instance

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
            # Используем дефолтную сессию для обычных операций
            if cls._default_session is None:
                cls._default_session = cls().SessionLocal()
            return cls._default_session
        else:
            # Создаем новую сессию для изолированных операций
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


# Создаем глобальный экземпляр менеджера сессий
session_manager = SessionManager()

# Экспортируем функции для удобства использования
get_session = session_manager.get_session
close_session = session_manager.close_session
get_db = session_manager.get_db
