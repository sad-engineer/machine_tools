#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Optional

from sqlalchemy.orm import Session

from machine_tools_2.app.models.machine import Machine, ProcessingType
from machine_tools_2.app.schemas.machine import MachineCreate, MachineUpdate


class MachineRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, machine_id: int) -> Optional[Machine]:
        return self.db.query(Machine).filter(Machine.id == machine_id).first()

    def get_by_name(self, name: str) -> Optional[Machine]:
        return self.db.query(Machine).filter(Machine.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Machine]:
        return self.db.query(Machine).offset(skip).limit(limit).all()

    def get_by_processing_type(self, processing_type: ProcessingType) -> List[Machine]:
        return (
            self.db.query(Machine)
            .filter(Machine.processing_type == processing_type)
            .all()
        )

    def create(self, machine: MachineCreate) -> Machine:
        db_machine = Machine(**machine.model_dump())
        self.db.add(db_machine)
        self.db.commit()
        self.db.refresh(db_machine)
        return db_machine

    def update(self, machine_id: int, machine: MachineUpdate) -> Optional[Machine]:
        db_machine = self.get(machine_id)
        if not db_machine:
            return None

        update_data = machine.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_machine, field, value)

        self.db.commit()
        self.db.refresh(db_machine)
        return db_machine

    def delete(self, machine_id: int) -> bool:
        db_machine = self.get(machine_id)
        if not db_machine:
            return False

        self.db.delete(db_machine)
        self.db.commit()
        return True
