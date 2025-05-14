#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from machine_tools_3.app.models.machine import Base


class TechnicalRequirement(Base):
    __tablename__ = "technical_requirements"

    id = Column(Integer, primary_key=True)
    machine_name = Column(String, ForeignKey("machine_tools.name"), nullable=False)
    requirement = Column(String, nullable=False)
    value = Column(String, nullable=True)

    # Связь с моделью Machine
    machine = relationship("Machine", back_populates="technical_requirements")
