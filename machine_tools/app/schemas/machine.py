#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt, confloat, conint

from machine_tools.app.enumerations import Accuracy, Automation, Specialization, WeightClass


class Dimensions(BaseModel):
    """Габариты станка"""

    length: Optional[PositiveFloat] = Field(None, description="Длина станка в мм")
    width: Optional[PositiveFloat] = Field(None, description="Ширина станка в мм")
    height: Optional[PositiveFloat] = Field(None, description="Высота станка в мм")
    overall_diameter: Optional[str] = Field(None, description="Габаритный диаметр станка")


class Location(BaseModel):
    """Информация о местоположении"""

    city: Optional[str] = Field(None, description="Город производителя")
    manufacturer: Optional[str] = Field(None, description="Название производителя")


class MachineInfo(BaseModel):
    """Полная информация о станке"""

    name: str = Field(..., min_length=1, description="Название станка (например, '16К20')")
    group: Optional[conint(ge=0, le=9)] = Field(None, description="Группа станка")
    type: Optional[conint(ge=0, le=9)] = Field(None, description="Тип станка")
    power: Optional[PositiveFloat] = Field(None, description="Мощность станка в кВт")
    efficiency: Optional[confloat(ge=0, le=1)] = Field(None, description="КПД станка")
    accuracy: Accuracy = Field(Accuracy.NO_DATA, description="Класс точности станка")
    automation: Automation = Field(Automation.MANUAL, description="Уровень автоматизации")
    specialization: Specialization = Field(Specialization.UNIVERSAL, description="Специализация станка")
    weight: Optional[PositiveFloat] = Field(None, description="Масса станка в кг")
    weight_class: WeightClass = Field(WeightClass.LIGHT, description="Класс станка по массе")
    dimensions: Optional[Dimensions] = Field(None, description="Габариты станка")
    location: Optional[Location] = Field(None, description="Информация о местоположении")
    machine_type: Optional[str] = Field(None, min_length=1, description="Тип станка (например, 'Токарный')")
    technical_requirements: Optional[Dict[str, Any]] = Field(None, description="Технические требования станка")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,  # Включаем валидацию при присваивании
    )


class MachineBase(MachineInfo):
    pass


class MachineCreate(MachineBase):
    pass


class MachineUpdate(MachineBase):
    pass


class MachineInDBBase(MachineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Machine(MachineInDBBase):
    pass
