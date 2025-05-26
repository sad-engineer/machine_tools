#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from datetime import datetime
from unittest.mock import Mock

from machine_tools.app.finders.finder import MachineFinder
from machine_tools.app.formatters import (
    ListMachineInfoFormatter,
    ListNameFormatter,
)
from machine_tools.app.models.machine import Machine
from machine_tools.app.models.technical_requirement import TechnicalRequirement


class TestMachineFinder(unittest.TestCase):
    """Тесты для MachineFinder"""

    @classmethod
    def setUpClass(cls):
        """Подготовка тестовой БД"""
        # Создаем тестовые данные
        cls.machines = [
            Machine(
                id=1,
                name="16К20",
                group=1.0,
                type=2.0,
                power=10.5,
                efficiency=0.85,
                accuracy="Н",
                automation="ЧПУ",
                specialization="Токарная обработка",
                weight=2500.0,
                weight_class="Средний",
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
                ],
            ),
            Machine(
                id=2,
                name="6Р13Ф3",
                group=2.0,
                type=1.0,
                power=7.5,
                efficiency=0.8,
                accuracy="П",
                automation="Ручное управление",
                specialization="Фрезерная обработка",
                weight=1800.0,
                weight_class="Средний",
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
                    TechnicalRequirement(id=3, machine_name="6Р13Ф3", requirement="table_size", value="400x1600"),
                    TechnicalRequirement(id=4, machine_name="6Р13Ф3", requirement="max_travel", value=800),
                ],
            ),
            Machine(
                id=3,
                name="2А135",
                group=1.0,
                type=3.0,
                power=5.5,
                efficiency=0.75,
                accuracy="Н",
                automation="ЧПУ",
                specialization="Сверлильная обработка",
                weight=1500.0,
                weight_class="Средний",
                length=1500,
                width=800,
                height=1200,
                overall_diameter="Ø 200",
                city="Санкт-Петербург",
                manufacturer="ЛЗОС",
                machine_type="Сверлильный",
                created_at=datetime(2024, 1, 1),
                updated_at=datetime(2024, 1, 1),
                technical_requirements=[
                    TechnicalRequirement(id=5, machine_name="2А135", requirement="max_drill_diameter", value=35),
                    TechnicalRequirement(id=6, machine_name="2А135", requirement="max_depth", value=300),
                ],
            ),
        ]

    def setUp(self):
        """Подготовка перед каждым тестом"""
        # Создаем мок для сессии БД
        self.mock_session = Mock()
        self.mock_session.query.return_value = self.mock_session
        self.mock_session.filter.return_value = self.mock_session
        self.mock_session.order_by.return_value = self.mock_session
        self.mock_session.limit.return_value = self.mock_session
        self.mock_session.all.return_value = self.machines

        # Создаем мок для форматтера
        self.mock_formatter = Mock()

        # Создаем мок для builder
        self.mock_builder = Mock()
        self.mock_builder.filter_by_power.return_value = self.mock_builder
        self.mock_builder.filter_by_efficiency.return_value = self.mock_builder
        self.mock_builder.filter_by_accuracy.return_value = self.mock_builder
        self.mock_builder.filter_by_automation.return_value = self.mock_builder
        self.mock_builder.filter_by_specialization.return_value = self.mock_builder
        self.mock_builder.filter_by_name.return_value = self.mock_builder
        self.mock_builder.filter_by_software_control.return_value = self.mock_builder
        self.mock_builder.order_by.return_value = self.mock_builder
        self.mock_builder.limit.return_value = self.mock_builder
        self.mock_builder.execute.return_value = self.machines

        # Создаем finder с моками
        self.finder = MachineFinder(session=self.mock_session)
        self.finder._formatter = self.mock_formatter
        self.finder._builder = self.mock_builder

    def test_01_by_power(self):
        """Тест поиска по мощности"""
        # Поиск станков с мощностью больше 7 кВт
        self.finder.find_by_power(min_power=7.0)
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_power.assert_called_once_with(min_power=7.0, max_power=None)
        self.mock_builder.execute.assert_called_once()

        # Поиск станков с мощностью меньше 6 кВт
        self.finder.find_by_power(max_power=6.0)
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_power.assert_called_with(min_power=None, max_power=6.0)
        self.mock_builder.execute.assert_called()

        # Сортировка по мощности
        self.finder.find_by_power(order_by_power=True, descending=True)
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_power.assert_called_with(min_power=None, max_power=None)
        self.mock_builder.order_by.assert_called_once_with("power", descending=True)
        self.mock_builder.execute.assert_called()

    def test_02_by_efficiency(self):
        """Тест поиска по КПД"""
        # Поиск станков с КПД больше 0.8
        self.finder.find_by_efficiency(min_efficiency=0.8)
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_efficiency.assert_called_once_with(min_efficiency=0.8, max_efficiency=None)
        self.mock_builder.execute.assert_called_once()

        # Сортировка по КПД
        self.finder.find_by_efficiency(order_by_efficiency=True, descending=True)
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_efficiency.assert_called_with(min_efficiency=None, max_efficiency=None)
        self.mock_builder.order_by.assert_called_once_with("efficiency", descending=True)
        self.mock_builder.execute.assert_called()

    def test_03_by_accuracy(self):
        """Тест поиска по классу точности"""
        # Поиск станков класса точности "Н"
        self.finder.find_by_accuracy("Н")
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_accuracy.assert_called_once_with("Н")
        self.mock_builder.execute.assert_called_once()

        # Поиск станков нескольких классов точности
        self.finder.find_by_accuracy(["Н", "П"])
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_accuracy.assert_called_with(["Н", "П"])
        self.mock_builder.execute.assert_called()

    def test_04_by_automation(self):
        """Тест поиска по уровню автоматизации"""
        # Поиск станков с ЧПУ
        self.finder.find_by_automation("ЧПУ")
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_automation.assert_called_once_with("ЧПУ")
        self.mock_builder.execute.assert_called_once()

        # Поиск станков с разными уровнями автоматизации
        self.finder.find_by_automation(["ЧПУ", "Ручное управление"])
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_automation.assert_called_with(["ЧПУ", "Ручное управление"])
        self.mock_builder.execute.assert_called()

    def test_05_by_specialization(self):
        """Тест поиска по специализации"""
        # Поиск токарных станков
        self.finder.find_by_specialization("Токарная обработка")
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_specialization.assert_called_once_with("Токарная обработка")
        self.mock_builder.execute.assert_called_once()

        # Поиск станков разных специализаций
        self.finder.find_by_specialization(["Токарная обработка", "Фрезерная обработка"])
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_specialization.assert_called_with(["Токарная обработка", "Фрезерная обработка"])
        self.mock_builder.execute.assert_called()

    def test_06_by_name(self):
        """Тест поиска по имени"""
        # Поиск по точному совпадению (по умолчанию)
        self.finder.find_by_name("16К20")
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_name.assert_called_once_with(name="16К20", case_sensitive=False, exact_match=True)
        self.mock_builder.execute.assert_called_once()

        # Поиск по вхождению строки
        self.finder.find_by_name("16К20", exact_match=False)
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_name.assert_called_with(name="16К20", case_sensitive=False, exact_match=False)
        self.mock_builder.execute.assert_called()

        # Поиск с учетом регистра
        self.finder.find_by_name("16к20", case_sensitive=True)
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_name.assert_called_with(name="16к20", case_sensitive=True, exact_match=True)
        self.mock_builder.execute.assert_called()

        # Поиск по вхождению с учетом регистра
        self.finder.find_by_name("16к20", case_sensitive=True, exact_match=False)
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_name.assert_called_with(name="16к20", case_sensitive=True, exact_match=False)
        self.mock_builder.execute.assert_called()

    def test_07_all(self):
        """Тест получения всех станков"""
        self.finder.find_all()
        # Проверяем, что builder вызван без параметров
        self.mock_builder.execute.assert_called_once()

    def test_08_formatters(self):
        """Тест работы с форматтерами"""
        # Проверяем, что форматтер устанавливается
        formatter = ListNameFormatter()
        self.finder.set_formatter(formatter)
        self.assertEqual(self.finder._formatter, formatter)

        # Проверяем, что форматтер устанавливается
        formatter = ListMachineInfoFormatter()
        self.finder.set_formatter(formatter)
        self.assertEqual(self.finder._formatter, formatter)

    def test_09_by_software_control(self):
        """Тест поиска по наличию системы управления"""
        # Поиск станков с определенной системой управления
        self.finder.find_by_software_control("CNC")
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_software_control.assert_called_once_with("CNC")
        self.mock_builder.execute.assert_called_once()

        # Поиск станков с разными системами управления
        self.finder.find_by_software_control(["CNC", "ЧПУ"])
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_software_control.assert_called_with(["CNC", "ЧПУ"])
        self.mock_builder.execute.assert_called()

        # Проверка с лимитом
        self.finder.find_by_software_control("CNC", limit=5)
        # Проверяем, что builder вызван с правильными параметрами
        self.mock_builder.filter_by_software_control.assert_called_with("CNC")
        self.mock_builder.limit.assert_called_once_with(5)
        self.mock_builder.execute.assert_called()


if __name__ == "__main__":
    unittest.main()
