#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
from typing import Optional, Union

from machine_tools.find import characteristics, passport_data
from machine_tools.obj.constants import \
    DEFAULT_SETTINGS_FOR_MACHINE_TOOL as DEFAULT_SETTINGS
from machine_tools.obj.constants import (INDEXES_OF_HARD_MFTD,
                                         NAMES_OF_HARD_MFTD)
from machine_tools.obj.exceptions import InvalidValue


class MachineTool:
    """Параметры применяемого оборудования"""

    def __init__(
        self,
        kind_of_cut: str = "milling",
        name: Optional[str] = None,  # Наименование выбранного станка
        quantity: Optional[int] = 1,  # количество станков
        # Жесткость системы СПИД: станок, приспособление, инструмент, деталь - machine, fixture, tool, detail
        hard_mftd: Optional[Union[str, int]] = None,
    ):
        self.kind_of_cut = kind_of_cut
        self.quantity = quantity
        self.hard_mftd = hard_mftd
        (
            self.update_chars(name)
            if not isinstance(name, type(None))
            else self.get_default_settings()
        )
        # Тип строгального станка. Задать только для строгального станка:
        # 0-продольно строгальный, 1-поперечно строгальный, 2-долбежный
        self.type_of_planing_machine: Optional[int] = None

    def __calculate_spindle_power(self) -> None:
        """Рассчитывает мощность шпинделя"""
        performance = (
            self.performance_proc if hasattr(self, "performance_proc") else None
        )
        n_lathe_passport = (
            self.power_lathe_passport_kvt
            if hasattr(self, "power_lathe_passport_kvt")
            else None
        )
        self.spindle_power = None
        if not isinstance(n_lathe_passport, type(None)) and not isinstance(
            performance, type(None)
        ):
            self.spindle_power = n_lathe_passport * performance

    def show(self):
        report = f"""
        ### Параметры применяемого оборудования ###
            Наименование выбранного станка: {self.name}.
            КПД станка: {self.performance_proc*100}%.
            Мощность главного двигателя станка = {self.power_lathe_passport_kvt} кВт.
            Мощность шпинделя станка = {self.spindle_power} кВт.
            Габаритные характеристики станка (длина х ширина х высота): {self.length} x {self.width} x {self.height} мм.
            Масса станка = {self.weight} кг.
            Класс автоматизации станка: {self.automation}.
            Класс точности станка по ГОСТ 8-82: {self.accuracy}. 
            Класс специализации станка: {self.specialization}.
            Группа станка по виду обработки: {self.group}.
            Тип станка по виду обработки: {self.machine_type}.
            Количество станков: {self.quantity} шт.
            Жесткость системы СПИД: {self.hard_mftd}."""
        print(report)

    def get_default_settings(self) -> None:
        """Настраивает атрибуты класса в соответствии с
        глобальными дефолтными настройками"""
        for setting_name, setting_val in DEFAULT_SETTINGS[self.kind_of_cut].items():
            (
                self.update_chars(name=setting_val)
                if setting_name == "name"
                else setattr(self, setting_name, setting_val)
            )
        self.__calculate_spindle_power()

    def update_chars(self, name: Optional[str] = None) -> None:
        """Запрашивает паспортные данные станка в БД и определяет характеристики класса в соответствии с
        паспортными данными
        """
        if not isinstance(name, type(None)):
            self.name = name
            # Запрашиваем характеристики станка в БД
            chars = characteristics(name)
            self.performance_proc = float(chars["КПД"][0])
            self.power_lathe_passport_kvt = float(chars["Мощность"][0])
            self.type_of_planing_machine = None
            self.city = str(chars["Город"][0])
            self.manufacturer = str(chars["Производитель"][0])
            self.length = float(chars["Длина"][0])
            self.width = float(chars["Ширина"][0])
            self.height = float(chars["Высота"][0])
            self.weight = float(chars["Масса"][0])
            # self.class_by_weight = chars["Классификация_по_массе"][0]
            self.automation = str(chars["Автоматизация"][0])
            self.accuracy = str(chars["Точность"][0])
            self.specialization = str(chars["Специализация"][0])
            self.group = (
                int(chars["Группа"][0])
                if not isinstance(chars["Группа"][0], type(None))
                else 0
            )
            self.machine_type = (
                int(chars["Тип"][0])
                if not isinstance(chars["Тип"][0], type(None))
                else 0
            )
            # Запрашиваем паспортные данные станка в БД
            self.passport_data = passport_data(name)

            self.__calculate_spindle_power()
        else:
            print("Необходимо ввести наименование станка!")

    def update_hard_mftd(self, hard_mftd: Optional[Union[str, int]] = None):
        """Проверяет значение параметра "Жесткость системы СПИД". При корректном значении устанавливает тип параметра."""
        if isinstance(hard_mftd, type(None)):
            print("Параметр 'Жесткость системы СПИД' не был передан")
        else:
            if isinstance(hard_mftd, int):
                if hard_mftd in NAMES_OF_HARD_MFTD:
                    self.hard_mftd = hard_mftd
                else:
                    message = {
                        "Индекс параметра 'Жесткость системы СПИД' не определен."
                    }
                    raise InvalidValue(message)
            elif isinstance(hard_mftd, str):
                if hard_mftd in INDEXES_OF_HARD_MFTD:
                    self.hard_mftd = INDEXES_OF_HARD_MFTD[hard_mftd]
                else:
                    message = {"Параметр 'Жесткость системы СПИД' не определен."}
                    raise InvalidValue(message)
            else:
                message = {"Параметр 'Жесткость системы СПИД' не определен."}
                raise InvalidValue(message)

    def clear_characteristics(self) -> None:
        """Производит очистку всех характеристик"""
        self.name = None
        self.performance_proc = None
        self.power_lathe_passport_kvt = None
        self.type_of_planing_machine = None
        self.city = None
        self.manufacturer = None
        self.length = None
        self.width = None
        self.height = None
        self.weight = None
        self.class_by_weight = None
        self.automation = None
        self.accuracy = None
        self.specialization = None
        self.group = None
        self.machine_type = None
        self.passport_data = None
        self.spindle_power = None


"""
#TODO: Список задач в данном модуле программе:
    Добавить классификацию по точности, массе, автоматизации, специализации
    Добавить габарит рабочего пространства
"""
