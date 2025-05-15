#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Protocol

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.schemas.machine import MachineInfo


class MachineFormatter(Protocol):
    """Протокол для форматтеров станков"""

    def format(self, machines: List[Machine]) -> List[Any]:
        """Форматирует список станков"""
        ...


class ListNameFormatter(MachineFormatter):
    """Форматтер, возвращающий список имен станков"""

    def format(self, machines: List[Machine]) -> List[str]:
        return [machine.name for machine in machines]


class ListMachineInfoFormatter(MachineFormatter):
    """Форматтер, возвращающий список MachineInfo"""

    def format(self, machines: List[Machine]) -> List[MachineInfo]:
        return [MachineInfo.model_validate(machine.__dict__) for machine in machines]


class DictNameFormatter(MachineFormatter):
    """Форматтер, возвращающий словарь {id: name}"""

    def format(self, machines: List[Machine]) -> Dict[int, str]:
        return {machine.id: machine.name for machine in machines}


class DictMachineInfoFormatter(MachineFormatter):
    """Форматтер, возвращающий словарь {id: MachineInfo}"""

    def format(self, machines: List[Machine]) -> Dict[int, MachineInfo]:
        return {machine.id: MachineInfo.model_validate(machine.__dict__) for machine in machines}


class IndexedNameFormatter(MachineFormatter):
    """Форматтер, возвращающий словарь {номер: name}"""

    def format(self, machines: List[Machine]) -> Dict[int, str]:
        return {i + 1: machine.name for i, machine in enumerate(machines)}


class IndexedMachineInfoFormatter(MachineFormatter):
    """Форматтер, возвращающий словарь {номер: MachineInfo}"""

    def format(self, machines: List[Machine]) -> Dict[int, MachineInfo]:
        return {i + 1: MachineInfo.model_validate(machine.__dict__) for i, machine in enumerate(machines)}
