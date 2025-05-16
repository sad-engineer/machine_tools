#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        find
# Purpose:     Contains the functions of working with the database for the machine_tools_old
#
# Author:      ANKorenuk
#
# Created:     28.10.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит функции работы с базой данных по станкам
# -------------------------------------------------------------------------------
from typing import Optional, Union

import pandas as pd

from machine_tools_old.fun import connect
from machine_tools_old.obj.constants import PATH_DB_FOR_TOOLS as PATH_DB
from machine_tools_old.obj.exceptions import CalculationIsNotDefined, ReceivedEmptyDataFrame, UnexpectedDataInDataFrame


def list_mt(
    group: Optional[Union[int, float]] = None,
    type_: Optional[Union[int, float]] = None,
    path_bd: str = PATH_DB,
) -> list:
    """Открывает базу данных по станкам (по пути 'path_db'), запрашивает
    список всех доступных станков по соответствию группы ("machine_group") и
    типа ("machine_type") станков.
    Возвращает сортированный список.

    Parameters
    ----------
    group : int, float, optional
        Группа станков (от update_relationships.py до 9 вкл.)
        По умолчанию : None
    type_ : int, float, optional
        Тип станков в группе (от update_relationships.py до 9 вкл.)
        По умолчанию : None
    path_bd : str, optional
        Путь к базе данных по материалам

    Returns
    -------
    list_names : list
        Сортированный список имен станков, доступных в БД .
    """
    if not isinstance(group, type(None)) and not isinstance(type_, type(None)):
        request = f"SELECT * FROM machine_tools WHERE Группа = '{group}' AND Тип = '{type_}'"
    elif not isinstance(group, type(None)) and isinstance(type_, type(None)):
        request = f"SELECT * FROM machine_tools WHERE Группа = '{group}'"
    elif isinstance(group, type(None)) and not isinstance(type_, type(None)):
        request = f"SELECT * FROM machine_tools WHERE Тип = '{type_}'"
    else:
        message = "Необходимо передать либо тип станка, либо группу станка. либо и то и другое."
        raise CalculationIsNotDefined(message)
    db, cursor = connect(path_bd)
    table_mt_by_choice = pd.read_sql(request, db)
    db.close()
    list_names = list(table_mt_by_choice["Станок"])
    return sorted(set(list_names))


def characteristics(name: str = "5В12", path_bd: str = PATH_DB) -> pd.DataFrame:
    """Запрашивает из БД характеристики станка.

    Parameters
    ----------
    name : str, optional
        Наименование станка. По умолчанию : "5В12".
    path_bd : str, optional
        Путь к базе данных по материалам.

    Returns
    -------
    characteristic : pd.DataFrame
        Возвращает DataFrame, содержащий характеристики станка.
    """
    db, cursor = connect(path_bd)
    characteristic = pd.read_sql(f"SELECT * FROM machine_tools WHERE Станок = '{name}'", db)
    db.close()
    if len(characteristic) != 1:
        if len(characteristic) == 0:
            message = f"Получена пустая таблица характеристик станка:{name}. Проверьте данные БД: {path_bd}"
            raise ReceivedEmptyDataFrame(message)
        elif len(characteristic) > 1:
            message = (
                f"Таблица характеристик станка содержит больше одной строки. Проверь запрос, или данные БД: "
                "{path_bd}. Должна быть одна строка!"
            )
            raise UnexpectedDataInDataFrame(message)
    else:
        characteristic = characteristic.drop(columns="index")
        return characteristic


def passport_data(name: str = "5В12", path_bd: str = PATH_DB) -> pd.DataFrame:
    """Запрашивает из БД таблицу паспортных данных станка.

    Parameters
    ----------
    name : str, optional
        Наименование станка. По умолчанию : "5В12".
    path_bd : str, optional
        Путь к базе данных по материалам.

    Returns
    -------
    data : pd.DataFrame
        Возвращает DataFrame, содержащий паспортные данные станка, если в БД существует таблица паспортных данных.
    """
    data = None
    db, cursor = connect(path_bd)
    is_exists = cursor.execute(
        f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}'"
    ).fetchone()[0]
    if is_exists:
        data = pd.read_sql(f"SELECT * FROM '{name}'", db)
    db.close()
    if isinstance(data, type(None)):
        message = f"База данных не содержит паспортных данных для станка {name}."
        raise UnexpectedDataInDataFrame(message)
    if len(data) < 1:
        message = f"Получена пустая таблица паспортных данных станка:{name}. Проверьте данные БД: {path_bd}"
        raise ReceivedEmptyDataFrame(message)
    data = data.drop(columns="index")
    data.rename(columns={name: "Значение"}, inplace=True)
    return data


if __name__ == "__main__":
    print(list_mt(1, 1))
    print(characteristics())
    print(passport_data())
