#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MachineBase(BaseModel):
    name: str
    group: Optional[float]
    type: Optional[float]
    power: Optional[float]
    efficiency: Optional[float]
    accuracy: Optional[str]
    automation: Optional[str]
    specialization: Optional[str]
    weight: Optional[float]
    weight_class: Optional[str]
    length: Optional[int]
    width: Optional[int]
    height: Optional[int]
    overall_diameter: Optional[str]
    city: Optional[str]
    manufacturer: Optional[str]
    machine_type: Optional[str]


class MachineCreate(MachineBase):
    pass


class MachineUpdate(MachineBase):
    pass


class MachineInDBBase(MachineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Machine(MachineInDBBase):
    pass
