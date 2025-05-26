#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from datetime import datetime

from pydantic import ValidationError

from machine_tools.app.enumerations import Accuracy, Automation, SoftwareControl, Specialization, WeightClass
from machine_tools.app.schemas.machine import (
    Dimensions,
    Location,
    Machine,
    MachineCreate,
    MachineInfo,
    MachineUpdate,
)


class TestDimensions(unittest.TestCase):
    """Тесты для схемы Dimensions"""

    def test_01_valid_dimensions(self):
        """Тест валидных размеров"""
        dimensions = Dimensions(length=2000, width=1000, height=1500, overall_diameter="2000x1000x1500")
        self.assertEqual(dimensions.length, 2000)
        self.assertEqual(dimensions.width, 1000)
        self.assertEqual(dimensions.height, 1500)
        self.assertEqual(dimensions.overall_diameter, "2000x1000x1500")

    def test_02_invalid_dimensions(self):
        """Тест невалидных размеров"""
        with self.assertRaises(ValidationError):
            Dimensions(length=-1)  # Отрицательная длина

        with self.assertRaises(ValidationError):
            Dimensions(width=0)  # Нулевая ширина

        with self.assertRaises(ValidationError):
            Dimensions(height=-100)  # Отрицательная высота


class TestLocation(unittest.TestCase):
    """Тесты для схемы Location"""

    def test_01_valid_location(self):
        """Тест валидного местоположения"""
        location = Location(city="Москва", manufacturer="Завод им. Орджоникидзе")
        self.assertEqual(location.city, "Москва")
        self.assertEqual(location.manufacturer, "Завод им. Орджоникидзе")

    def test_02_empty_location(self):
        """Тест пустого местоположения"""
        location = Location()
        self.assertIsNone(location.city)
        self.assertIsNone(location.manufacturer)


class TestMachineInfo(unittest.TestCase):
    """Тесты для схемы MachineInfo"""

    def test_01_valid_machine_info(self):
        """Тест валидной информации о станке"""
        machine = MachineInfo(
            name="16К20",
            group=1,
            type=1,
            power=10.0,
            efficiency=0.85,
            accuracy=Accuracy.P,
            automation=Automation.AUTOMATIC,
            software_control=SoftwareControl.CNC,
            specialization=Specialization.UNIVERSAL,
            weight=2000.0,
            weight_class=WeightClass.MEDIUM,
            dimensions=Dimensions(length=2000, width=1000, height=1500, overall_diameter="2000x1000x1500"),
            location=Location(city="Москва", manufacturer="Завод им. Орджоникидзе"),
            machine_type="Токарный",
        )
        self.assertEqual(machine.name, "16К20")
        self.assertEqual(machine.group, 1)
        self.assertEqual(machine.type, 1)
        self.assertEqual(machine.power, 10.0)
        self.assertEqual(machine.efficiency, 0.85)
        self.assertEqual(machine.accuracy, Accuracy.P)
        self.assertEqual(machine.automation, Automation.AUTOMATIC)
        self.assertEqual(machine.software_control, SoftwareControl.CNC)
        self.assertEqual(machine.specialization, Specialization.UNIVERSAL)
        self.assertEqual(machine.weight, 2000.0)
        self.assertEqual(machine.weight_class, WeightClass.MEDIUM)
        self.assertEqual(machine.dimensions.length, 2000)
        self.assertEqual(machine.dimensions.width, 1000)
        self.assertEqual(machine.dimensions.height, 1500)
        self.assertEqual(machine.dimensions.overall_diameter, "2000x1000x1500")
        self.assertEqual(machine.location.city, "Москва")
        self.assertEqual(machine.location.manufacturer, "Завод им. Орджоникидзе")
        self.assertEqual(machine.machine_type, "Токарный")

    def test_02_default_values(self):
        """Тест значений по умолчанию"""
        machine = MachineInfo(name="16К20")
        self.assertEqual(machine.accuracy, Accuracy.NO_DATA)
        self.assertEqual(machine.automation, Automation.MANUAL)
        self.assertEqual(machine.software_control, SoftwareControl.NO)
        self.assertEqual(machine.specialization, Specialization.UNIVERSAL)
        self.assertEqual(machine.weight_class, WeightClass.LIGHT)
        self.assertIsNone(machine.group)
        self.assertIsNone(machine.type)
        self.assertIsNone(machine.power)
        self.assertIsNone(machine.efficiency)
        self.assertIsNone(machine.weight)
        self.assertIsNone(machine.dimensions)
        self.assertIsNone(machine.location)
        self.assertIsNone(machine.machine_type)
        self.assertIsNone(machine.technical_requirements)

    def test_03_invalid_values(self):
        """Тест невалидных значений"""
        # Пустое имя
        with self.assertRaises(ValidationError):
            MachineInfo(name="")

        # Отрицательная группа
        with self.assertRaises(ValidationError):
            MachineInfo(name="16К20", group=-1)

        # Группа больше 9
        with self.assertRaises(ValidationError):
            MachineInfo(name="16К20", group=10)

        # Отрицательная мощность
        with self.assertRaises(ValidationError):
            MachineInfo(name="16К20", power=-10.0)

        # КПД больше 1
        with self.assertRaises(ValidationError):
            MachineInfo(name="16К20", efficiency=1.5)

        # Отрицательная масса
        with self.assertRaises(ValidationError):
            MachineInfo(name="16К20", weight=-2000.0)


