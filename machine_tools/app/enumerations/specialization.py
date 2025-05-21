#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools.app.enumerations.base import BaseEnum


class Specialization(BaseEnum):
    """Перечисление возможных значений специализации станка"""

    SPECIALIZED = "Специализированный"
    SPECIAL = "Специальный"
    UNIVERSAL = "Универсальный"

    @classmethod
    def from_str(cls, value: str) -> 'Specialization':
        """
        Преобразует строковое значение в элемент перечисления.

        Args:
            value (str): Строковое значение специализации

        Returns:
            MachineSpecialization: Элемент перечисления

        Raises:
            ValueError: Если значение не соответствует ни одному из допустимых
        """
        value = value.strip()
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(
            f"Недопустимое значение специализации: {value}. " f"Допустимые значения: {[m.value for m in cls]}"
        )
