#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools.app.descriptions import ACCURACY_DESCRIPTIONS, GROUP_DESCRIPTIONS, TYPE_DESCRIPTIONS
from machine_tools.app.enumerations import Accuracy, Automation, SoftwareControl, Specialization, WeightClass
from machine_tools.app.fields import AccuracyField, AutomationField, SpecializationField, WeightClassField
from machine_tools.app.finders import MachineFinder as Finder
from machine_tools.app.formatters import (
    DictMachineInfoFormatter,
    DictNameFormatter,
    IndexedMachineInfoFormatter,
    IndexedNameFormatter,
    ListMachineInfoFormatter,
    ListNameFormatter,
    MachineFormatter,
)
from machine_tools.app.models import Machine, TechnicalRequirement
from machine_tools.app.schemas import Dimensions, Location, MachineInfo
from machine_tools.app.services import FinderContainer as Container
from machine_tools.app.services import (
    find_names,
    get_finder_with_dict_info,
    get_finder_with_dict_names,
    get_finder_with_indexed_info,
    get_finder_with_indexed_names,
    get_finder_with_list_info,
    get_finder_with_list_names,
)
from machine_tools.app.services import get_machine_info_by_name as info_by_name
from machine_tools.app.services import (
    update,
)
from machine_tools.version import __version__

__all__ = [
    # описания полей
    "ACCURACY_DESCRIPTIONS",
    "GROUP_DESCRIPTIONS",
    "TYPE_DESCRIPTIONS",
    # перечисления
    "Accuracy",
    "Automation",
    "Specialization",
    "WeightClass",
    "SoftwareControl",
    # поля
    "AccuracyField",
    "AutomationField",
    "SpecializationField",
    "WeightClassField",
    # поисковики
    "Finder",
    # форматировщики
    "DictMachineInfoFormatter",
    "DictNameFormatter",
    "IndexedMachineInfoFormatter",
    "IndexedNameFormatter",
    "ListMachineInfoFormatter",
    "ListNameFormatter",
    "MachineFormatter",
    # модели
    "Machine",
    "TechnicalRequirement",
    # схемы
    "Dimensions",
    "Location",
    "MachineInfo",
    # контейнеры
    "Container",
    # функции
    "find_names",
    "get_finder_with_list_names",
    "get_finder_with_list_info",
    "get_finder_with_dict_names",
    "get_finder_with_dict_info",
    "get_finder_with_indexed_names",
    "get_finder_with_indexed_info",
    "update",
    "info_by_name",
    "__version__",
]
