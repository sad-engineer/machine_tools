#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
# import os
# import sys
#
# from machine_tools.app.db.check_connection import check_connection
#
# # Проверяем, что это импорт пакета, а не запуск скрипта
# if not os.path.basename(sys.argv[0]) == "check_connection.py":
#     # Проверяем доступность сервера при импорте модуля
#     if not check_connection():
#         sys.exit(1)
#
# # Импортируем все сервисы
# from machine_tools.app.finders.finder import MachineFinder
#
# __all__ = [
#     "MachineFinder",
# ]

from machine_tools.app.services.finder_getters import (
    get_finder_with_dict_info,
    get_finder_with_dict_names,
    get_finder_with_indexed_info,
    get_finder_with_indexed_names,
    get_finder_with_list_info,
    get_finder_with_list_names,
)
from machine_tools.app.services.scripts import FinderContainer, find_names, get_machine_info_by_name

__all__ = [
    "FinderContainer",
    "get_finder_with_list_names",
    "get_finder_with_list_info",
    "get_finder_with_dict_names",
    "get_finder_with_dict_info",
    "get_finder_with_indexed_names",
    "get_finder_with_indexed_info",
    "find_names",
    "get_machine_info_by_name",
]
