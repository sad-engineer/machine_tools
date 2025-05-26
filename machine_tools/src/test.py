#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools import Automation, ListMachineInfoFormatter, SoftwareControl, find_names
from machine_tools.app.finders import MachineFinder
from machine_tools.app.updaters.updater import MachineUpdater


def update_software_control():
    # with MachineUpdater() as updater:
    #     updated_count = updater.update_by_software_control(
    #         {
    #             "software_control": SoftwareControl.NO.value,
    #         },
    #         software_control=None,
    #     )
    #     print(f"Обновлено станков по наличию системы управления: {updated_count}")

    names = []
    with MachineFinder(limit=None) as finder:
        names = finder.by_name("Ф4", exact_match=False)

    names_for_update = [name for name in names if name.endswith("Ф4")]
    names_for_no_update = [name for name in names if name.endswith("Ф4") == False]

    print(f"names_for_update: {names_for_update}")
    print(f"names_for_no_update: {names_for_no_update}")

    # Создаем временные списки для перемещения элементов
    to_move = []

    for name in names_for_no_update:
        with MachineFinder(limit=None, formatter=ListMachineInfoFormatter()) as finder_with_info:
            machine = finder_with_info.by_name(name, exact_match=True)[0]
            if machine.machine_type.find("ЧПУ") != -1 and machine.software_control != SoftwareControl.CNC:
                to_move.append(name)
            else:
                if machine.software_control != SoftwareControl.CNC:
                    print(f"{machine.name}: {machine.machine_type}")

    # Перемещаем элементы после завершения итерации
    for name in to_move:
        names_for_no_update.remove(name)
        names_for_update.append(name)

    print(f"names_for_update: {names_for_update}")
    print(f"names_for_no_update: {names_for_no_update}")

    updated_count = 0
    # обновляем станки по имени
    for name in names_for_update:
        with MachineUpdater() as updater:
            count = updater.update_by_name(
                name,
                {
                    "software_control": SoftwareControl.CNC.value,
                },
                exact_match=True,
            )
            updated_count += count
    print(f"Обновлено станков по имени: {updated_count}")


if __name__ == "__main__":

    names = []
    with MachineFinder(limit=None) as finder:
        names.extend(finder.all())
    print(f"names: {names}")

    for name in names:
        with MachineFinder(limit=None, formatter=ListMachineInfoFormatter()) as finder_with_info:
            try:
                machine = finder_with_info.by_name(name, exact_match=True)[0]
                if machine.machine_type.find("втомат") == -1 and machine.automation != Automation.MANUAL:
                    print(f"machine.name: {machine.name}, machine.automation: {machine.automation}")
            except Exception as e:
                print(name)
