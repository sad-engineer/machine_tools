#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest

from machine_tools.app.enumerations.automation import Automation


class TestAutomation(unittest.TestCase):
    """Тесты для перечисления Automation"""

    def test_01_values(self):
        """Тест проверки значений перечисления"""

        self.assertEqual(Automation.AUTOMATIC.value, "Автомат")
        self.assertEqual(Automation.SEMI_AUTOMATIC.value, "Полуавтомат")
        self.assertEqual(Automation.MANUAL.value, "Ручной")

    def test_02_from_str_valid(self):
        """Тест преобразования корректных строковых значений"""

        self.assertEqual(Automation.from_str("Автомат"), Automation.AUTOMATIC)
        self.assertEqual(Automation.from_str("Полуавтомат"), Automation.SEMI_AUTOMATIC)
        self.assertEqual(Automation.from_str("Ручной"), Automation.MANUAL)

        self.assertEqual(Automation.from_str("  Автомат  "), Automation.AUTOMATIC)
        self.assertEqual(Automation.from_str("  Полуавтомат  "), Automation.SEMI_AUTOMATIC)

    def test_03_from_str_invalid(self):
        """Тест обработки некорректных строковых значений"""

        with self.assertRaises(ValueError) as context:
            Automation.from_str("Некорректное значение")

        error_message = str(context.exception)
        self.assertIn("Недопустимое значение автоматизации", error_message)
        self.assertIn("Допустимые значения", error_message)
        for value in [m.value for m in Automation]:
            self.assertIn(value, error_message)

    def test_04_case_sensitivity(self):
        """Тест чувствительности к регистру"""

        with self.assertRaises(ValueError):
            Automation.from_str("автомат")  # строчные буквы


if __name__ == "__main__":
    unittest.main()
