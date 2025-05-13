#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Optional

from sqlalchemy.orm import Session

from machine_tools_2.app.models.machine import MachineType, PlaningMachineType
from machine_tools_2.app.repositories.machine import MachineRepository
from machine_tools_2.app.schemas.machine import (Machine, MachineCreate,
                                                 MachineUpdate)


class MachineService:
    def __init__(self, db: Session):
        self.repository = MachineRepository(db)

    def get_machine(self, machine_id: int) -> Optional[Machine]:
        """Получить станок по ID"""
        db_machine = self.repository.get(machine_id)
        if not db_machine:
            return None
        return Machine.model_validate(db_machine)

    def get_machine_by_name(self, name: str) -> Optional[Machine]:
        """Получить станок по названию"""
        db_machine = self.repository.get_by_name(name)
        if not db_machine:
            return None
        return Machine.model_validate(db_machine)

    def get_machines(self, skip: int = 0, limit: int = 100) -> List[Machine]:
        """Получить список станков с пагинацией"""
        db_machines = self.repository.get_all(skip=skip, limit=limit)
        return [Machine.model_validate(machine) for machine in db_machines]

    def get_machines_by_type(self, machine_type: MachineType) -> List[Machine]:
        """Получить станки по типу"""
        db_machines = self.repository.get_by_machine_type(machine_type)
        return [Machine.model_validate(machine) for machine in db_machines]

    def get_machines_by_planing_type(
        self, planing_type: PlaningMachineType
    ) -> List[Machine]:
        """Получить строгальные станки по типу"""
        db_machines = self.repository.get_by_planing_type(planing_type)
        return [Machine.model_validate(machine) for machine in db_machines]

    def create_machine(self, machine: MachineCreate) -> Machine:
        """Создать новый станок"""
        db_machine = self.repository.create(machine)
        return Machine.model_validate(db_machine)

    def update_machine(
        self, machine_id: int, machine: MachineUpdate
    ) -> Optional[Machine]:
        """Обновить существующий станок"""
        db_machine = self.repository.update(machine_id, machine)
        if not db_machine:
            return None
        return Machine.model_validate(db_machine)

    def delete_machine(self, machine_id: int) -> bool:
        """Удалить станок"""
        return self.repository.delete(machine_id)

    def get_machines_by_characteristics(
        self,
        min_power: Optional[float] = None,
        max_power: Optional[float] = None,
        min_weight: Optional[float] = None,
        max_weight: Optional[float] = None,
        automation_type: Optional[str] = None,
    ) -> List[Machine]:
        """Получить станки по характеристикам"""
        db_machines = self.repository.get_by_characteristics(
            min_power=min_power,
            max_power=max_power,
            min_weight=min_weight,
            max_weight=max_weight,
            automation_type=automation_type,
        )
        return [Machine.model_validate(machine) for machine in db_machines]
