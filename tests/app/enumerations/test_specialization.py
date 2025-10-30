#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest

from machine_tools.app.enumerations.specialization import Specialization


class TestSpecialization(unittest.TestCase):
    """Тесты для перечисления Specialization"""

    def test_01_values(self):
        """Тест проверки значений перечисления"""

        self.assertEqual(Specialization.SPECIALIZED.value, "Специализированный")
        self.assertEqual(Specialization.SPECIAL.value, "Специальный")
        self.assertEqual(Specialization.UNIVERSAL.value, "Универсальный")

    def test_02_from_str_valid(self):
        """Тест преобразования корректных строковых значений"""

        self.assertEqual(Specialization.from_str("Специализированный"), Specialization.SPECIALIZED)
        self.assertEqual(Specialization.from_str("Специальный"), Specialization.SPECIAL)
        self.assertEqual(Specialization.from_str("Универсальный"), Specialization.UNIVERSAL)

        self.assertEqual(Specialization.from_str("  Специализированный  "), Specialization.SPECIALIZED)
        self.assertEqual(Specialization.from_str("  Специальный  "), Specialization.SPECIAL)

    def test_03_from_str_invalid(self):
        """Тест обработки некорректных строковых значений"""

        with self.assertRaises(ValueError) as context:
            Specialization.from_str("Некорректное значение")

        error_message = str(context.exception)
        self.assertIn("Недопустимое значение специализации", error_message)
        self.assertIn("Допустимые значения", error_message)
        for value in [m.value for m in Specialization]:
            self.assertIn(value, error_message)

    def test_04_case_sensitivity(self):
        """Тест чувствительности к регистру"""

        with self.assertRaises(ValueError):
            Specialization.from_str("специализированный")  # строчные буквы


if __name__ == "__main__":
    unittest.main()
