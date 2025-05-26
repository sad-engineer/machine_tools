#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools.app.enumerations.base import BaseEnum


class SoftwareControl(BaseEnum):
    """Тип программного управления"""

    NO = "Нет"
    IC = "УЦИ"
    CNC = "ЧПУ"

    @classmethod
    def from_str(cls, value: str) -> 'SoftwareControl':
        """
        Преобразует строковое значение в элемент перечисления.

        Args:
            value (str): Строковое значение программного управления

        Returns:
            SoftwareControl: Элемент перечисления

        Raises:
            ValueError: Если значение не соответствует ни одному из допустимых
        """
        value = value.strip()
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(
            f"Недопустимое значение программного управления: {value}. Допустимые значения: {[m.value for m in cls]}"
        )
