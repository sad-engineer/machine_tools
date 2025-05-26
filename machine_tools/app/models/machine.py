#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Machine(Base):
    """SQLAlchemy модель станка, которая представляет таблицу в базе данных"""

    __tablename__ = "machine_tools"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор станка
    name = Column(String, nullable=False, unique=True)  # Название станка (например, "16К20")
    group = Column(Integer)  # Группа станка
    type = Column(Integer)  # Тип станка
    power = Column(Float)  # Мощность станка в кВт
    efficiency = Column(Float)  # КПД станка
    accuracy = Column(String)  # Класс точности станка
    automation = Column(String)  # Уровень автоматизации (например, "Автоматизированный")
    software_control = Column(String)  # тип программного управления
    specialization = Column(String)  # Специализация станка
    weight = Column(Float)  # Масса станка в кг
    weight_class = Column(String)  # Класс станка по массе
    length = Column(Integer)  # Длина станка в мм
    width = Column(Integer)  # Ширина станка в мм
    height = Column(Integer)  # Высота станка в мм
    overall_diameter = Column(String)  # Габаритный диаметр станка
    city = Column(String)  # Город производителя
    manufacturer = Column(String)  # Название производителя
    machine_type = Column(String)  # Тип станка (например, "Токарный")
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания записи
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Дата последнего обновления
    technical_requirements = relationship(
        "TechnicalRequirement",
        back_populates="machine",
        primaryjoin="Machine.name == TechnicalRequirement.machine_name",
    )
