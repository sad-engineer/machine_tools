#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import sys

from machine_tools_3.app.db.check_connection import check_connection

# Проверяем доступность сервера при импорте модуля
if not check_connection():
    sys.exit(1)

# Импортируем все сервисы
from machine_tools_3.app.services.finder import MachineFinder

__all__ = [
    "MachineFinder",
]
