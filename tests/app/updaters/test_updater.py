#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from unittest.mock import MagicMock, patch

from machine_tools.app.enumerations import Accuracy, Automation, SoftwareControl, Specialization, WeightClass
from machine_tools.app.schemas.machine import Dimensions, Location, MachineUpdate
from machine_tools.app.updaters.updater import MachineUpdater


class TestMachineUpdater(unittest.TestCase):
    """Тесты для MachineUpdater"""

    def setUp(self):
        """Подготовка тестового окружения"""
        # Создаем тестовые данные
        self.test_machine_info = {
            'name': '16К20',
            'group': 1,
            'type': 1,
            'power': 10.0,
            'efficiency': 0.95,
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

    @patch('machine_tools.app.updaters.updater.QueryBuilder')
    @patch('machine_tools.app.updaters.updater.session_manager')
    def test_01_update_by_id_success(self, mock_session_manager, mock_query_builder_class):
        """Тест успешного обновления по ID"""
        # Настраиваем моки
        mock_session = MagicMock()
        mock_session_manager.get_session.return_value = mock_session

        # Создаем мок для QueryBuilder
        mock_builder = MagicMock()
        mock_query_builder_class.return_value = mock_builder

        # Настраиваем цепочку вызовов
        mock_builder.filter_by_id.return_value = mock_builder
        mock_builder.update.return_value = 1

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Создаем обновлятор и вызываем метод
        updater = MachineUpdater(session=mock_session)
        result = updater.update_by_id(1, machine_update)

        # Проверяем результат
        self.assertTrue(result)
        mock_builder.filter_by_id.assert_called_once_with(1)
        mock_builder.update.assert_called_once_with(machine_update.get_flat_dict())

    @patch('machine_tools.app.updaters.updater.QueryBuilder')
    @patch('machine_tools.app.updaters.updater.session_manager')
    def test_02_update_by_id_failure(self, mock_session_manager, mock_query_builder_class):
        """Тест неудачного обновления по ID"""
        # Настраиваем моки
        mock_session = MagicMock()
        mock_session_manager.get_session.return_value = mock_session

        # Создаем мок для QueryBuilder
        mock_builder = MagicMock()
        mock_query_builder_class.return_value = mock_builder

        # Настраиваем цепочку вызовов
        mock_builder.filter_by_id.return_value = mock_builder
        mock_builder.update.return_value = 0

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Создаем обновлятор и вызываем метод
        updater = MachineUpdater()
        result = updater.update_by_id(10, machine_update)

        # Проверяем результат
        self.assertFalse(result)
        mock_builder.filter_by_id.assert_called_once_with(10)
        mock_builder.update.assert_called_once_with(machine_update.get_flat_dict())

    @patch('machine_tools.app.updaters.updater.QueryBuilder')
    @patch('machine_tools.app.updaters.updater.session_manager')
    def test_03_update_by_name(self, mock_session_manager, mock_query_builder_class):
        """Тест обновления по имени"""
        # Настраиваем моки
        mock_session = MagicMock()
        mock_session_manager.get_session.return_value = mock_session

        # Создаем мок для QueryBuilder
        mock_builder = MagicMock()
        mock_query_builder_class.return_value = mock_builder

        # Настраиваем цепочку вызовов
        mock_builder.filter_by_name.return_value = mock_builder
        mock_builder.update.return_value = 1

        # Создаем обновлятор и вызываем метод
        updater = MachineUpdater()
        result = updater.update_by_name("16К20", {"power": 15.0}, case_sensitive=True, exact_match=True)

        # Проверяем результат
        self.assertEqual(result, 1)
        mock_builder.filter_by_name.assert_called_once_with("16К20", case_sensitive=True, exact_match=True)
        mock_builder.update.assert_called_once_with({"power": 15.0})

    @patch('machine_tools.app.updaters.updater.QueryBuilder')
    @patch('machine_tools.app.updaters.updater.session_manager')
    def test_04_update_by_power(self, mock_session_manager, mock_query_builder_class):
        """Тест обновления по мощности"""
        # Настраиваем моки
        mock_session = MagicMock()
        mock_session_manager.get_session.return_value = mock_session

        # Создаем мок для QueryBuilder
        mock_builder = MagicMock()
        mock_query_builder_class.return_value = mock_builder

        # Настраиваем цепочку вызовов
        mock_builder.filter_by_power.return_value = mock_builder
        mock_builder.update.return_value = 2

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Создаем обновлятор и вызываем метод
        updater = MachineUpdater()
        result = updater.update_by_power(machine_update, min_power=5.0, max_power=15.0)

        # Проверяем результат
        self.assertEqual(result, 2)
        mock_builder.filter_by_power.assert_called_once_with(min_power=5.0, max_power=15.0)
        mock_builder.update.assert_called_once_with(machine_update.model_dump(exclude_unset=True))

    @patch('machine_tools.app.updaters.updater.QueryBuilder')
    @patch('machine_tools.app.updaters.updater.session_manager')
    def test_05_update_by_accuracy(self, mock_session_manager, mock_query_builder_class):
        """Тест обновления по точности"""
        # Настраиваем моки
        mock_session = MagicMock()
        mock_session_manager.get_session.return_value = mock_session

        # Создаем мок для QueryBuilder
        mock_builder = MagicMock()
        mock_query_builder_class.return_value = mock_builder

        # Настраиваем цепочку вызовов
        mock_builder.filter_by_accuracy.return_value = mock_builder
        mock_builder.update.return_value = 1

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Создаем обновлятор и вызываем метод
        updater = MachineUpdater()
        result = updater.update_by_accuracy(machine_update, accuracy=Accuracy.P.value)

        # Проверяем результат
        self.assertEqual(result, 1)
        mock_builder.filter_by_accuracy.assert_called_once_with(Accuracy.P.value)
        mock_builder.update.assert_called_once_with(machine_update.get_flat_dict())

    @patch('machine_tools.app.updaters.updater.QueryBuilder')
    @patch('machine_tools.app.updaters.updater.session_manager')
    def test_06_update_by_automation(self, mock_session_manager, mock_query_builder_class):
        """Тест обновления по автоматизации"""
        # Настраиваем моки
        mock_session = MagicMock()
        mock_session_manager.get_session.return_value = mock_session

        # Создаем мок для QueryBuilder
        mock_builder = MagicMock()
        mock_query_builder_class.return_value = mock_builder

        # Настраиваем цепочку вызовов
        mock_builder.filter_by_automation.return_value = mock_builder
        mock_builder.update.return_value = 1

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Создаем обновлятор и вызываем метод
        updater = MachineUpdater()
        result = updater.update_by_automation(machine_update, automation=Automation.AUTOMATIC.value)

        # Проверяем результат
        self.assertEqual(result, 1)
        mock_builder.filter_by_automation.assert_called_once_with(Automation.AUTOMATIC.value)
        mock_builder.update.assert_called_once_with(machine_update.get_flat_dict())

    @patch('machine_tools.app.updaters.updater.QueryBuilder')
    @patch('machine_tools.app.updaters.updater.session_manager')
    def test_07_update_by_specialization(self, mock_session_manager, mock_query_builder_class):
        """Тест обновления по специализации"""
        # Настраиваем моки
        mock_session = MagicMock()
        mock_session_manager.get_session.return_value = mock_session

        # Создаем мок для QueryBuilder
        mock_builder = MagicMock()
        mock_query_builder_class.return_value = mock_builder

        # Настраиваем цепочку вызовов
        mock_builder.filter_by_specialization.return_value = mock_builder
        mock_builder.update.return_value = 1

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Создаем обновлятор и вызываем метод
        updater = MachineUpdater()
        result = updater.update_by_specialization(machine_update, specialization=Specialization.UNIVERSAL.value)

        # Проверяем результат
        self.assertEqual(result, 1)
        mock_builder.filter_by_specialization.assert_called_once_with(Specialization.UNIVERSAL.value)
        mock_builder.update.assert_called_once_with(machine_update.get_flat_dict())

    @patch('machine_tools.app.updaters.updater.QueryBuilder')
    @patch('machine_tools.app.updaters.updater.session_manager')
    def test_08_update_by_software_control(self, mock_session_manager, mock_query_builder_class):
        """Тест обновления по программному управлению"""
        # Настраиваем моки
        mock_session = MagicMock()
        mock_session_manager.get_session.return_value = mock_session

        # Создаем мок для QueryBuilder
        mock_builder = MagicMock()
        mock_query_builder_class.return_value = mock_builder

        # Настраиваем цепочку вызовов
        mock_builder.filter_by_software_control.return_value = mock_builder
        mock_builder.update.return_value = 1

        # Создаем тестовые данные
        machine_update = MachineUpdate(**self.test_machine_info)

        # Создаем обновлятор и вызываем метод
        updater = MachineUpdater()
        result = updater.update_by_software_control(machine_update, software_control=SoftwareControl.CNC.value)

        # Проверяем результат
        self.assertEqual(result, 1)
        mock_builder.filter_by_software_control.assert_called_once_with(SoftwareControl.CNC.value)
        mock_builder.update.assert_called_once_with(machine_update.get_flat_dict())

    def test_09_context_manager(self):
        """Тест использования как контекстный менеджер"""
        with patch('machine_tools.app.updaters.updater.session_manager') as mock_session_manager:
            mock_session = MagicMock()
            mock_session_manager.get_session.return_value = mock_session

            with MachineUpdater() as updater:
                self.assertIsInstance(updater, MachineUpdater)
                mock_session_manager.get_session.assert_called_once()

            mock_session_manager.close_session.assert_called_once()


if __name__ == "__main__":
    unittest.main()
