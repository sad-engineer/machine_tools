#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import itertools
from typing import Any, Callable

from service_for_my_projects import RecordRequester, logged
from service_for_my_projects import \
    output_debug_message_for_init_method as debug_message_for_init


def output_debug_message_with_kwargs_and_length(message: str):
    """Выводит в лог сообщение message"""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            len_result = 0 if isinstance(result, type(None)) else len(result)
            (
                self.debug(message)
                if message.find("{") == -1
                else self.debug(
                    message.format(
                        self.__class__.__name__,
                        "; ".join([f"{k}= {v}" for k, v in kwargs.items()]),
                        len_result,
                    )
                )
            )
            return result

        return wrapper

    return decorator


def output_debug_message_with_with_length(message: str):
    """Выводит в лог сообщение message"""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            gen1, gen2 = itertools.tee(func(self, *args, **kwargs))
            length = len(list(gen1))
            (
                self.debug(message)
                if message.find("{") == -1
                else self.debug(message.format(self.__class__.__name__, length))
            )
            return gen2

        return wrapper

    return decorator


@logged
class MachineToolsFinder:
    """Ищет записи в БД по конкретным параметрам."""

    @debug_message_for_init()
    def __init__(self, record_requester: Callable[..., RecordRequester]):
        self._requester = record_requester()

    @output_debug_message_with_kwargs_and_length("{0} по ключу {1} нашел записей: {2}")
    def by_name(self, any_name: str) -> Any:
        """Возвращает найденные записи по наименованию станка. Формат возвращаемых данных определяет self._requester

        Parameters:
        any_name : str : Наименование материала
        """
        records = self._requester.get_records({"Станок": any_name})
        return records if records else None

    @output_debug_message_with_kwargs_and_length("{0} по ключу {1} нашел записей: {2}")
    def by_type(self, machine_type) -> Any:
        records = self._requester.get_records({"Тип": machine_type})
        return records if records else None

    @output_debug_message_with_kwargs_and_length("{0} по ключу {1} нашел записей: {2}")
    def by_group(self, machine_group) -> Any:
        records = self._requester.get_records({"Группа": machine_group})
        return records if records else None

    @output_debug_message_with_kwargs_and_length("{0} по ключу {1} нашел записей: {2}")
    def by_type_and_group(self, machine_type, machine_group) -> Any:
        records = self._requester.get_records(
            {"Группа": machine_group, "Тип": machine_type}
        )
        return records if records else None

    @property
    @output_debug_message_with_with_length(
        "{0} ищет все записи таблицы. Найдено записей: {1}"
    )
    def all(self) -> Any:
        """Возвращает все записи. Формат возвращаемых данных определяет self._requester."""
        for record in self._requester.get_all_records:
            yield record

    @property
    def available_values(self) -> Any:
        """Возвращает наборы доступных в таблице БД значений по категориям."""
        return self._requester.available_values
