#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools.app.enumerations.base import BaseEnum


class Automation(BaseEnum):
    """Перечисление возможных значений автоматизации станка"""

    AUTOMATIC = "Автомат"
    SEMI_AUTOMATIC = "Полуавтомат"
    MANUAL = "Ручной"

    @classmethod
    def from_str(cls, value: str) -> 'Automation':
        """
        Преобразует строковое значение в элемент перечисления.

        Args:
            value (str): Строковое значение автоматизации

        Returns:
            MachineAutomation: Элемент перечисления

        Raises:
            ValueError: Если значение не соответствует ни одному из допустимых
        """
        value = value.strip()
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Недопустимое значение автоматизации: {value}. Допустимые значения: {[m.value for m in cls]}")
