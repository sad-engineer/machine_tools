#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
import sys

from machine_tools.app.db.check_connection import check_connection

# Проверяем, что это импорт пакета, а не запуск скрипта
if not os.path.basename(sys.argv[0]) == "check_connection.py":
    # Проверяем доступность сервера при импорте модуля
    if not check_connection():
        sys.exit(1)

# Импортируем все сервисы
from machine_tools.app.services.finder import MachineFinder

__all__ = [
    "MachineFinder",
]
