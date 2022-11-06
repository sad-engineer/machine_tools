#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        constants
# Purpose:     Contains local constants
#
# Author:      ANKorenuk
#
# Created:     2.06.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит локальные переменные
# -------------------------------------------------------------------------------
from pathlib import Path
import os.path
# possible_paths = [str(Path.cwd()) + "\\env\\Lib\\site-packages\\machine_tools\\data\\machine_tools.db",
#                   str(Path.cwd()) + "\\venv\\Lib\\site-packages\\machine_tools\\data\\machine_tools.db",
#                   str(Path.cwd()) + "\\data\\machine_tools.db",
#                   __file__.replace("obj\\constants.py", "data\\machine_tools.db")
#                   ]
# for path in possible_paths:
#     if os.path.exists(path):
#         PATH_DB_FOR_TOOLS = path
PATH_DB_FOR_TOOLS = __file__.replace("obj\\constants.py", "data\\machine_tools.db")
# Настройка начальных данных
DEFAULT_SETTINGS_FOR_MACHINE_TOOL = {
    "milling":{"name": "6Р82", "quantity": 1, "hard_MFTD": 0},
    "turning":{"name": "16К20", "quantity": 1, "hard_MFTD": 0},
    "planing":{"name": "7212", "quantity": 1, "hard_MFTD": 0},
    "drilling":{"name": "2М112", "quantity": 1, "hard_MFTD": 0},
    "countersinking":{"name": "2М112", "quantity": 1, "hard_MFTD": 0},
    "deployment":{"name": "2М112", "quantity": 1, "hard_MFTD": 0},
    "broaching":{"name": "7Б55", "quantity": 1, "hard_MFTD": 0},
    }
# Описание параметра "Жесткость системы СПИД":
NAMES_OF_HARD_MFTD = {None: "Без указания", 0: "Малая жесткость", 1: "Средняя жесткость", 2: "Высокая жесткость"}
INDEXES_OF_HARD_MFTD = {"Без указания": None, "Малая жесткость": 0, "Средняя жесткость": 1, "Высокая жесткость": 2}
