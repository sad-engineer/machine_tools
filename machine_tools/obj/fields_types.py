#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union, Optional, ClassVar
from pydantic import BaseModel, validator

from machine_tools.obj.constants import HARD_MFTD, TYPES_OF_AUTOMATION, TYPES_OF_SPECIALIZATION, TYPES_PROCESSING


class ValueFromDict:
    """Для определения полей, значение которых должны быть из словаря доступных значений"""
    AVAILABLE_VALUES: ClassVar[dict] = {}

    @classmethod
    def validate(cls, value):
        if not isinstance(value, (int, str)):
            raise ValueError(f"Ожидается целое число или строка, получено: {type(value)}")
        elif isinstance(value, str):
            if value not in cls.AVAILABLE_VALUES.values():
                raise ValueError(f"Строковое значение должно быть из списка {list(cls.AVAILABLE_VALUES.values())}, "
                                 f"получено: {value}")
            return {v: k for k, v in cls.AVAILABLE_VALUES.items()}[value]
        elif isinstance(value, int):
            if value not in cls.AVAILABLE_VALUES:
                raise ValueError(f"Значение должно быть из списка {list(cls.AVAILABLE_VALUES.keys())}, "
                                 f"получено: {value}")
            return value

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class InvertedValueFromDict:
    """ Делает тоже, что и ValueFromDict, но сохраняет строковое значение, а не числовое"""
    AVAILABLE_VALUES: ClassVar[dict] = {}

    @classmethod
    def validate(cls, value):
        if not isinstance(value, (int, str)):
            raise ValueError(f"Ожидается целое число или строка, получено: {type(value)}")
        elif isinstance(value, str):
            if value not in cls.AVAILABLE_VALUES.values():
                raise ValueError(f"Строковое значение должно быть из списка {list(cls.AVAILABLE_VALUES.values())}, "
                                 f"получено: {value}")
            return value
        elif isinstance(value, int):
            if value not in cls.AVAILABLE_VALUES:
                raise ValueError(f"Значение должно быть из списка {list(cls.AVAILABLE_VALUES.keys())}, "
                                 f"получено: {value}")
            return cls.AVAILABLE_VALUES[value]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class InHardMFTD(ValueFromDict):
    AVAILABLE_VALUES = HARD_MFTD


class InTypesOfAutomation(ValueFromDict):
    AVAILABLE_VALUES = TYPES_OF_AUTOMATION


class InTypesOfSpecialization(ValueFromDict):
    AVAILABLE_VALUES = TYPES_OF_SPECIALIZATION


class InTypesOfProcessing(InvertedValueFromDict):
    AVAILABLE_VALUES = TYPES_PROCESSING




