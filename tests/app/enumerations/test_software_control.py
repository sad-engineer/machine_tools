#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest

from machine_tools.app.enumerations.software_control import SoftwareControl


class TestSoftwareControl(unittest.TestCase):
    """Тесты для перечисления SoftwareControl"""

    def test_01_values(self):
        """Тест проверки значений перечисления"""

        self.assertEqual(SoftwareControl.NO.value, "Нет")
        self.assertEqual(SoftwareControl.IC.value, "УЦИ")
        self.assertEqual(SoftwareControl.CNC.value, "ЧПУ")

    def test_02_from_str_valid(self):
        """Тест преобразования корректных строковых значений"""

        self.assertEqual(SoftwareControl.from_str("Нет"), SoftwareControl.NO)
        self.assertEqual(SoftwareControl.from_str("УЦИ"), SoftwareControl.IC)
        self.assertEqual(SoftwareControl.from_str("ЧПУ"), SoftwareControl.CNC)

        self.assertEqual(SoftwareControl.from_str("  Нет  "), SoftwareControl.NO)
        self.assertEqual(SoftwareControl.from_str("  УЦИ  "), SoftwareControl.IC)

    def test_03_from_str_invalid(self):
        """Тест обработки некорректных строковых значений"""

        with self.assertRaises(ValueError) as context:
            SoftwareControl.from_str("Некорректное значение")

        error_message = str(context.exception)
        self.assertIn("Недопустимое значение программного управления", error_message)
        self.assertIn("Допустимые значения", error_message)
        for value in [m.value for m in SoftwareControl]:
            self.assertIn(value, error_message)

    def test_04_case_sensitivity(self):
        """Тест чувствительности к регистру"""

        with self.assertRaises(ValueError):
            SoftwareControl.from_str("нет")  # строчные буквы

        with self.assertRaises(ValueError):
            SoftwareControl.from_str("Чпу")  # неправильный регистр


if __name__ == "__main__":
    unittest.main()
