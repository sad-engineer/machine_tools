#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable
from abc import abstractmethod
from pydantic import ValidationError

from service import logged
from service import output_debug_message_for_init_method as debug_message_for_init

from machine_tools.obj.finders import Finder
from machine_tools.obj.entities import MachineTool
from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_MACHINE_TOOL as DEF_SET
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
class Creator:
    """ Создает класс станок с параметрами из БД"""
    @abstractmethod
    @debug_message_for_init()
    def __init__(self,
                 finder_provider: Callable[..., Finder],
                 ):
        self._finder = finder_provider

        self.data = {}

    def _prepare_data(self, raw_data: dict):
        data = dict({"name": raw_data['Станок']})
        data["name"] = DEF_SET['quantity']
        data["hard_mftd"] = DEF_SET['hard_mftd']
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
    def by_name(self, any_name: str):
        rows = self._finder().by_name(any_name)
        data = self._prepare_data(rows[0])
        try:
            return MachineTool.parse_obj(data)
        except Exception as error:
            return ErrorWithData(err=error, name=MachineTool.__name__, params=data)
    #
    # @property
    # def create_all(self):
    #     for row in self._finder().all:
    #         name = row['Станок']
    #         yield self.by_name(name)
    #
    # def by_type(self, machine_type):
    #     for row in self._finder().by_type(machine_type):
    #         name = row['Станок']
    #         yield self.by_name(name)
    #
    # def by_group(self, machine_group):
    #     for row in self._finder().by_group(machine_group):
    #         name = row['Станок']
    #         yield self.by_name(name)
    #
    # def by_type_and_group(self, machine_type, machine_group):
    #     for row in self._finder().by_type_and_group(machine_group=machine_group, machine_type=machine_type):
    #         name = row['Станок']
    #         yield self.by_name(name)


