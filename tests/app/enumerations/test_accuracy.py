#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest

from machine_tools.app.enumerations.accuracy import Accuracy


class TestAccuracy(unittest.TestCase):
    """Тесты для перечисления Accuracy"""

    def test_01_values(self):
        """Тест проверки значений перечисления"""
        # Проверяем все значения
        self.assertEqual(Accuracy.S.value, "С")
        self.assertEqual(Accuracy.S_A.value, "С/А")
        self.assertEqual(Accuracy.A.value, "А")
        self.assertEqual(Accuracy.V_A.value, "В/А")
        self.assertEqual(Accuracy.V.value, "В")
        self.assertEqual(Accuracy.P_V.value, "П/В")
        self.assertEqual(Accuracy.P.value, "П")
        self.assertEqual(Accuracy.N_P.value, "Н/П")
        self.assertEqual(Accuracy.N.value, "Н")
        self.assertEqual(Accuracy.NO_DATA.value, "Нет данных")
        self.assertEqual(Accuracy.TU_TB_16_0001.value, "ТУ ТВ-16-0001")

    def test_02_from_str_valid(self):
        """Тест преобразования корректных строковых значений"""
        # Проверяем преобразование для каждого значения
        self.assertEqual(Accuracy.from_str("С"), Accuracy.S)
        self.assertEqual(Accuracy.from_str("С/А"), Accuracy.S_A)
        self.assertEqual(Accuracy.from_str("А"), Accuracy.A)
        self.assertEqual(Accuracy.from_str("В/А"), Accuracy.V_A)
        self.assertEqual(Accuracy.from_str("В"), Accuracy.V)
        self.assertEqual(Accuracy.from_str("П/В"), Accuracy.P_V)
        self.assertEqual(Accuracy.from_str("П"), Accuracy.P)
        self.assertEqual(Accuracy.from_str("Н/П"), Accuracy.N_P)
        self.assertEqual(Accuracy.from_str("Н"), Accuracy.N)
        self.assertEqual(Accuracy.from_str("Нет данных"), Accuracy.NO_DATA)
        self.assertEqual(Accuracy.from_str("ТУ ТВ-16-0001"), Accuracy.TU_TB_16_0001)

        # Проверяем обработку пробелов
        self.assertEqual(Accuracy.from_str("  С  "), Accuracy.S)
        self.assertEqual(Accuracy.from_str("  С/А  "), Accuracy.S_A)

    def test_03_from_str_invalid(self):
        """Тест обработки некорректных строковых значений"""
        # Проверяем обработку некорректных значений
        with self.assertRaises(ValueError) as context:
            Accuracy.from_str("Некорректное значение")

        # Проверяем, что сообщение об ошибке содержит список допустимых значений
        error_message = str(context.exception)
        self.assertIn("Недопустимое значение точности", error_message)
        self.assertIn("Допустимые значения", error_message)
        for value in [m.value for m in Accuracy]:
            self.assertIn(value, error_message)

    def test_04_case_sensitivity(self):
        """Тест чувствительности к регистру"""
        # Проверяем, что значения чувствительны к регистру
        with self.assertRaises(ValueError):
            Accuracy.from_str("с")  # строчная буква вместо заглавной

        with self.assertRaises(ValueError):
            Accuracy.from_str("С/а")  # строчная буква в середине


if __name__ == "__main__":
    unittest.main()
