#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools.app.enumerations.base import BaseEnum


class WeightClass(BaseEnum):
    """Перечисление возможных значений класса массы станка"""

    LIGHT = "Лёгкий"
    MEDIUM = "Средний"
    HEAVY = "Тяжёлый"
    UNIQUE = "Уникальный"

    @classmethod
    def from_str(cls, value: str) -> 'WeightClass':
        """
        Преобразует строковое значение в элемент перечисления.

        Args:
            value (str): Строковое значение класса массы

        Returns:
            MachineWeightClass: Элемент перечисления

        Raises:
            ValueError: Если значение не соответствует ни одному из допустимых
        """
        value = value.strip()
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Недопустимое значение класса массы: {value}. Допустимые значения: {[m.value for m in cls]}")
