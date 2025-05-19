#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
class MachineGroupField:
    """Дескриптор для поля группы станков"""

    def __init__(self):
        self._value = None
        self._descriptions = {
            1: "Токарные станки",
            2: "Сверлильные и расточные станки",
            3: "Шлифовальные, полировальные, доводочные станки",
            4: "Комбинированные",
            5: "Зубообрабатывающие и резьбообрабатывающие станки",
            6: "Фрезерные станки",
            7: "Строгальные, долбежные и протяжные станки",
            8: "Разрезные станки",
            9: "Разные станки"
        }

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._value is None:
            return None
        return {self._value: self._descriptions[self._value]}

    def __set__(self, instance, value):
        if value is None:
            self._value = None
            return

        try:
            value = int(value)
            if value not in self._descriptions:
                raise ValueError(f"Недопустимое значение для группы станков: {value}")
            self._value = value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Недопустимое значение для группы станков: {value}") from e

    @property
    def str(self):
        """Возвращает описание группы станков"""
        if self._value is None:
            return ""
        return self._descriptions.get(self._value, "")


if __name__ == "__main__":
    class Machine:
        group = MachineGroupField()

        def __init__(self):
            self.group = None


    machine = Machine()

    # Можно присваивать числа
    machine.group = 1  # OK
    print(machine.group)  # {1: "Токарные станки"}

    machine.group = 2  # OK
    print(machine.group)  # {2: "Сверлильные и расточные станки"}

    # machine.group = 12  # ValueError: Недопустимое значение для группы станков: 12