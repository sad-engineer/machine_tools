#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum
from typing import TypeVar, Generic, Type, Any

T = TypeVar('T')


class BaseEnum(Enum):
    """Базовый класс для перечислений с общими методами"""

    @classmethod
    def get_values(cls) -> list[str]:
        """
        Получить список всех значений перечисления.

        Returns:
            list[str]: Список значений
        """
        return [member.value for member in cls]

    @classmethod
    def get_names(cls) -> list[str]:
        """
        Получить список всех имен перечисления.

        Returns:
            list[str]: Список имен
        """
        return [member.name for member in cls]

    @classmethod
    def get_items(cls) -> list[tuple[str, str]]:
        """
        Получить список кортежей (имя, значение).

        Returns:
            list[tuple[str, str]]: Список кортежей
        """
        return [(member.name, member.value) for member in cls]

    @classmethod
    def get_dict(cls) -> dict[str, str]:
        """
        Получить словарь {имя: значение}.

        Returns:
            dict[str, str]: Словарь имен и значений
        """
        return {member.name: member.value for member in cls}

    @classmethod
    def from_str(cls, value: str) -> 'BaseEnum':
        """
        Преобразует строковое значение в элемент перечисления.

        Args:
            value (str): Строковое значение

        Returns:
            BaseEnum: Элемент перечисления

        Raises:
            ValueError: Если значение не соответствует ни одному из допустимых
        """
        value = value.strip()
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Недопустимое значение: {value}. Допустимые значения: {cls.get_values()}") 