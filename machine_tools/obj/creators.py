#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar, Optional, Union, Callable
from abc import ABC, abstractmethod
import pandas as pd

from machine_tools.obj.finders import Finder
from machine_tools.obj.entities import MachineTool
from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_MACHINE_TOOL as DEF_SET


class Creator(ABC):
    """ создает класс станок с параметрами из БД"""
    @abstractmethod
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

    def by_name(self, any_name: str):
        rows = self._finder().by_name(any_name)
        if len(rows) != 1:
            raise ValueError(f"По наименованию {any_name} в БД не найдено записей, либо найдено несколько записей")
        row = self._prepare_data(rows[0])
        return MachineTool.parse_obj(row)

    @property
    def create_all(self):
        for row in self._finder().all:
            name = row['Станок']
            yield self.by_name(name)

    def by_type(self, machine_type):
        for row in self._finder().by_type(machine_type):
            name = row['Станок']
            yield self.by_name(name)

    def by_group(self, machine_group):
        for row in self._finder().by_group(machine_group):
            name = row['Станок']
            yield self.by_name(name)

    def by_type_and_group(self, machine_type, machine_group):
        for row in self._finder().by_type_and_group(machine_group=machine_group, machine_type=machine_type):
            name = row['Станок']
            yield self.by_name(name)


