#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from machine_tools.app.models.machine import Base, Machine


class TestMachine(unittest.TestCase):
    """Тесты для модели Machine"""

    @classmethod
    def setUpClass(cls):
        """Подготовка тестового окружения"""

        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    def setUp(self):
        """Подготовка к каждому тесту"""

        self.session.rollback()

        self.session.query(Machine).delete()
        self.session.commit()

    def test_01_create_machine(self):
        """Тест создания станка"""

        machine = Machine(
            name="16К20",
            group=1,
            type=1,
            power=10.0,
            efficiency=0.85,
            accuracy="Н",
            automation="Автомат",
            software_control="ЧПУ",
            specialization="Универсальный",
            weight=2000.0,
            weight_class="Средний",
            length=2000,
            width=1000,
            height=1500,
            overall_diameter="2000x1000x1500",
            city="Москва",
            manufacturer="Завод им. Орджоникидзе",
            machine_type="Токарный",
        )

        self.session.add(machine)
        self.session.commit()

        saved_machine = self.session.query(Machine).filter_by(name="16К20").first()

        self.assertEqual(saved_machine.name, "16К20")
        self.assertEqual(saved_machine.group, 1)
        self.assertEqual(saved_machine.type, 1)
        self.assertEqual(saved_machine.power, 10.0)
        self.assertEqual(saved_machine.efficiency, 0.85)
        self.assertEqual(saved_machine.accuracy, "Н")
        self.assertEqual(saved_machine.automation, "Автомат")
        self.assertEqual(saved_machine.software_control, "ЧПУ")
        self.assertEqual(saved_machine.specialization, "Универсальный")
        self.assertEqual(saved_machine.weight, 2000.0)
        self.assertEqual(saved_machine.weight_class, "Средний")
        self.assertEqual(saved_machine.length, 2000)
        self.assertEqual(saved_machine.width, 1000)
        self.assertEqual(saved_machine.height, 1500)
        self.assertEqual(saved_machine.overall_diameter, "2000x1000x1500")
        self.assertEqual(saved_machine.city, "Москва")
        self.assertEqual(saved_machine.manufacturer, "Завод им. Орджоникидзе")
        self.assertEqual(saved_machine.machine_type, "Токарный")

    def test_02_unique_name_constraint(self):
        """Тест ограничения уникальности имени"""

        machine1 = Machine(name="16К20")
        self.session.add(machine1)
        self.session.commit()

        machine2 = Machine(name="16К20")
        self.session.add(machine2)

        with self.assertRaises(Exception):
            self.session.commit()

    def test_03_not_null_name_constraint(self):
        """Тест ограничения NOT NULL для имени"""

        machine = Machine()
        self.session.add(machine)

        with self.assertRaises(Exception):
            self.session.commit()

    def test_04_default_timestamps(self):
        """Тест значений по умолчанию для временных меток"""

        machine = Machine(name="16К20")
        self.session.add(machine)
        self.session.commit()

        self.assertIsNotNone(machine.created_at)
        self.assertIsNotNone(machine.updated_at)
        self.assertIsInstance(machine.created_at, datetime)
        self.assertIsInstance(machine.updated_at, datetime)

    def test_05_relationship_technical_requirements(self):
        """Тест связи с техническими требованиями"""

        machine = Machine(name="16К20")
        self.session.add(machine)
        self.session.commit()

        self.assertIsNotNone(machine.technical_requirements)
        self.assertEqual(len(machine.technical_requirements), 0)

    def test_06_update_timestamp(self):
        """Тест обновления временной метки"""

        machine = Machine(name="16К20")
        self.session.add(machine)
        self.session.commit()

        created_at = machine.created_at
        updated_at = machine.updated_at

        machine.power = 15.0
        self.session.commit()

        self.assertEqual(machine.created_at, created_at)
        self.assertGreater(machine.updated_at, updated_at)


if __name__ == "__main__":
    unittest.main()
