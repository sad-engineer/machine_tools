#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools import get_finder_with_list_info

with get_finder_with_list_info() as finder:
    machines = finder.find_all()

    machines = finder.find_by_name(name="16К20Ф3", exact_match=True)
    if len(machines) == 1:
        machine_info = machines[0]
        if machine_info:
            print(f"Станок: {machine_info.name}")
            print(f"Тип: {machine_info.machine_type}")
            print(f"Мощность: {machine_info.power} кВт")
            print(f"Точность: {machine_info.accuracy.value}")
            print(f"Автоматизация: {machine_info.automation.value}")
            print("\nГабариты:")
            print(f"Длина: {machine_info.dimensions.length} мм")
            print(f"Ширина: {machine_info.dimensions.width} мм")
            print(f"Высота: {machine_info.dimensions.height} мм")
            print("\nТехнические требования:")
            for req, value in machine_info.technical_requirements.items():
                if value is not None:
                    print(f"{req}: {value}")
        else:
            print("Станок не найден")

    machines = finder.find_by_power(min_power=10.0, order_by_power=True, descending=True, limit=5)
    for machine in machines:
        print(f"{machine.name} - {machine.power}")


