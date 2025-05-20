#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum


class MachineAccuracy(Enum):
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
    def from_str(cls, value: str) -> 'MachineAccuracy':
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
        raise ValueError(f"Недопустимое значение точности: {value}. "
                         f"Допустимые значения: {[m.value for m in cls]}")


class MachineAccuracyField:
    """Дескриптор для поля точности станка"""

    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._value is None:
            return MachineAccuracy.NO_DATA.value
        if isinstance(self._value, MachineAccuracy):
            return self._value.value
        return self._value

    def __set__(self, instance, value):
        if value is None:
            self._value = MachineAccuracy.NO_DATA
            return

        if isinstance(value, MachineAccuracy):
            self._value = value
        else:
            try:
                self._value = MachineAccuracy.from_str(str(value))
            except ValueError as e:
                raise ValueError(str(e)) from e

    @property
    def str(self):
        """Возвращает строковое значение точности станка"""
        if self._value is None:
            return MachineAccuracy.NO_DATA.value
        return self._value.value


if __name__ == "__main__":
    class Machine:
        accuracy: MachineAccuracyField = MachineAccuracyField()

        def __init__(self):
            self.accuracy = None

    machine = Machine()

    # Можно присваивать строки
    machine.accuracy = "Н"        # OK
    print(machine.accuracy)       # Н

    machine.accuracy = "В/А"      # OK
    print(machine.accuracy)       # В/А

    machine.accuracy = "П/В"      # OK
    print(machine.accuracy)       # П/В

    # Можно присваивать 'Нет данных'
    machine.accuracy = 'Нет данных'    # OK
    print(machine.accuracy)       # "Нет данных"

    try:
        machine.accuracy = "X"      # ValueError: Недопустимое значение точности: X
    except ValueError as e:
        print(f"Ошибка: {e}")
