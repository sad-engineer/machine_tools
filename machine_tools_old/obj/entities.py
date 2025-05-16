#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
from collections import namedtuple
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt, confloat

from machine_tools_old.obj.fields_types import InHardMFTD, InTypesOfAutomation, InTypesOfSpecialization

ErrorWithData = namedtuple("ErrorWithData", ["err", "name", "params"])  # для сохранения данных с ошибкой


class MachineTool(BaseModel):
    """Параметры оборудования"""

    name: str = Field(..., description="Наименование станка")
    quantity: Optional[PositiveInt] = Field(None, description="Количество станков")
    hard_mftd: Optional[InHardMFTD] = Field(None, description="Жесткость системы СПИД")
    performance_proc: Optional[confloat(ge=0, le=1)] = Field(None, description="КПД станка")
    power_lathe_passport_kvt: Optional[PositiveFloat] = Field(None, description="Мощность главного двигателя")
    city: Optional[str] = Field(None, description="Город производителя")
    manufacturer: Optional[str] = Field(None, description="Производитель")
    length: Optional[PositiveFloat] = Field(None, description="Длина станка")
    width: Optional[PositiveFloat] = Field(None, description="Ширина станка")
    height: Optional[PositiveFloat] = Field(None, description="Высота станка")
    weight: Optional[PositiveFloat] = Field(None, description="Масса станка")
    automation: Optional[InTypesOfAutomation] = Field(None, description="Класс автоматизации")
    accuracy: Optional[str] = Field(None, description="Класс точности")
    specialization: Optional[InTypesOfSpecialization] = Field(None, description="Класс специализации")
    group: Optional[confloat(ge=0, le=9)] = Field(None, description="Группа станка")
    machine_type: Optional[confloat(ge=0, le=9)] = Field(None, description="Тип станка")
    passport_data: Optional[Any] = Field(None, description="Паспортные данные")

    model_config = ConfigDict(arbitrary_types_allowed=True)


if __name__ == "__main__":
    machine_tool = MachineTool(name="16К20")
    print(machine_tool)


"""
#TODO: Список задач в данном модуле программе:
    Добавить классификацию по точности, массе, автоматизации, специализации
    Добавить габарит рабочего пространства
"""
