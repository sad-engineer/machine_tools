#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from machine_tools_3.app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    """
    Создает новую сессию для работы с базой данных.
    
    Returns:
        Session: Объект сессии SQLAlchemy
    """
    session = SessionLocal()
    try:
        return session
    except Exception as e:
        session.close()
        raise e
