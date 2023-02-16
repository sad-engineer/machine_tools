#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Any

from service import RecordRequester


class Finder:
    """ Ищет записи в БД по конкретным параметрам."""
    def __init__(self, record_requester: RecordRequester):
        self._requester = record_requester

    def by_name(self, any_name: str) -> Any:
        """ Возвращает найденные записи по наименованию станка. Формат возвращаемых данных определяет self._requester

        Parameters:
        any_name : str : Наименование материала
        """
        records = self._requester.get_records({"Станок": any_name})
        return records if records else None

    def by_type(self, machine_type):
        records = self._requester.get_records({"Тип": machine_type})
        return records if records else None

    def by_group(self, machine_group):
        records = self._requester.get_records({"Группа": machine_group})
        return records if records else None

    def by_type_and_group(self, machine_type, machine_group):
        records = self._requester.get_records({"Группа": machine_group, "Тип": machine_type})
        return records if records else None

    @property
    def all(self) -> Any:
        """ Возвращает все записи. Формат возвращаемых данных определяет self._requester."""
        for index, record in self._requester.get_all_records.items():
            yield record

    @property
    def available_values(self) -> Any:
        """ Возвращает наборы доступных в таблице БД значений по категориям."""
        return self._requester.available_values
