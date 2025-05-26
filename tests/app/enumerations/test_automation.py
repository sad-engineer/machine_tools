#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest

from machine_tools.app.enumerations.automation import Automation


class TestAutomation(unittest.TestCase):
    """Тесты для перечисления Automation"""

    def test_01_values(self):
        """Тест проверки значений перечисления"""
        # Проверяем все значения
        self.assertEqual(Automation.AUTOMATIC.value, "Автомат")
        self.assertEqual(Automation.SEMI_AUTOMATIC.value, "Полуавтомат")
        self.assertEqual(Automation.MANUAL.value, "Ручной")

    def test_02_from_str_valid(self):
        """Тест преобразования корректных строковых значений"""
        # Проверяем преобразование для каждого значения
        self.assertEqual(Automation.from_str("Автомат"), Automation.AUTOMATIC)
        self.assertEqual(Automation.from_str("Полуавтомат"), Automation.SEMI_AUTOMATIC)
        self.assertEqual(Automation.from_str("Ручной"), Automation.MANUAL)

        # Проверяем обработку пробелов
        self.assertEqual(Automation.from_str("  Автомат  "), Automation.AUTOMATIC)
        self.assertEqual(Automation.from_str("  Полуавтомат  "), Automation.SEMI_AUTOMATIC)

    def test_03_from_str_invalid(self):
        """Тест обработки некорректных строковых значений"""
        # Проверяем обработку некорректных значений
        with self.assertRaises(ValueError) as context:
            Automation.from_str("Некорректное значение")

        # Проверяем, что сообщение об ошибке содержит список допустимых значений
        error_message = str(context.exception)
        self.assertIn("Недопустимое значение автоматизации", error_message)
        self.assertIn("Допустимые значения", error_message)
        for value in [m.value for m in Automation]:
            self.assertIn(value, error_message)

    def test_04_case_sensitivity(self):
        """Тест чувствительности к регистру"""
        # Проверяем, что значения чувствительны к регистру
        with self.assertRaises(ValueError):
            Automation.from_str("автомат")  # строчные буквы


if __name__ == "__main__":
    unittest.main()
