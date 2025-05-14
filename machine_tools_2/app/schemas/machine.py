#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from machine_tools_2.app.models.machine import (
    AccuracyClass,
    AutomationType,
    MachineGroup,
    MachineType,
    PlaningMachineType,
    SpecializationType,
    WeightClass,
)


class MachineBase(BaseModel):
    name: str = Field(..., description="Название станка")

    # Габаритные размеры и вес
    length: Optional[float] = Field(None, description="Длина станка")
    width: Optional[float] = Field(None, description="Ширина станка")
    height: Optional[float] = Field(None, description="Высота станка")
    weight: Optional[float] = Field(None, description="Вес станка")

    # Производитель
    manufacturer: Optional[str] = Field(None, description="Производитель")
    city: Optional[str] = Field(None, description="Город производителя")

    # Классификация
    machine_type: MachineType = Field(..., description="Тип станка")
    group: Optional[MachineGroup] = Field(None, description="Группа станка")
    type_of_planing_machine: Optional[PlaningMachineType] = Field(
        None, description="Тип строгального станка"
    )
    class_by_weight: Optional[WeightClass] = Field(None, description="Класс по весу")

    # Технические характеристики
    performance_proc: Optional[float] = Field(None, description="КПД обработки")
    power_lathe_passport_kvt: Optional[float] = Field(
        None, description="Мощность станка по паспорту, кВт"
    )
    spindle_power: Optional[float] = Field(None, description="Мощность шпинделя")
    automation: Optional[AutomationType] = Field(None, description="Тип автоматизации")
    accuracy: Optional[AccuracyClass] = Field(None, description="Класс точности")
    specialization: Optional[SpecializationType] = Field(
        None, description="Специализация"
    )

    # Дополнительные данные
    passport_data: Optional[Dict[str, Any]] = Field(
        None, description="Паспортные данные"
    )


class MachineCreate(MachineBase):
    pass


class MachineUpdate(MachineBase):
    name: Optional[str] = None
    machine_type: Optional[MachineType] = None


class MachineInDB(MachineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Machine(MachineInDB):
    pass
