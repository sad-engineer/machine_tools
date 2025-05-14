#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Machine(Base):
    __tablename__ = "machine_tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    group = Column(Float)
    type = Column(Float)
    power = Column(Float)
    efficiency = Column(Float)
    accuracy = Column(String)
    automation = Column(String)
    specialization = Column(String)
    weight = Column(Float)
    weight_class = Column(String)
    length = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    overall_diameter = Column(String)
    city = Column(String)
    manufacturer = Column(String)
    machine_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    technical_requirements = relationship(
        "TechnicalRequirement",
        back_populates="machine",
        primaryjoin="Machine.name == TechnicalRequirement.machine_name",
    )
