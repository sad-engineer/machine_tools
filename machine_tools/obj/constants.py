#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------

# Расположение БД
DEFAULT_SETTINGS_FOR_DB= {
    'path': f"{__file__}".replace("obj\\constants.py", "data\\machine_tools.db"),
    'requester_type': "sqlite",
    'reader_type': 'list_dict',
    'tablename': 'machine_tools'
}

# Настройка начальных данных
# DEFAULT_SETTINGS_FOR_MACHINE_TOOL = {
#     "milling": {"name": "6Р82", "quantity": 1, "hard_mftd": 0},
#     "turning": {"name": "16К20", "quantity": 1, "hard_mftd": 0},
#     "planing": {"name": "7212", "quantity": 1, "hard_mftd": 0},
#     "drilling": {"name": "2М112", "quantity": 1, "hard_mftd": 0},
#     "countersinking": {"name": "2М112", "quantity": 1, "hard_mftd": 0},
#     "deployment": {"name": "2М112", "quantity": 1, "hard_mftd": 0},
#     "broaching": {"name": "7Б55", "quantity": 1, "hard_mftd": 0},
#     }
DEFAULT_SETTINGS_FOR_MACHINE_TOOL = {"name": "16К20", "quantity": 1, "hard_mftd": 0}

# Описание параметра "Жесткость системы СПИД":
HARD_MFTD = {None: "Без указания", 0: "Малая жесткость", 1: "Средняя жесткость", 2: "Высокая жесткость"}
# Описание типов автоматизации
TYPES_OF_AUTOMATION = {None: "Без указания", 0: 'Ручной', 1: 'Полуавтомат', 2: 'Автомат'}
# Описание типов специализации
TYPES_OF_SPECIALIZATION = {None: "Без указания", 0: 'Специализированный', 1: 'Универсальный', 2: 'Специальный'}

