#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum


class MachineWeightClass(Enum):
    """Перечисление возможных значений класса массы станка"""
    LIGHT = "Лёгкий"
    MEDIUM = "Средний"
    HEAVY = "Тяжёлый"
    UNIQUE = "Уникальный"

    @classmethod
    def from_str(cls, value: str) -> 'MachineWeightClass':
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
        raise ValueError(f"Недопустимое значение класса массы: {value}. "
                        f"Допустимые значения: {[m.value for m in cls]}")


class MachineWeightClassField:
    """Дескриптор для поля класса массы станка"""

    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._value is None:
            return None
        if isinstance(self._value, MachineWeightClass):
            return self._value.value
        return self._value

    def __set__(self, instance, value):
        if value is None:
            self._value = None
            return

        if isinstance(value, MachineWeightClass):
            self._value = value
        else:
            try:
                self._value = MachineWeightClass.from_str(str(value))
            except ValueError as e:
                raise ValueError(str(e)) from e

    @property
    def str(self):
        """Возвращает строковое значение класса массы станка"""
        if self._value is None:
            return ""
        return self._value.value


if __name__ == "__main__":
    class Machine:
        weight_class: MachineWeightClassField = MachineWeightClassField()

        def __init__(self):
            self.weight_class = None

    machine = Machine()

    # Можно присваивать строки
    machine.weight_class = "Лёгкий"        # OK
    print(machine.weight_class)       # "Лёгкий"
    
    machine.weight_class = "Средний"       # OK
    print(machine.weight_class)       # "Средний"
    
    machine.weight_class = "Тяжёлый"       # OK
    print(machine.weight_class)       # "Тяжёлый"

    machine.weight_class = "Уникальный"     # OK
    print(machine.weight_class)       # "Уникальный"

    try:
        machine.weight_class = "X"      # ValueError: Недопустимое значение класса массы: X
    except ValueError as e:
        print(f"Ошибка: {e}") 