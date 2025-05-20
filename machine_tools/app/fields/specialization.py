#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum


class MachineSpecialization(Enum):
    """Перечисление возможных значений специализации станка"""
    SPECIALIZED = "Специализированный"
    SPECIAL = "Специальный"
    UNIVERSAL = "Универсальный"

    @classmethod
    def from_str(cls, value: str) -> 'MachineSpecialization':
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
        raise ValueError(f"Недопустимое значение специализации: {value}. "
                        f"Допустимые значения: {[m.value for m in cls]}")


class MachineSpecializationField:
    """Дескриптор для поля специализации станка"""

    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._value is None:
            return None
        if isinstance(self._value, MachineSpecialization):
            return self._value.value
        return self._value

    def __set__(self, instance, value):
        if value is None:
            self._value = None
            return

        if isinstance(value, MachineSpecialization):
            self._value = value
        else:
            try:
                self._value = MachineSpecialization.from_str(str(value))
            except ValueError as e:
                raise ValueError(str(e)) from e

    @property
    def str(self):
        """Возвращает строковое значение специализации станка"""
        if self._value is None:
            return ""
        return self._value.value


if __name__ == "__main__":
    class Machine:
        specialization: MachineSpecializationField = MachineSpecializationField()

        def __init__(self):
            self.specialization = None

    machine = Machine()

    # Можно присваивать строки
    machine.specialization = "Специализированный"    # OK
    print(machine.specialization)       # "Специализированный"
    
    machine.specialization = "Специальный"          # OK
    print(machine.specialization)       # "Специальный"
    
    machine.specialization = "Универсальный"        # OK
    print(machine.specialization)       # "Универсальный"

    try:
        machine.specialization = "X"      # ValueError: Недопустимое значение специализации: X
    except ValueError as e:
        print(f"Ошибка: {e}") 