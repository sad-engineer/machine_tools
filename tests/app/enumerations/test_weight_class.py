#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest

from machine_tools.app.enumerations.weight_class import WeightClass


class TestWeightClass(unittest.TestCase):
    """Тесты для перечисления WeightClass"""

    def test_01_values(self):
        """Тест проверки значений перечисления"""
        # Проверяем все значения
        self.assertEqual(WeightClass.LIGHT.value, "Лёгкий")
        self.assertEqual(WeightClass.MEDIUM.value, "Средний")
        self.assertEqual(WeightClass.HEAVY.value, "Тяжёлый")
        self.assertEqual(WeightClass.UNIQUE.value, "Уникальный")

    def test_02_from_str_valid(self):
        """Тест преобразования корректных строковых значений"""
        # Проверяем преобразование для каждого значения
        self.assertEqual(WeightClass.from_str("Лёгкий"), WeightClass.LIGHT)
        self.assertEqual(WeightClass.from_str("Средний"), WeightClass.MEDIUM)
        self.assertEqual(WeightClass.from_str("Тяжёлый"), WeightClass.HEAVY)
        self.assertEqual(WeightClass.from_str("Уникальный"), WeightClass.UNIQUE)

        # Проверяем обработку пробелов
        self.assertEqual(WeightClass.from_str("  Лёгкий  "), WeightClass.LIGHT)
        self.assertEqual(WeightClass.from_str("  Средний  "), WeightClass.MEDIUM)

    def test_03_from_str_invalid(self):
        """Тест обработки некорректных строковых значений"""
        # Проверяем обработку некорректных значений
        with self.assertRaises(ValueError) as context:
            WeightClass.from_str("Некорректное значение")

        # Проверяем, что сообщение об ошибке содержит список допустимых значений
        error_message = str(context.exception)
        self.assertIn("Недопустимое значение класса массы", error_message)
        self.assertIn("Допустимые значения", error_message)
        for value in [m.value for m in WeightClass]:
            self.assertIn(value, error_message)

    def test_04_case_sensitivity(self):
        """Тест чувствительности к регистру"""
        # Проверяем, что значения чувствительны к регистру
        with self.assertRaises(ValueError):
            WeightClass.from_str("лёгкий")  # строчные буквы


if __name__ == "__main__":
    unittest.main()
