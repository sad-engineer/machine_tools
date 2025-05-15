#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable

from pydantic import confloat
from service_for_my_projects import logged
from service_for_my_projects import output_debug_message_for_init_method as debug_message_for_init

from machine_tools.obj.creators import MachineToolsCreator
from machine_tools.obj.finders import MachineToolsFinder


def output_debug_message(message: str):
    """Выводит в лог сообщение message"""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            (
                self.debug(message)
                if message.find("{") == -1
                else self.debug(message.format("; ".join([f"{k}= {v}" for k, v in kwargs.items()])))
            )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


@logged
class MachineToolsLister:
    @debug_message_for_init()
    def __init__(
        self,
        creator_provider: Callable[..., MachineToolsCreator],
        finder_provider: Callable[..., MachineToolsFinder],
    ):
        self._creator = creator_provider()
        self._finder = finder_provider()

    @output_debug_message("Создание списка доступных станков по классу {}")
    def by_type(self, machine_type: confloat(ge=0, le=9)) -> list:
        self._finder._verbose = True
        return [self._creator.by_name(row["Станок"]) for row in self._finder.by_type(machine_type=machine_type)]

    @output_debug_message("Создание списка доступных станков по группе {}")
    def by_group(self, group: confloat(ge=0, le=9)) -> list:
        self._finder._verbose = True
        return [self._creator.by_name(row["Станок"]) for row in self._finder.by_group(group=group)]

    @output_debug_message("Создание списка доступных станков по классу {}")
    def by_type_and_group(self, machine_type: confloat(ge=0, le=9), group: confloat(ge=0, le=9)) -> list:
        self._finder._verbose = True
        return [
            self._creator.by_name(row["Станок"])
            for row in self._finder.by_type_and_group(machine_type=machine_type, machine_group=group)
        ]

    @property
    @output_debug_message("Создание списка всех доступных материалов")
    def all(self) -> list:
        self._finder._verbose = False
        return [self._creator.by_name(row["Станок"]) for row in self._finder.all]
