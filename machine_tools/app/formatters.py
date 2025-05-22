#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Protocol, Union

from machine_tools.app.models.machine import Machine
from machine_tools.app.schemas.machine import MachineInfo


def _machine_to_dict(machine: Machine) -> dict:
    """
    Преобразует объект Machine в словарь для MachineInfo.

    Args:
        machine (Machine): Объект станка.

    Returns:
        dict: Словарь с данными станка.
    """
    return {
        "name": machine.name,
        "group": machine.group,
        "type": machine.type,
        "power": machine.power,
        "efficiency": machine.efficiency,
        "accuracy": machine.accuracy,
        "automation": machine.automation,
        "specialization": machine.specialization,
        "weight": machine.weight,
        "weight_class": machine.weight_class,
        "machine_type": machine.machine_type,
        # Создаем вложенные модели
        "dimensions": (
            {
                "length": machine.length,
                "width": machine.width,
                "height": machine.height,
                "overall_diameter": machine.overall_diameter,
            }
            if machine.length or machine.width or machine.height or machine.overall_diameter
            else None
        ),
        "location": (
            {"city": machine.city, "manufacturer": machine.manufacturer}
            if machine.city or machine.manufacturer
            else None
        ),
        # Преобразуем список TechnicalRequirement в словарь
        "technical_requirements": (
            {req.requirement: req.value for req in machine.technical_requirements}
            if machine.technical_requirements
            else None
        ),
    }


class MachineFormatter(Protocol):
    """Протокол для форматтеров станков"""

    def format(self, machines: List[Machine]):
        """Форматирует список станков"""
        ...


class ListNameFormatter(MachineFormatter):
    """Форматтер, возвращающий список имен станков"""

    def format(self, machines: List[Machine]) -> List[str]:
        return [machine.name for machine in machines]


class ListMachineInfoFormatter(MachineFormatter):
    """Форматтер, возвращающий список MachineInfo"""

    def format(self, machines: List[Machine]) -> List[MachineInfo]:
        result = []
        for machine in machines:
            data = _machine_to_dict(machine)
            result.append(MachineInfo.model_validate(data))
        return result


class DictNameFormatter(MachineFormatter):
    """Форматтер, возвращающий словарь {id: name}"""

    def format(self, machines: List[Machine]) -> Dict[int, str]:
        return {machine.id: machine.name for machine in machines}


class DictMachineInfoFormatter(MachineFormatter):
    """Форматтер, возвращающий словарь {id: MachineInfo}"""

    def format(self, machines: List[Machine]) -> Dict[int, MachineInfo]:
        return {machine.name: MachineInfo.model_validate(_machine_to_dict(machine)) for machine in machines}


class IndexedNameFormatter(MachineFormatter):
    """Форматтер, возвращающий словарь {номер: name}"""

    def format(self, machines: List[Machine]) -> Dict[int, str]:
        return {i + 1: machine.name for i, machine in enumerate(machines)}


class IndexedMachineInfoFormatter(MachineFormatter):
    """Форматтер, возвращающий словарь {номер: MachineInfo}"""

    def format(self, machines: List[Machine]) -> Dict[int, MachineInfo]:
        return {i + 1: MachineInfo.model_validate(_machine_to_dict(machine)) for i, machine in enumerate(machines)}
