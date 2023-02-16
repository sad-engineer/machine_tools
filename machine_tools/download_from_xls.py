#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
from tkinter.filedialog import askopenfilenames
import pandas as pd
import sqlite3

from machine_tools.fun import connect
from machine_tools.obj.exceptions import InvalidValue

PATH_DB = "data\\machine_tools_pro.db"



def save_table(table, name, path=PATH_DB):
    db, cursor = connect(path)
    table.to_sql(name, db, if_exists='replace', index=False)
    db.commit()


def update_main_table(path):
    data_df = pd.read_excel(path, sheet_name="Sheet1")
    save_table(table=data_df, name="machine_tools",)


def get_name(path):
    """Определяет имя станка по пути файла паспортных данных"""
    name = path.split("/")[-1]
    name = name.replace(".xlsx", "")
    name = name.replace(".xls", "")
    if name == 'machine_tools':
        return name
    if name.find("_") != -1:
        name = name.replace("_",".")
    return name


def is_name_in_main_table(name, path=PATH_DB) -> bool:
    """Проверяет, есть ли name в главной таблице"""
    db, cursor = connect(path)
    data = pd.read_sql(f"SELECT * FROM machine_tools WHERE Станок = '{name}'", db)
    if len(data) == 1:
        return True
    elif len(data) > 1:
        raise InvalidValue(f"Имя станка {name} в таблице 'machine_tools' встречается несколько раз.")
    return False


def download_from_xls():
    """ Загружает данные из файлов эксель с обновлением главной таблицы"""
    path_main_table = __file__.replace("download_from_xls.py", "tables_new\\machine_tools.xlsx")
    update_main_table(path_main_table)
    paths = askopenfilenames(title="Выберите таблицы паспортных данных станков",
                             filetypes=(("Эксель файл", "*.xls *.xlsx"),))
    for path in paths:
        name = get_name(path)
        if name != 'machine_tools':
            if is_name_in_main_table(name):
                data_df = pd.read_excel(path, sheet_name="Sheet1")
                save_table(data_df, name)
            else:
                raise InvalidValue(f"Станка {name} нет в таблице 'machine_tools'")


if __name__ == "__main__":
    download_from_xls()


