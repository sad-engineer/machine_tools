#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum


class Accuracy(Enum):
    """Перечисление возможных значений точности станка"""

    S = "С"
    S_A = "С/А"
    A = "А"
    V_A = "В/А"
    V = "В"
    P_V = "П/В"
    P = "П"
    N_P = "Н/П"
    N = "Н"
    NO_DATA = "Нет данных"
    TU_TB_16_0001 = "ТУ ТВ-16-0001"

    @classmethod
    def from_str(cls, value: str) -> 'Accuracy':
        """
        Преобразует строковое значение в элемент перечисления.

        Args:
            value (str): Строковое значение точности

        Returns:
            MachineAccuracy: Элемент перечисления

        Raises:
            ValueError: Если значение не соответствует ни одному из допустимых
        """
        value = value.strip()
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Недопустимое значение точности: {value}. Допустимые значения: {[m.value for m in cls]}")
