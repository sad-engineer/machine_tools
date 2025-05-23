#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from machine_tools.app.db.query_builder import QueryBuilder
from machine_tools.app.models import Base, Machine


class TestQueryBuilder(unittest.TestCase):
    """Тесты для QueryBuilder"""

    @classmethod
    def setUpClass(cls):
        """Подготовка тестовой БД"""
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом"""
        # Очищаем все таблицы перед каждым тестом
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        
        self.session = self.Session()
        self.machines = [
            Machine(
                name="Станок1",
                group=1,
                type=1,
                power=10.0,
                efficiency=0.8,
                accuracy="A",
                automation="Автомат",
                specialization="Универсальный",
            ),
            Machine(
                name="Станок2",
                group=1,
                type=2,
                power=15.0,
                efficiency=0.7,
                accuracy="B",
                automation="Полуавтомат",
                specialization="Специализированный",
            ),
            Machine(
                name="Станок3",
                group=2,
                type=1,
                power=20.0,
                efficiency=0.9,
                accuracy="A",
                automation="Автомат",
                specialization="Универсальный",
            ),
        ]
        self.session.add_all(self.machines)
        self.session.commit()

    def tearDown(self):
        """Очистка после каждого теста"""
        self.session.close()
        # Очищаем все таблицы после каждого теста
        Base.metadata.drop_all(self.engine)

    @classmethod
    def tearDownClass(cls):
        """Очистка БД после всех тестов"""
        Base.metadata.drop_all(cls.engine)

    def test_01_filter_by_group(self):
        """Тест фильтрации по группе"""
        builder = QueryBuilder(self.session)
        result = builder.filter_by_group(1).execute()
        self.assertEqual(len(result), 2)
        self.assertTrue(all(machine.group == 1 for machine in result))

    def test_02_filter_by_type(self):
        """Тест фильтрации по типу"""
        builder = QueryBuilder(self.session)
        result = builder.filter_by_type(1).execute()
        self.assertEqual(len(result), 2)
        self.assertTrue(all(machine.type == 1 for machine in result))

    def test_03_filter_by_power(self):
        """Тест фильтрации по мощности"""
        builder = QueryBuilder(self.session)
        result = builder.filter_by_power(min_power=15.0, max_power=20.0).execute()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].power, 15.0)
        self.assertEqual(result[1].power, 20.0)

    def test_04_filter_by_efficiency(self):
        """Тест фильтрации по КПД"""
        builder = QueryBuilder(self.session)
        result = builder.filter_by_efficiency(min_efficiency=0.8).execute()
        self.assertEqual(len(result), 2)
        self.assertTrue(all(machine.efficiency >= 0.6 for machine in result))

    def test_05_filter_by_accuracy(self):
        """Тест фильтрации по точности"""
        builder = QueryBuilder(self.session)
        result = builder.filter_by_accuracy("A").execute()
        self.assertEqual(len(result), 2)
        self.assertTrue(all(machine.accuracy == "A" for machine in result))

    def test_06_filter_by_automation(self):
        """Тест фильтрации по автоматизации"""
        builder = QueryBuilder(self.session)
        result = builder.filter_by_automation("Автомат").execute()
        self.assertEqual(len(result), 2)
        self.assertTrue(all(machine.automation == "Автомат" for machine in result))

    def test_07_filter_by_specialization(self):
        """Тест фильтрации по специализации"""
        builder = QueryBuilder(self.session)
        result = builder.filter_by_specialization("Универсальный").execute()
        self.assertEqual(len(result), 2)
        self.assertTrue(all(machine.specialization == "Универсальный" for machine in result))

    def test_08_filter_by_name(self):
        """Тест фильтрации по имени"""
        builder = QueryBuilder(self.session)
        result = builder.filter_by_name("Станок1").execute()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Станок1")

    def test_09_filter_by_name_case_insensitive(self):
        """Тест фильтрации по имени без учета регистра"""
        builder = QueryBuilder(self.session)
        result = builder.filter_by_name("Станок", case_sensitive=False).execute()
        self.assertEqual(len(result), 3)

    def test_10_order_by(self):
        """Тест сортировки"""
        builder = QueryBuilder(self.session)
        result = builder.order_by("power", descending=True).execute()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].power, 20.0)
        self.assertEqual(result[1].power, 15.0)
        self.assertEqual(result[2].power, 10.0)

    def test_11_limit(self):
        """Тест ограничения количества результатов"""
        builder = QueryBuilder(self.session)
        result = builder.limit(2).execute()
        self.assertEqual(len(result), 2)

    def test_12_offset(self):
        """Тест смещения результатов"""
        builder = QueryBuilder(self.session)
        result = builder.offset(1).limit(1).execute()
        self.assertEqual(len(result), 1)

    def test_13_get_unique_values(self):
        """Тест получения уникальных значений"""
        builder = QueryBuilder(self.session)
        result = builder.get_unique_values("power")
        self.assertEqual(len(result), 3)
        self.assertEqual(set(result), {10.0, 15.0, 20.0})

    def test_14_complex_query(self):
        """Тест сложного запроса с несколькими условиями"""
        builder = QueryBuilder(self.session)
        result = (
            builder.filter_by_group(1)
            .filter_by_power(min_power=10.0, max_power=15.0)
            .filter_by_efficiency(min_efficiency=0.7)
            .order_by("power", descending=True)
            .limit(1)
            .execute()
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Станок2")


if __name__ == "__main__":
    unittest.main() 