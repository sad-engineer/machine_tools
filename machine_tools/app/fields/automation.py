#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum


class MachineAutomation(Enum):
    """Перечисление возможных значений автоматизации станка"""
    AUTOMATIC = "Автомат"
    SEMI_AUTOMATIC = "Полуавтомат"
    MANUAL = "Ручной"

    @classmethod
    def from_str(cls, value: str) -> 'MachineAutomation':
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
        raise ValueError(f"Недопустимое значение автоматизации: {value}. "
                         f"Допустимые значения: {[m.value for m in cls]}")


class MachineAutomationField:
    """Дескриптор для поля автоматизации станка"""

    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._value is None:
            return None
        if isinstance(self._value, MachineAutomation):
            return self._value.value
        return self._value

    def __set__(self, instance, value):
        if value is None:
            self._value = None
            return

        if isinstance(value, MachineAutomation):
            self._value = value
        else:
            try:
                self._value = MachineAutomation.from_str(str(value))
            except ValueError as e:
                raise ValueError(str(e)) from e

    @property
    def str(self):
        """Возвращает строковое значение автоматизации станка"""
        if self._value is None:
            return ""
        return self._value.value


if __name__ == "__main__":
    class Machine:
        automation: MachineAutomationField = MachineAutomationField()

        def __init__(self):
            self.automation = None

    machine = Machine()

    # Можно присваивать строки
    machine.automation = "Автомат"        # OK
    print(machine.automation)       # "Автомат"
    
    machine.automation = "Полуавтомат"    # OK
    print(machine.automation)       # "Полуавтомат"
    
    machine.automation = "Ручной"         # OK
    print(machine.automation)       # "Ручной"

    try:
        machine.automation = "X"      # ValueError: Недопустимое значение автоматизации: X
    except ValueError as e:
        print(f"Ошибка: {e}") 