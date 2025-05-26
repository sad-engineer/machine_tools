#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from unittest.mock import MagicMock, patch

from machine_tools.app.enumerations import Accuracy, Automation, SoftwareControl, Specialization, WeightClass
from machine_tools.app.schemas.machine import Dimensions, Location, MachineInfo, MachineUpdate
from machine_tools.app.updaters.utils import update_by_machine_info, update_by_machine_update


class TestUtils(unittest.TestCase):
    """Тесты для утилит обновления"""

    def setUp(self):
        """Подготовка тестового окружения"""
        # Создаем тестовые данные
        self.test_machine_info = {
            'name': '16К20',
            'group': 1,
            'type': 1,
            'power': 10.0,
            'efficiency': 0.85,
            'accuracy': Accuracy.P,
            'automation': Automation.AUTOMATIC,
            'software_control': SoftwareControl.CNC,
            'specialization': Specialization.UNIVERSAL,
            'weight': 2000.0,
            'weight_class': WeightClass.MEDIUM,
            'dimensions': Dimensions(length=2000, width=1000, height=1500, overall_diameter="2000x1000x1500"),
            'location': Location(city="Москва", manufacturer="Завод им. Орджоникидзе"),
            'machine_type': "Токарный",
            'technical_requirements': None,
        }

    @patch('machine_tools.app.updaters.utils.MachineUpdater')
    def test_01_update_by_machine_update_success(self, mock_updater_class):
        """Тест успешного обновления через MachineUpdate"""
        # Настраиваем мок
        mock_updater = MagicMock()
        mock_updater_class.return_value = mock_updater
        mock_updater.update_by_name.return_value = 1

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Вызываем функцию
        result = update_by_machine_update(machine_update)

        # Проверяем результат
        self.assertTrue(result)
        mock_updater.update_by_name.assert_called_once_with(machine_update.name, machine_update.get_flat_dict())

    @patch('machine_tools.app.updaters.utils.MachineUpdater')
    def test_02_update_by_machine_update_failure(self, mock_updater_class):
        """Тест неудачного обновления через MachineUpdate"""
        # Настраиваем мок
        mock_updater = MagicMock()
        mock_updater_class.return_value = mock_updater
        mock_updater.update_by_name.return_value = 0

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Вызываем функцию
        result = update_by_machine_update(machine_update)

        # Проверяем результат
        self.assertFalse(result)
        mock_updater.update_by_name.assert_called_once_with(machine_update.name, machine_update.get_flat_dict())

    def test_03_update_by_machine_update_invalid_type(self):
        """Тест обновления с невалидным типом"""
        # Вызываем функцию с невалидным типом
        with self.assertRaises(ValueError) as context:
            update_by_machine_update("невалидный_тип")

        # Проверяем сообщение об ошибке
        self.assertIn("info должен быть экземпляром MachineUpdate", str(context.exception))

    @patch('machine_tools.app.updaters.utils.update_by_machine_update')
    def test_04_update_by_machine_info_success(self, mock_update):
        """Тест успешного обновления через MachineInfo"""
        # Настраиваем мок
        mock_update.return_value = True

        # Создаем тестовые данные
        machine_info = MachineInfo(**self.test_machine_info)

        # Вызываем функцию
        result = update_by_machine_info(machine_info)

        # Проверяем результат
        self.assertTrue(result)
        mock_update.assert_called_once()

    def test_05_update_by_machine_info_invalid_type(self):
        """Тест обновления с невалидным типом"""
        # Вызываем функцию с невалидным типом
        with self.assertRaises(ValueError) as context:
            update_by_machine_info("невалидный_тип")

        # Проверяем сообщение об ошибке
        self.assertIn("info должен быть экземпляром MachineInfo", str(context.exception))


if __name__ == "__main__":
    unittest.main()