class TestMachineUpdate(unittest.TestCase):
    """Тесты для схемы MachineUpdate"""

    def test_01_get_flat_dict(self):
        """Тест преобразования в плоский словарь"""
        machine = MachineUpdate(
            name="16К20",
            dimensions=Dimensions(length=2000, width=1000, height=1500, overall_diameter="2000x1000x1500"),
            location=Location(city="Москва", manufacturer="Завод им. Орджоникидзе"),
            accuracy=Accuracy.P,
            automation=Automation.AUTOMATIC,
            software_control=SoftwareControl.CNC,
            specialization=Specialization.UNIVERSAL,
            weight_class=WeightClass.MEDIUM,
        )

        flat_dict = machine.get_flat_dict()

        # Проверяем, что вложенные структуры развернуты
        self.assertEqual(flat_dict['length'], 2000)
        self.assertEqual(flat_dict['width'], 1000)
        self.assertEqual(flat_dict['height'], 1500)
        self.assertEqual(flat_dict['overall_diameter'], "2000x1000x1500")
        self.assertEqual(flat_dict['city'], "Москва")
        self.assertEqual(flat_dict['manufacturer'], "Завод им. Орджоникидзе")

        # Проверяем, что Enum значения преобразованы в строки
        self.assertEqual(flat_dict['accuracy'], Accuracy.P.value)
        self.assertEqual(flat_dict['automation'], Automation.AUTOMATIC.value)
        self.assertEqual(flat_dict['software_control'], SoftwareControl.CNC.value)
        self.assertEqual(flat_dict['specialization'], Specialization.UNIVERSAL.value)
        self.assertEqual(flat_dict['weight_class'], WeightClass.MEDIUM.value)

        # Проверяем, что вложенные структуры удалены
        self.assertNotIn('dimensions', flat_dict)
        self.assertNotIn('location', flat_dict)


class TestMachine(unittest.TestCase):
    """Тесты для схемы Machine"""

    def test_01_valid_machine(self):
        """Тест валидного станка"""
        now = datetime.utcnow()
        machine = Machine(id=1, name="16К20", created_at=now, updated_at=now)
        self.assertEqual(machine.id, 1)
        self.assertEqual(machine.name, "16К20")
        self.assertEqual(machine.created_at, now)
        self.assertEqual(machine.updated_at, now)


if __name__ == "__main__":
    unittest.main()
