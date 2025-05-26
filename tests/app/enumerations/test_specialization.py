#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest

from machine_tools.app.enumerations.specialization import Specialization


class TestSpecialization(unittest.TestCase):
    """Тесты для перечисления Specialization"""

    def test_01_values(self):
        """Тест проверки значений перечисления"""
        # Проверяем все значения
        self.assertEqual(Specialization.SPECIALIZED.value, "Специализированный")
        self.assertEqual(Specialization.SPECIAL.value, "Специальный")
        self.assertEqual(Specialization.UNIVERSAL.value, "Универсальный")

    def test_02_from_str_valid(self):
        """Тест преобразования корректных строковых значений"""
        # Проверяем преобразование для каждого значения
        self.assertEqual(Specialization.from_str("Специализированный"), Specialization.SPECIALIZED)
        self.assertEqual(Specialization.from_str("Специальный"), Specialization.SPECIAL)
        self.assertEqual(Specialization.from_str("Универсальный"), Specialization.UNIVERSAL)

        # Проверяем обработку пробелов
        self.assertEqual(Specialization.from_str("  Специализированный  "), Specialization.SPECIALIZED)
        self.assertEqual(Specialization.from_str("  Специальный  "), Specialization.SPECIAL)

    def test_03_from_str_invalid(self):
        """Тест обработки некорректных строковых значений"""
        # Проверяем обработку некорректных значений
        with self.assertRaises(ValueError) as context:
            Specialization.from_str("Некорректное значение")

        # Проверяем, что сообщение об ошибке содержит список допустимых значений
        error_message = str(context.exception)
        self.assertIn("Недопустимое значение специализации", error_message)
        self.assertIn("Допустимые значения", error_message)
        for value in [m.value for m in Specialization]:
            self.assertIn(value, error_message)

    def test_04_case_sensitivity(self):
        """Тест чувствительности к регистру"""
        # Проверяем, что значения чувствительны к регистру
        with self.assertRaises(ValueError):
            Specialization.from_str("специализированный")  # строчные буквы


if __name__ == "__main__":
    unittest.main()
