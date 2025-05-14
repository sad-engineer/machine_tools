#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Optional

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.models.technical_requirement import TechnicalRequirement
from machine_tools_3.app.db.session import get_session
from machine_tools_3.app.schemas.machine import MachineInfo


def get_machines_by_group_and_type(group: float, type_value: float) -> List[MachineInfo]:
    """
    Получает список станков по группе и типу.
    
    Args:
        group (float): Группа станка (от 0 до 9)
        type_value (float): Тип станка (от 0 до 9)
        
    Returns:
        List[MachineInfo]: Список станков указанной группы и типа
    """
    session = get_session()
    try:
        # Получаем станки указанной группы и типа
        machines = session.query(Machine).filter(
            Machine.group == group,
            Machine.type == type_value
        ).all()
        
        result = []
        for machine in machines:
            # Получаем технические требования
            requirements = session.query(TechnicalRequirement).filter(
                TechnicalRequirement.machine_name == machine.name
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
            result.append(machine_info)
            
        return result
        
    finally:
        session.close()


if __name__ == "__main__":
    machines = get_machines_by_group_and_type(1, 1)
    for machine in machines:
        print(f"\nСтанок: {machine.name}")
        print(f"Тип: {machine.machine_type}")
        print(f"Мощность: {machine.power} кВт")
        print(f"Точность: {machine.accuracy}")
        print(f"Автоматизация: {machine.automation}")
        
        if machine.dimensions:
            print("\nГабариты:")
            print(f"Длина: {machine.dimensions.length} мм")
            print(f"Ширина: {machine.dimensions.width} мм")
            print(f"Высота: {machine.dimensions.height} мм")
        
        if machine.technical_requirements:
            print("\nТехнические требования:")
            for req, value in machine.technical_requirements.items():
                print(f"{req}: {value}")
        print("-" * 50) 