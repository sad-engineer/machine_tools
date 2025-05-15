#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import enum
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from machine_tools_2.app.db.base import Base


class ProcessingType(enum.Enum):
    TURNING = "Токарная"
    MILLING = "Фрезерная"
    DRILLING = "Сверлильная"
    GRINDING = "Шлифовальная"
    PLANING = "Строгальная"


class AutomationType(enum.Enum):
    MANUAL = "Ручное"
    SEMI_AUTO = "Полуавтомат"
    AUTO = "Автомат"
    CNC = "ЧПУ"


class AccuracyClass(enum.Enum):
    NORMAL = "Нормальная"
    HIGH = "Повышенная"
    PRECISION = "Высокая"
    ULTRA = "Особо высокая"


class SpecializationType(enum.Enum):
    UNIVERSAL = "Универсальный"
    SPECIALIZED = "Специализированный"
    SPECIAL = "Специальный"


class WeightClass(enum.Enum):
    LIGHT = "Легкий"
    MEDIUM = "Средний"
    HEAVY = "Тяжелый"
    EXTRA_HEAVY = "Особо тяжелый"


class MachineType(enum.Enum):
    TURNING = "Токарный"
    MILLING = "Фрезерный"
    DRILLING = "Сверлильный"
    GRINDING = "Шлифовальный"
    PLANING = "Строгальный"


class MachineGroup(enum.Enum):
    GROUP_1 = "Группа update_relationships.py"
    GROUP_2 = "Группа 2"
    GROUP_3 = "Группа 3"
    GROUP_4 = "Группа 4"
    GROUP_5 = "Группа 5"


class PlaningMachineType(enum.Enum):
    LONGITUDINAL = "Продольно строгальный"
    CROSS = "Поперечно строгальный"
    SLOTTING = "Долбежный"

    @classmethod
    def get_index(cls, value):
        """Получить числовой индекс для значения"""
        return list(cls).index(value)

    @classmethod
    def from_index(cls, index):
        """Получить значение по числовому индексу"""
        return list(cls)[index]

    def get_index(self):
        """Получить числовой индекс текущего значения"""
        return self.get_index(self)


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    # Габаритные размеры и вес
    length = Column(Float, comment="Длина станка")
    width = Column(Float, comment="Ширина станка")
    height = Column(Float, comment="Высота станка")
    weight = Column(Float, comment="Вес станка")
    # Производитель
    manufacturer = Column(String, comment="Производитель")
    city = Column(String, comment="Город производителя")
    # Классификация
    machine_type = Column(Enum(MachineType), nullable=False, comment="Тип станка")
    group = Column(Enum(MachineGroup), comment="Группа станка")
    type_of_planing_machine = Column(Enum(PlaningMachineType), comment="Тип строгального станка")
    class_by_weight = Column(Enum(WeightClass), comment="Класс по весу")
    # Технические характеристики
    performance_proc = Column(Float, comment="КПД обработки")
    power_lathe_passport_kvt = Column(Float, comment="Мощность станка по паспорту, кВт")
    spindle_power = Column(Float, comment="Мощность шпинделя")
    automation = Column(Enum(AutomationType), comment="Тип автоматизации")
    accuracy = Column(Enum(AccuracyClass), comment="Класс точности")
    specialization = Column(Enum(SpecializationType), comment="Специализация")

    # Дополнительные данные
    passport_data = Column(JSON, comment="Паспортные данные")

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # технические требования
    technical_requirements = relationship("TechnicalRequirement", back_populates="machine")

    def __repr__(self):
        return f"<Machine {self.name}>"
