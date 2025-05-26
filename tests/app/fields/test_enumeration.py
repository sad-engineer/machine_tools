#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest

from machine_tools.app.enumerations import Accuracy, Automation, Specialization, WeightClass
from machine_tools.app.fields.enumeration import (
    AccuracyField,
    AutomationField,
    EnumerationField,
    SpecializationField,
    WeightClassField,
)


class TestEnumerationField(unittest.TestCase):
    """Тесты для базового класса EnumerationField"""

    def test_01_abstract_methods(self):
        """Тест абстрактных методов"""
        # Проверяем, что нельзя создать экземпляр абстрактного класса
        with self.assertRaises(TypeError):
            EnumerationField()


class TestAccuracyField(unittest.TestCase):
    """Тесты для дескриптора AccuracyField"""

    def setUp(self):
        """Подготовка тестового окружения"""

        class TestClass:
            accuracy = AccuracyField()

        self.test_instance = TestClass()

    def test_01_default_value(self):
        """Тест значения по умолчанию"""
        self.assertEqual(self.test_instance.accuracy, Accuracy.NO_DATA.value)

    def test_02_set_valid_value(self):
        """Тест установки корректного значения"""
        # Устанавливаем строковое значение
        self.test_instance.accuracy = "Н"
        self.assertEqual(self.test_instance.accuracy, "Н")

        # Устанавливаем значение перечисления
        self.test_instance.accuracy = Accuracy.P
        self.assertEqual(self.test_instance.accuracy, Accuracy.P.value)

    def test_03_set_invalid_value(self):
        """Тест установки некорректного значения"""
        with self.assertRaises(ValueError) as context:
            self.test_instance.accuracy = "Некорректное значение"

        error_message = str(context.exception)
        self.assertIn("Недопустимое значение точности", error_message)

    def test_04_set_none(self):
        """Тест установки None"""
        self.test_instance.accuracy = None
        self.assertEqual(self.test_instance.accuracy, Accuracy.NO_DATA.value)


class TestAutomationField(unittest.TestCase):
    """Тесты для дескриптора AutomationField"""

    def setUp(self):
        """Подготовка тестового окружения"""

        class TestClass:
            automation = AutomationField()

        self.test_instance = TestClass()

    def test_01_default_value(self):
        """Тест значения по умолчанию"""
        self.assertIsNone(self.test_instance.automation)

    def test_02_set_valid_value(self):
        """Тест установки корректного значения"""
        # Устанавливаем строковое значение
        self.test_instance.automation = "Автомат"
        self.assertEqual(self.test_instance.automation, "Автомат")

        # Устанавливаем значение перечисления
        self.test_instance.automation = Automation.AUTOMATIC
        self.assertEqual(self.test_instance.automation, Automation.AUTOMATIC.value)

    def test_03_set_invalid_value(self):
        """Тест установки некорректного значения"""
        with self.assertRaises(ValueError) as context:
            self.test_instance.automation = "Некорректное значение"

        error_message = str(context.exception)
        self.assertIn("Недопустимое значение автоматизации", error_message)

    def test_04_set_none(self):
        """Тест установки None"""
        self.test_instance.automation = None
        self.assertIsNone(self.test_instance.automation)


class TestSpecializationField(unittest.TestCase):
    """Тесты для дескриптора SpecializationField"""

    def setUp(self):
        """Подготовка тестового окружения"""

        class TestClass:
            specialization = SpecializationField()

        self.test_instance = TestClass()

    def test_01_default_value(self):
        """Тест значения по умолчанию"""
        self.assertIsNone(self.test_instance.specialization)

    def test_02_set_valid_value(self):
        """Тест установки корректного значения"""
        # Устанавливаем строковое значение
        self.test_instance.specialization = "Специализированный"
        self.assertEqual(self.test_instance.specialization, "Специализированный")

        # Устанавливаем значение перечисления
        self.test_instance.specialization = Specialization.SPECIALIZED
        self.assertEqual(self.test_instance.specialization, Specialization.SPECIALIZED.value)

    def test_03_set_invalid_value(self):
        """Тест установки некорректного значения"""
        with self.assertRaises(ValueError) as context:
            self.test_instance.specialization = "Некорректное значение"

        error_message = str(context.exception)
        self.assertIn("Недопустимое значение специализации", error_message)

    def test_04_set_none(self):
        """Тест установки None"""
        self.test_instance.specialization = None
        self.assertIsNone(self.test_instance.specialization)


class TestWeightClassField(unittest.TestCase):
    """Тесты для дескриптора WeightClassField"""

    def setUp(self):
        """Подготовка тестового окружения"""

        class TestClass:
            weight_class = WeightClassField()

        self.test_instance = TestClass()

    def test_01_default_value(self):
        """Тест значения по умолчанию"""
        self.assertIsNone(self.test_instance.weight_class)

    def test_02_set_valid_value(self):
        """Тест установки корректного значения"""
        # Устанавливаем строковое значение
        self.test_instance.weight_class = "Лёгкий"
        self.assertEqual(self.test_instance.weight_class, "Лёгкий")

        # Устанавливаем значение перечисления
        self.test_instance.weight_class = WeightClass.LIGHT
        self.assertEqual(self.test_instance.weight_class, WeightClass.LIGHT.value)

    def test_03_set_invalid_value(self):
        """Тест установки некорректного значения"""
        with self.assertRaises(ValueError) as context:
            self.test_instance.weight_class = "Некорректное значение"

        error_message = str(context.exception)
        self.assertIn("Недопустимое значение класса массы", error_message)

    def test_04_set_none(self):
        """Тест установки None"""
        self.test_instance.weight_class = None
        self.assertIsNone(self.test_instance.weight_class)


if __name__ == "__main__":
    unittest.main()
