#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Константы пакета
from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_DB
from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_MACHINE_TOOL_BY_TYPE_PROCESSING
from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_MACHINE_TOOL
from machine_tools.obj.constants import HARD_MFTD
from machine_tools.obj.constants import TYPES_OF_AUTOMATION
from machine_tools.obj.constants import TYPES_OF_SPECIALIZATION
from machine_tools.obj.constants import TYPES_PROCESSING
# Методы пакета

# Классы пакета
from machine_tools.obj.containers import MachineToolsContainer
MachineToolsFinder = MachineToolsContainer.finder
MachineToolsCreator = MachineToolsContainer.creator
MachineToolsLister = MachineToolsContainer.lister
from machine_tools.obj.entities import MachineTool

__all__ = [
    # Константы пакета
    "DEFAULT_SETTINGS_FOR_DB",
    "DEFAULT_SETTINGS_FOR_MACHINE_TOOL_BY_TYPE_PROCESSING",
    "DEFAULT_SETTINGS_FOR_MACHINE_TOOL",
    "HARD_MFTD",
    "TYPES_OF_AUTOMATION",
    "TYPES_OF_SPECIALIZATION",
    "TYPES_PROCESSING",
    # Методы пакета
    # Классы пакета
    "MachineToolsContainer",
    "MachineToolsFinder",
    "MachineToolsCreator",
    "MachineToolsLister",
    "MachineTool",
    ]


# if __name__ == "__main__":
#     pass
