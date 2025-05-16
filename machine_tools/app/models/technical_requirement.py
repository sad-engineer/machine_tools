#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from machine_tools.app.models.machine import Base


class TechnicalRequirement(Base):
    """SQLAlchemy модель технических требований станка, которая представляет таблицу в базе данных"""

    __tablename__ = "technical_requirements"

    id = Column(Integer, primary_key=True)  # Уникальный идентификатор требования
    machine_name = Column(String, ForeignKey("machine_tools.name"), nullable=False)  # Имя станка (внешний ключ)
    requirement = Column(String, nullable=False)  # Наименование параметра (например, "Максимальный диаметр обработки")
    value = Column(String, nullable=True)  # Значение параметра (может быть числом, текстом или диапазоном)

    # Связь с моделью Machine
    machine = relationship("Machine", back_populates="technical_requirements")
