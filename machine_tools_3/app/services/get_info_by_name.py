#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Optional

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.models.technical_requirement import TechnicalRequirement
from machine_tools_3.app.db.session import get_session
from machine_tools_3.app.schemas.machine import MachineInfo


def get_machines_by_name(machine_name: str) -> Optional[MachineInfo]:
    """
    Получает полную информацию о станке по его имени.
    
    Args:
        machine_name (str): Имя станка (например, "16К20")
        
    Returns:
        Optional[MachineInfo]: Объект с информацией о станке или None, если станок не найден
    """
    session = get_session()
    try:
        # Получаем основную информацию о станке
        machine = session.query(Machine).filter(Machine.name == machine_name).first()
        
        if not machine:
            return None
            
        # Получаем технические требования
        requirements = session.query(TechnicalRequirement).filter(
            TechnicalRequirement.machine_name == machine_name
        ).all()
        
        # Создаем объект с информацией о станке
        machine_info = MachineInfo(
            name=machine.name,
            group=machine.group,
            type=machine.type,
            power=machine.power,
            efficiency=machine.efficiency,
            accuracy=machine.accuracy,
            automation=machine.automation,
            specialization=machine.specialization,
            weight=machine.weight,
            weight_class=machine.weight_class,
            dimensions={
                "length": machine.length,
                "width": machine.width,
                "height": machine.height,
                "overall_diameter": machine.overall_diameter
            },
            location={
                "city": machine.city,
                "manufacturer": machine.manufacturer
            },
            machine_type=machine.machine_type,
            technical_requirements={
                req.requirement: req.value for req in requirements
            }
        )
        
        return machine_info
        
    finally:
        session.close()


if __name__ == "__main__":
    info = get_machines_by_name("16К20")
    if info:
        print(f"Станок: {info.name}")
        print(f"Тип: {info.machine_type}")
        print(f"Мощность: {info.power} кВт")
        print(f"Точность: {info.accuracy}")
        print(f"Автоматизация: {info.automation}")
        
        if info.dimensions:
            print("\nГабариты:")
            print(f"Длина: {info.dimensions.length} мм")
            print(f"Ширина: {info.dimensions.width} мм")
            print(f"Высота: {info.dimensions.height} мм")
        
        if info.technical_requirements:
            print("\nТехнические требования:")
            for req, value in info.technical_requirements.items():
                print(f"{req}: {value}")
    else:
        print("Станок не найден")

