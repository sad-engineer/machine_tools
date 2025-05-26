#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from unittest.mock import MagicMock, patch

from machine_tools.app.enumerations import Accuracy, Automation, SoftwareControl, Specialization, WeightClass
from machine_tools.app.schemas.machine import Dimensions, Location, MachineInfo, MachineUpdate
from machine_tools.app.services.scripts import (
    _dict_to_machine_update,
    find_names,
    get_machine_info_by_name,
    update,
)


class TestScripts(unittest.TestCase):
    """Тесты для скриптов"""

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

    @patch('machine_tools.app.services.scripts.FinderContainer')
    def test_01_find_names_with_substring(self, mock_container):
        """Тест поиска имен по подстроке"""
        # Настраиваем мок
        mock_finder = MagicMock()
        mock_finder.by_name.return_value = ["16К20", "16К20Ф3"]
        mock_container.return_value.finder_with_list_names.return_value = mock_finder

        # Вызываем функцию
        result = find_names("16К20")

        # Проверяем результат
        self.assertEqual(result, ["16К20", "16К20Ф3"])
        mock_finder.by_name.assert_called_once_with("16К20", exact_match=False)

    @patch('machine_tools.app.services.scripts.FinderContainer')
    def test_02_find_names_without_substring(self, mock_container):
        """Тест получения всех имен"""
        # Настраиваем мок
        mock_finder = MagicMock()
        mock_finder.all.return_value = ["16К20", "16К20Ф3", "1К62"]
        mock_container.return_value.finder_with_list_names.return_value = mock_finder

        # Вызываем функцию
        result = find_names(None)

        # Проверяем результат
        self.assertEqual(result, ["16К20", "16К20Ф3", "1К62"])
        mock_finder.all.assert_called_once()

    @patch('machine_tools.app.services.scripts.FinderContainer')
    def test_03_get_machine_info_by_name_found(self, mock_container):
        """Тест получения информации о станке (станок найден)"""
        # Настраиваем мок
        mock_finder = MagicMock()
        mock_finder.by_name.return_value = [MachineInfo(**self.test_machine_info)]
        mock_container.return_value.finder_with_list_info.return_value = mock_finder

        # Вызываем функцию
        result = get_machine_info_by_name("16К20")

        # Проверяем результат
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "16К20")
        mock_finder.by_name.assert_called_once_with("16К20", exact_match=True)

    @patch('machine_tools.app.services.scripts.FinderContainer')
    def test_04_get_machine_info_by_name_not_found(self, mock_container):
        """Тест получения информации о станке (станок не найден)"""
        # Настраиваем мок
        mock_finder = MagicMock()
        mock_finder.by_name.return_value = []
        mock_container.return_value.finder_with_list_info.return_value = mock_finder

        # Вызываем функцию
        result = get_machine_info_by_name("НесуществующийСтанок")

        # Проверяем результат
        self.assertIsNone(result)
        mock_finder.by_name.assert_called_once_with("НесуществующийСтанок", exact_match=True)

    def test_05_dict_to_machine_update(self):
        """Тест преобразования словаря в MachineUpdate"""
        # Проверяем значение в словаре перед вызовом
        # Вызываем функцию
        result = _dict_to_machine_update(self.test_machine_info)

        # Проверяем результат
        self.assertIsInstance(result, MachineUpdate)
        self.assertEqual(result.name, "16К20")
        self.assertEqual(result.group, 1)
        self.assertEqual(result.type, 1)
        self.assertEqual(result.power, 10.0)
        self.assertEqual(result.efficiency, 0.85)
        self.assertEqual(result.accuracy, Accuracy.P)
        self.assertEqual(result.automation, Automation.AUTOMATIC)
        self.assertEqual(result.software_control, SoftwareControl.CNC)
        self.assertEqual(result.specialization, Specialization.UNIVERSAL)
        self.assertEqual(result.weight, 2000.0)
        self.assertEqual(result.weight_class, WeightClass.MEDIUM)
        self.assertEqual(result.dimensions.length, 2000)
        self.assertEqual(result.dimensions.width, 1000)
        self.assertEqual(result.dimensions.height, 1500)
        self.assertEqual(result.dimensions.overall_diameter, "2000x1000x1500")
        self.assertEqual(result.location.city, "Москва")
        self.assertEqual(result.location.manufacturer, "Завод им. Орджоникидзе")
        self.assertEqual(result.machine_type, "Токарный")

    @patch('machine_tools.app.services.scripts.update_by_machine_info')
    def test_06_update_with_machine_info(self, mock_update):
        """Тест обновления с MachineInfo"""
        # Настраиваем мок
        mock_update.return_value = True

        # Создаем тестовые данные
        machine_info = MachineInfo(**self.test_machine_info)

        # Вызываем функцию
        result = update(machine_info)

        # Проверяем результат
        self.assertTrue(result)
        mock_update.assert_called_once_with(machine_info)

    @patch('machine_tools.app.updaters.utils.update_by_machine_update')
    def test_07_update_with_machine_update(self, mock_update):
        """Тест обновления с MachineUpdate"""
        # Настраиваем мок
        mock_update.return_value = True

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Вызываем функцию
        result = update(machine_update)

        # Проверяем результат
        self.assertTrue(result)
        mock_update.assert_called_once_with(machine_update)

    @patch('machine_tools.app.services.scripts.update_by_machine_update')
    def test_08_update_with_dict(self, mock_update):
        """Тест обновления со словарем"""
        # Настраиваем мок
        mock_update.return_value = True

        # Вызываем функцию
        result = update(self.test_machine_info)

        # Проверяем результат
        self.assertTrue(result)
        mock_update.assert_called_once()

    def test_09_update_with_invalid_type(self):
        """Тест обновления с невалидным типом"""
        # Вызываем функцию с невалидным типом
        with self.assertRaises(ValueError) as context:
            update("невалидный_тип")

        # Проверяем сообщение об ошибке
        self.assertIn("info должен быть экземпляром MachineInfo или MachineUpdate", str(context.exception))


if __name__ == "__main__":
    unittest.main()
