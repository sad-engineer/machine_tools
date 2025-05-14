#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
machine_tools - модуль для работы с базой данных станков.

Этот модуль предоставляет:
- Константы для настройки базы данных и станков
- Классы для работы со станками
- Контейнеры для внедрения зависимостей
"""
from machine_tools.obj.constants import HARD_MFTD  # Жесткость системы СПИД
from machine_tools.obj.constants import TYPES_OF_AUTOMATION  # Типы автоматизации
from machine_tools.obj.constants import TYPES_OF_SPECIALIZATION  # Типы специализации
from machine_tools.obj.constants import TYPES_PROCESSING  # Типы обработки
from machine_tools.obj.constants import (  # Настройки базы данных; Настройки станков; Справочники
    DEFAULT_SETTINGS_FOR_DB,
    DEFAULT_SETTINGS_FOR_MACHINE_TOOL,
    DEFAULT_SETTINGS_FOR_MACHINE_TOOL_BY_TYPE_PROCESSING,
)

# Импорты классов
from machine_tools.obj.containers import MachineToolsContainer
from machine_tools.obj.entities import MachineTool

# Алиасы для удобства использования
MachineToolsFinder = MachineToolsContainer.finder
MachineToolsCreator = MachineToolsContainer.creator
MachineToolsLister = MachineToolsContainer.lister

__all__ = [
    # Константы
    "DEFAULT_SETTINGS_FOR_DB",
    "DEFAULT_SETTINGS_FOR_MACHINE_TOOL",
    "DEFAULT_SETTINGS_FOR_MACHINE_TOOL_BY_TYPE_PROCESSING",
    "HARD_MFTD",
    "TYPES_OF_AUTOMATION",
    "TYPES_OF_SPECIALIZATION",
    "TYPES_PROCESSING",
    # Классы
    "MachineToolsContainer",
    "MachineToolsFinder",
    "MachineToolsCreator",
    "MachineToolsLister",
    "MachineTool",
]
