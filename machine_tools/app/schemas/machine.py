#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat, PositiveFloat, PositiveInt, confloat, conint

from machine_tools.app.enumerations import Accuracy, Automation, SoftwareControl, Specialization, WeightClass


class Dimensions(BaseModel):
    """Габариты станка"""

    length: Optional[PositiveInt] = Field(None, description="Длина станка в мм")
    width: Optional[PositiveInt] = Field(None, description="Ширина станка в мм")
    height: Optional[PositiveInt] = Field(None, description="Высота станка в мм")
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
    # В БД есть инфа по приспособлениям (например УДГ Н-100), у каоторых power = 0
    power: Optional[NonNegativeFloat] = Field(None, description="Мощность станка в кВт")
    efficiency: Optional[confloat(ge=0, le=1)] = Field(None, description="КПД станка")
    accuracy: Accuracy = Field(Accuracy.NO_DATA, description="Класс точности станка")
    automation: Automation = Field(Automation.MANUAL, description="Уровень автоматизации")
    software_control: SoftwareControl = Field(SoftwareControl.NO, description="Тип программного управления")
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
    """Схема для обновления станка"""

    def get_flat_dict(self) -> Dict[str, Any]:
        """
        Возвращает плоский словарь значений без вложенных структур,
        кроме technical_requirements.

        Returns:
            Dict[str, Any]: Словарь с данными для обновления
        """
        data = self.model_dump()

        # Обрабатываем dimensions
        if self.dimensions:
            data.update(
                {
                    'length': self.dimensions.length,
                    'width': self.dimensions.width,
                    'height': self.dimensions.height,
                    'overall_diameter': self.dimensions.overall_diameter,
                }
            )
        data.pop('dimensions', None)

        # Обрабатываем location
        if self.location:
            data.update({'city': self.location.city, 'manufacturer': self.location.manufacturer})
        data.pop('location', None)

        # Преобразуем Enum значения в строки
        if isinstance(data.get('accuracy'), Accuracy):
            data['accuracy'] = data['accuracy'].value
        if isinstance(data.get('automation'), Automation):
            data['automation'] = data['automation'].value
        if isinstance(data.get('specialization'), Specialization):
            data['specialization'] = data['specialization'].value
        if isinstance(data.get('weight_class'), WeightClass):
            data['weight_class'] = data['weight_class'].value
        if isinstance(data.get('software_control'), SoftwareControl):
            data['software_control'] = data['software_control'].value
        return data


class MachineInDBBase(MachineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Machine(MachineInDBBase):
    pass
