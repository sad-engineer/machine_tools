#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from datetime import datetime
from typing import List

from machine_tools.app.enumerations import Accuracy, Automation, SoftwareControl, Specialization, WeightClass
from machine_tools.app.formatters import (
    DictMachineInfoFormatter,
    DictNameFormatter,
    IndexedMachineInfoFormatter,
    IndexedNameFormatter,
    ListMachineInfoFormatter,
    ListNameFormatter,
)
from machine_tools.app.models.machine import Machine
from machine_tools.app.models.technical_requirement import TechnicalRequirement
from machine_tools.app.schemas.machine import MachineInfo


class TestMachineFormatters(unittest.TestCase):
    """Тесты для форматтеров станков"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.machines = [
            Machine(
                id=1,
                name="16К20",
                group=1.0,
                type=2.0,
                power=10.5,
                efficiency=0.85,
                accuracy=Accuracy.P,
                automation=Automation.AUTOMATIC,
                specialization=Specialization.SPECIAL,
                software_control=SoftwareControl.NO,
                weight=2500.0,
                weight_class=WeightClass.LIGHT,
                length=2000,
                width=1000,
                height=1500,
                overall_diameter="Ø 400",
                city="Коломна",
                manufacturer="СтанкоМаш",
                machine_type="Токарный",
                created_at=datetime(2024, 1, 1),
                updated_at=datetime(2024, 1, 1),
                technical_requirements=[
                    TechnicalRequirement(id=1, machine_name="16К20", requirement="max_diameter", value=400),
                    TechnicalRequirement(id=2, machine_name="16К20", requirement="max_length", value=1000),
                    TechnicalRequirement(id=3, machine_name="16К20", requirement="spindle_speed", value=2000),
                ],
            ),
            Machine(
                id=2,
                name="6Р13Ф3",
                group=2.0,
                type=1.0,
                power=7.5,
                efficiency=0.8,
                accuracy=Accuracy.P,
                automation=Automation.MANUAL,
                specialization=Specialization.UNIVERSAL,
                software_control=SoftwareControl.CNC,
                weight=1800.0,
                weight_class=WeightClass.LIGHT,
                length=1800,
                width=900,
                height=1400,
                overall_diameter="Ø 300",
                city="Москва",
                manufacturer="МЗТС",
                machine_type="Фрезерный",
                created_at=datetime(2024, 1, 1),
                updated_at=datetime(2024, 1, 1),
                technical_requirements=[
                    TechnicalRequirement(id=4, machine_name="6Р13Ф3", requirement="table_size", value="400x1600"),
                    TechnicalRequirement(id=5, machine_name="6Р13Ф3", requirement="max_travel", value=800),
                    TechnicalRequirement(id=6, machine_name="6Р13Ф3", requirement="spindle_speed", value=1500),
                ],
            ),
        ]

    def test_01_list_name_formatter(self):
        """Тест форматтера ListNameFormatter"""
        formatter = ListNameFormatter()
        result = formatter.format(self.machines)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, ['16К20', '6Р13Ф3'])

    def test_02_list_machine_info_formatter(self):
        """Тест форматтера ListMachineInfoFormatter"""
        formatter = ListMachineInfoFormatter()
        result = formatter.format(self.machines)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], MachineInfo)
        self.assertEqual(result[0].name, '16К20')
        self.assertEqual(result[1].name, '6Р13Ф3')

    def test_03_dict_name_formatter(self):
        """Тест форматтера DictNameFormatter"""
        formatter = DictNameFormatter()
        result = formatter.format(self.machines)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1], '16К20')
        self.assertEqual(result[2], '6Р13Ф3')

    def test_04_dict_machine_info_formatter(self):
        """Тест форматтера DictMachineInfoFormatter"""
        formatter = DictMachineInfoFormatter()
        result = formatter.format(self.machines)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result['6Р13Ф3'], MachineInfo)
        self.assertEqual(result['16К20'].name, '16К20')
        self.assertEqual(result['6Р13Ф3'].name, '6Р13Ф3')

    def test_05_indexed_name_formatter(self):
        """Тест форматтера IndexedNameFormatter"""
        formatter = IndexedNameFormatter()
        result = formatter.format(self.machines)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1], '16К20')
        self.assertEqual(result[2], '6Р13Ф3')

    def test_06_indexed_machine_info_formatter(self):
        """Тест форматтера IndexedMachineInfoFormatter"""
        formatter = IndexedMachineInfoFormatter()
        result = formatter.format(self.machines)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[1], MachineInfo)
        self.assertEqual(result[1].name, '16К20')
        self.assertEqual(result[2].name, '6Р13Ф3')

    def test_07_empty_list(self):
        """Тест форматтеров с пустым списком"""
        empty_machines: List[Machine] = []

        # Проверяем все форматтеры
        formatters = [
            ListNameFormatter(),
            ListMachineInfoFormatter(),
            DictNameFormatter(),
            DictMachineInfoFormatter(),
            IndexedNameFormatter(),
            IndexedMachineInfoFormatter(),
        ]

        for formatter in formatters:
            result = formatter.format(empty_machines)
            if isinstance(result, list):
                self.assertEqual(len(result), 0)
            elif isinstance(result, dict):
                self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
