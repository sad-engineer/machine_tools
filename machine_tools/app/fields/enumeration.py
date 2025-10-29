#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Type, TypeVar

from machine_tools.app.enumerations import (
    Accuracy,
    Automation,
    Specialization,
    WeightClass,
)

T = TypeVar('T', bound=Enum)


class EnumerationField(ABC):
    """Базовый дескриптор для полей из перечисления"""

    def __init__(self):
        self._value = None

    @property
    @abstractmethod
    def enum_class(self) -> Type[T]:
        """Возвращает класс перечисления"""
        pass

    @property
    @abstractmethod
    def default_value(self) -> Optional[str]:
        """Возвращает значение по умолчанию"""
        pass

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._value is None:
            return self.default_value
        if isinstance(self._value, self.enum_class):
            return self._value.value
        return self._value

    def __set__(self, instance, value):
        if value is None:
            self._value = None
            return

        if isinstance(value, self.enum_class):
            self._value = value
        else:
            try:
                self._value = self.enum_class.from_str(str(value))
            except ValueError as e:
                raise ValueError(str(e)) from e

    @property
    def str(self):
        """Возвращает строковое значение"""
        if self._value is None:
            return self.default_value
        return self._value.value


class AccuracyField(EnumerationField):
    """Дескриптор для поля точности станка"""

    @property
    def enum_class(self) -> Type[Accuracy]:
        return Accuracy

    @property
    def default_value(self) -> str:
        return Accuracy.NO_DATA.value


class AutomationField(EnumerationField):
    """Дескриптор для поля автоматизации станка"""

    @property
    def enum_class(self) -> Type[Automation]:
        return Automation

    @property
    def default_value(self) -> Optional[str]:
        return None


class SpecializationField(EnumerationField):
    """Дескриптор для поля специализации станка"""

    @property
    def enum_class(self) -> Type[Specialization]:
        return Specialization

    @property
    def default_value(self) -> Optional[str]:
        return None


class WeightClassField(EnumerationField):
    """Дескриптор для поля класса массы станка"""

    @property
    def enum_class(self) -> Type[WeightClass]:
        return WeightClass

    @property
    def default_value(self) -> Optional[str]:
        return None


if __name__ == "__main__":

    class Machine:
        accuracy: Optional[AccuracyField] = AccuracyField()
        automation: Optional[AutomationField] = AutomationField()
        specialization: Optional[SpecializationField] = SpecializationField()
        weight_class: Optional[WeightClassField] = WeightClassField()

        def __init__(self):
            self.accuracy = None
            self.automation = None
            self.specialization = None
            self.weight_class = None

    machine = Machine()

    machine.accuracy = "Н"
    print(machine.accuracy)  # Н

    machine.accuracy = "В/А"
    print(machine.accuracy)  # В/А

    machine.accuracy = "П/В"
    print(machine.accuracy)  # П/В

    machine.accuracy = 'Нет данных'
    print(machine.accuracy)  # "Нет данных"

    machine.automation = "Автомат"
    print(machine.automation)  # "Автомат"

    machine.automation = "Полуавтомат"
    print(machine.automation)  # "Полуавтомат"

    machine.automation = "Ручной"
    print(machine.automation)  # "Ручной"

    machine.specialization = "Специализированный"
    print(machine.specialization)  # "Специализированный"

    machine.specialization = "Специальный"
    print(machine.specialization)  # "Специальный"

    machine.specialization = "Универсальный"
    print(machine.specialization)  # "Универсальный"

    machine.weight_class = "Лёгкий"
    print(machine.weight_class)  # "Лёгкий"

    machine.weight_class = "Средний"
    print(machine.weight_class)  # "Средний"

    machine.weight_class = "Тяжёлый"
    print(machine.weight_class)  # "Тяжёлый"

    machine.weight_class = "Уникальный"
    print(machine.weight_class)  # "Уникальный"

    try:
        machine.accuracy = "X"  # ValueError: Недопустимое значение точности: X
    except ValueError as e:
        print(f"Ошибка accuracy: {e}")

    try:
        machine.automation = "X"  # ValueError: Недопустимое значение автоматизации: X
    except ValueError as e:
        print(f"Ошибка automation: {e}")

    try:
        machine.specialization = "X"  # ValueError: Недопустимое значение специализации: X
    except ValueError as e:
        print(f"Ошибка specialization: {e}")

    try:
        machine.weight_class = "X"  # ValueError: Недопустимое значение класса массы: X
    except ValueError as e:
        print(f"Ошибка weight_class: {e}")
