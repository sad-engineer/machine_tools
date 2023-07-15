#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
from typing import Optional, Any
from pydantic import BaseModel, confloat, PositiveInt, PositiveFloat
from collections import namedtuple

from machine_tools.obj.fields_types import InHardMFTD, InTypesOfAutomation, InTypesOfSpecialization


ErrorWithData = namedtuple('ErrorWithData', ['err', 'name', 'params'])   # для сохранения данных с ошибкой


class MachineTool(BaseModel):
    """ Параметры оборудования """
    name: str
    quantity: Optional[PositiveInt] = None
    hard_mftd: Optional[InHardMFTD] = None
    performance_proc: Optional[confloat(ge=0, le=1)] = None
    power_lathe_passport_kvt: Optional[PositiveFloat] = None
    city: Optional[str] = None
    manufacturer: Optional[str] = None
    length: Optional[PositiveFloat] = None
    width: Optional[PositiveFloat] = None
    height: Optional[PositiveFloat] = None
    weight: Optional[PositiveFloat] = None
    automation: Optional[InTypesOfAutomation] = None
    accuracy: Optional[str] = None                              # InTypesOfAccuracy # TODO: переделать таблицу
    specialization: Optional[InTypesOfSpecialization] = None
    group: Optional[confloat(ge=0, le=9)] = None
    machine_type: Optional[confloat(ge=0, le=9)] = None
    passport_data: Optional[Any] = None

    class Config:
        validate_assignment = True
        extra = "allow"
        arbitrary_types_allowed = True


if __name__ == '__main__':
    machine_tool = MachineTool(name="16К20")
    print(machine_tool)




"""
#TODO: Список задач в данном модуле программе:
    Добавить классификацию по точности, массе, автоматизации, специализации
    Добавить габарит рабочего пространства
"""
