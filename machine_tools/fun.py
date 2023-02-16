#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        fun
# Purpose:     Contains local functions for working with the database
#
# Author:      ANKorenuk
#
# Created:     28.10.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит локальные функции работы с БД
# -------------------------------------------------------------------------------
import sqlite3


def connect(filename):
    """
    Создает и подключает базу данных если ее нет. Если БД есть - подключает ее

    Parameters
    ----------
    filename : str
        Имя файла БД.

    Returns
    -------
    db : TYPE
        Указатель на подключенную БД.
    cursor : TYPE
        Указатель на курсор БД.
    """
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    db.commit()
    return db, cursor


def ror(variable: float, order: int = 6) -> float:
    """ Функция округления (round_off_result).
    round - работает не так как надо
    round применяю только для выбора значений из таблиц, для отсечения
    миллионных погрешностей

    Argvs:
        variable - переменная или результат вычислений
        order - точность округления

    Возвращает значение variable, округленное до order-знака после запятой.
    Округляет вверх, если цифра пять и больше.
    """
    if order > 0:
        order = '1.' + '0' * order
        variable = Decimal(variable)
        try:
            variable = variable.quantize(Decimal(order), ROUND_HALF_UP)
        except Exception:
            pass
        variable = float(variable)
    elif order == 0:
        order = '1'
        variable = Decimal(variable)
        variable = variable.quantize(Decimal(order), ROUND_HALF_UP)
        variable = int(variable)
    else:
        order = order * (-1)
        order = '1' + '0' * order
        variable = float(variable // int(order) * int(order))
    return variable
