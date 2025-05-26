#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from machine_tools.app.config import get_settings
from machine_tools.app.db.session_manager import session_manager
from machine_tools.app.models import Base

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Настройка тестовой базы данных"""
    # Используем тестовую БД
    os.environ["POSTGRES_DB"] = "machine_tools_test"
    
    # Получаем настройки
    settings = get_settings()
    
    # Создаем движок
    engine = create_engine(settings.DATABASE_URL)
    
    # Создаем таблицы
    Base.metadata.create_all(engine)
    
    # Настраиваем session_manager
    session_manager.engine = engine
    session_manager.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield
    
    # Очистка после тестов
    Base.metadata.drop_all(engine) 