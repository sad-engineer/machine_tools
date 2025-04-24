#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable
from abc import abstractmethod
from pydantic import ValidationError
from pydantic import PositiveInt

from service_for_my_projects import logged
from service_for_my_projects import output_debug_message_for_init_method as debug_message_for_init

from machine_tools.obj.finders import MachineToolsFinder
from machine_tools.obj.entities import MachineTool
from machine_tools.obj.fields_types import InHardMFTD, InTypesOfProcessing
from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_MACHINE_TOOL as DEF_SET
from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_MACHINE_TOOL_BY_TYPE_PROCESSING as DEF_SET_BY_TYPE_PROC
from machine_tools.obj.entities import ErrorWithData


def output_debug_message():
    """Логирует создание объекта (экземпляра модели данных). При ошибке создания - логирует ошибку."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not isinstance(result, (ErrorWithData, type(None))) and self._verbose:
                self.debug(f"Создан экземпляр класса {result.__class__.__name__}: {result.name}.")
            return result
        return wrapper
    return decorator


def output_error_message():
    """Логирует ошибку создания объекта (экземпляра модели данных)."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not isinstance(result, ErrorWithData):
                return result
            if isinstance(result.err, ValueError):
                self.error(f"Переданные данные не соответствуют ожидаемой схеме модели {result.name}."
                           f"Данные, загружаемые в модель: {result.params}.")
            elif isinstance(result.err, TypeError):
                self.error(f"Данные, загружаемые в модель должны быть словарем. "
                           f"Полученный тип данных: {type(result.params)}.")
            elif isinstance(result.err, ValidationError):
                self.error(f"Входные данные содержат неверные значения для полей модели {result.name}."
                           f"Данные, загружаемые в модель: {result.params}.")
            elif isinstance(result.err, AttributeError):
                self.error(f"Входные данные содержат неверные значения для полей модели {result.name}."
                           f"Данные, загружаемые в модель: {result.params}.")
            else:
                self.error(f"Ошибка создания экземпляра класса {result.name} с параметрами {result.params}."
                           f"Данные, загружаемые в модель: {result.params}.")
        return wrapper
    return decorator


@logged
class MachineToolsCreator:
    """ Создает класс станок с параметрами из БД"""
    @abstractmethod
    @debug_message_for_init()
    def __init__(self,
                 finder_provider: Callable[..., MachineToolsFinder],
                 ):
        self._finder = finder_provider()

        self._verbose = True
        self.data = {}

    @staticmethod
    def _prepare_data(raw_data: dict,
                      quantity: PositiveInt = DEF_SET['quantity'],
                      hard_mftd: InHardMFTD = DEF_SET['hard_mftd']):
        data = dict({"name": raw_data['Станок']})
        data["quantity"] = quantity
        data["hard_mftd"] = hard_mftd
        data["performance_proc"] = raw_data['КПД']
        data["power_lathe_passport_kvt"] = raw_data['Мощность']
        data["city"] = raw_data['Город']
        data["manufacturer"] = raw_data['Производитель']
        data["length"] = raw_data['Длина']
        data["width"] = raw_data['Высота']
        data["height"] = raw_data['Ширина']
        data["weight"] = raw_data['Масса']
        data["automation"] = raw_data['Автоматизация']
        data["accuracy"] = raw_data['Точность']
        data["specialization"] = raw_data['Специализация']
        data["group"] = raw_data['Группа']
        data["machine_type"] = raw_data['Тип']
        data["passport_data"] = raw_data
        return data

    @output_debug_message()
    @output_error_message()
    def by_name(self,
                name: str,
                quantity: PositiveInt = DEF_SET['quantity'],
                hard_mftd: InHardMFTD = DEF_SET['hard_mftd']):
        rows = self._finder.by_name(any_name=name)
        data = self._prepare_data(rows[0], quantity=quantity, hard_mftd=hard_mftd)
        try:
            return MachineTool.construct(**data)
        except Exception as error:
            return ErrorWithData(err=error, name=MachineTool.__name__, params=data)

    def default(self, type_processing: InTypesOfProcessing = "Фрезерование"):
        default_settings = DEF_SET_BY_TYPE_PROC[type_processing]
        return self.by_name(**default_settings)
