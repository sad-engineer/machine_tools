#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        machine_tool
# Purpose:     Parameters of the equipment used
#
# Author:      ANKorenuk
#
# Created:     09.04.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Параметры применяемого оборудования
# -------------------------------------------------------------------------------
from typing import Optional, Union
from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_MACHINE_TOOL as DEFAULT_SETTINGS
from machine_tools.find import characteristics
from machine_tools.find import passport_data


class MachineTool():
    """Параметры применяемого оборудования"""
    def __init__(self,
                 kind_of_cut:str='milling',
                 name:Optional[str] = None,                     # Наименование выбранного станка
                 quantity:Optional[int] = 1,                    # количество станков
                 hard_MFTD:Optional[Union[str, int]] = None):   # Жесткость системы СПИД: станок, приспособление, инструмент, деталь - machine, fixture, tool, detail
        self.kind_of_cut = kind_of_cut
        self.update_chars(name)
        self.__calculate_spindle_power
        self.quantity = quantity
        self.hard_MFTD = hard_MFTD
        self.type_of_planing_machine:Optional[int] = None # Тип строгального станка. Задать долько для строгального станка: 0-продольно строгальный, 1-поперечно строгальный, 2-долбежный
        self.get_default_settings


    @property    
    def __calculate_spindle_power(self) -> None:
        """ Расчитывает мощность шпинделя """
        if hasattr(self, "performance_proc"):
            performance = self.performance_proc
        else:
            performance = None
        if hasattr(self, "power_lathe_passport_kVt"): 
            N_lathe_passport = self.power_lathe_passport_kVt
        else:
            N_lathe_passport = None
        
        self.spindle_power = None
        if not isinstance(N_lathe_passport, type(None)) and not isinstance(performance, type(None)):
            self.spindle_power = N_lathe_passport * performance
        
        
    @property    
    def show(self):
        report = f"""
        ### Параметры применяемого оборудования ###
            Наименование выбранного станка: {self.name}.
            КПД станка: {self.performance_proc*100}%.
            Мощность главного двигателя станка = {self.power_lathe_passport_kVt} кВт.
            Мощность шпинделя станка = {self.spindle_power} кВт.
            Габаритные характеристики станка (длина х ширина х высота): {self.length} x {self.width} x {self.height} мм.
            Масса станка = {self.weight} кг.
            Класс автоматизации станка: {self.automation}.
            Класс точности станка по ГОСТ 8-82: {self.accuracy}. 
            Класс специализации станка: {self.specialization}.
            Группа станка по виду обработки: {self.group}.
            Тип станка по виду обработки: {self.machine_type}.
            Количество станков: {self.quantity} шт.
            Жесткость системы СПИД: {self.hard_MFTD}."""
        print(report)
        
        
    @property
    def get_default_settings(self) -> None:
        """ Настраивает атрибуты класса в соответствии с 
        глобальными дефолтными настрйками"""
        for setting_name, setting_val in DEFAULT_SETTINGS[self.kind_of_cut].items():
            self.update_chars(name = setting_val) if setting_name == "name" else setattr(self, setting_name, setting_val)
        self.__calculate_spindle_power

        
    def update_chars(self, name:Optional[str]=None) -> None:
        """ Запрашивает паспортные данные станка в БД и определяет характеристики класса в соответствии с
        паспортными данными
        """
        if not isinstance(name, type(None)):
            self.name = name
            # Запрашиваем характеристики станка в БД
            chars = characteristics(name)
            self.performance_proc = float(chars["КПД"][0])
            self.power_lathe_passport_kVt = float(chars["Мощность"][0])
            self.type_of_planing_machine = None
            self.city   = str(chars["Город"][0])
            self.manufacturer = str(chars["Производитель"][0])
            self.length = float(chars["Длина"][0])
            self.width  = float(chars["Ширина"][0])
            self.height = float(chars["Высота"][0])
            self.weight = float(chars["Масса"][0])
            # self.class_by_weight = chars["Классификация_по_массе"][0]
            self.automation = str(chars["Автоматизация"][0])
            self.accuracy = str(chars["Точность"][0])
            self.specialization = str(chars["Специализация"][0])
            self.group = int(chars["Группа"][0]) if not isinstance(chars["Группа"][0], type(None)) else 0
            self.machine_type = int(chars["Тип"][0]) if not isinstance(chars["Тип"][0], type(None)) else 0
            # Запрашиваем паспортные данные станка в БД
            self.passport_data = passport_data(name)
            self.__calculate_spindle_power
        else:
            print("Необходимо ввести наименование станка!")


    def update_hard_MFTD(self, hard_MFTD:Optional[Union[str, int]] = None):
        """ Проверяет значение параметра "Жесткость системы СПИД". При корректном значении устанавливает тип параметра.
        """
        if  isinstance(hard_MFTD, type(None)):
            print("Параметр 'Жесткость системы СПИД' не был передан")
        else:
            if isinstance(hard_MFTD, int):
                if hard_MFTD in NAMES_OF_HARD_MFTD:
                    self.hard_MFTD = hard_MFTD
                else:
                    message = {"Индекс параметра 'Жесткость системы СПИД' не определен."}
                    raise InvalidValue(message)
            elif isinstance(hard_MFTD, str):
                if hard_MFTD in INDEXES_OF_HARD_MFTD:
                    self.hard_MFTD = INDEXES_OF_HARD_MFTD[hard_MFTD]
                else:
                    message = {"Параметр 'Жесткость системы СПИД' не определен."}
                    raise InvalidValue(message)
            else:
                message = {"Параметр 'Жесткость системы СПИД' не определен."}
                raise InvalidValue(message)


    @property
    def clear_characteristics(self) -> None:
        """ Производит очистку всех характеристик """
        self.name = None
        self.performance_proc = None
        self.power_lathe_passport_kVt = None
        self.type_of_planing_machine = None 
        self.city   = None
        self.manufacturer = None 
        self.length = None
        self.width  = None
        self.height = None
        self.weight =None
        self.class_by_weight = None
        self.automation = None
        self.accuracy = None
        self.specialization =None
        self.group = None
        self.machine_type = None
        self.passport_data = None
        self.spindle_power = None

"""
#TODO: Список задач в данном модуле программе:
    Добавить классификацию по точности, массе, автоматизации, специализации
    Добавить габарит рабочего пространства
"""
