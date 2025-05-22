#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, List, Optional, Union

from machine_tools.app.containers import FinderContainer
from machine_tools.app.schemas import MachineInfo, MachineUpdate
from machine_tools.app.updaters.utils import update_by_machine_info, update_by_machine_update


def find_names(substring: str) -> List[str]:
    """Запрашивает из БД список имен станков, соответствующих подстроке
    Args:
        substring: подстрока, по которой производится поиск
    Returns:
        список имен станков, соответствующих подстроке
    """
    container = FinderContainer()
    finder = container.finder_with_list_names()
    return finder.by_name(substring, exact_match=False)


def get_machine_info_by_name(name: str) -> Optional[MachineInfo]:
    """Запрашивает из БД информацию о станке по его имени
    Args:
        name: имя станка
    Returns:
        информация о станке, если она найдена, иначе None
    """
    container = FinderContainer()
    finder = container.finder_with_list_info()
    result = finder.by_name(name, exact_match=True)
    if len(result) > 0:
        return result[0]
    else:
        return None


def _dict_to_machine_update(machine_info: dict) -> MachineUpdate:
    """
    Преобразует словарь в объект MachineUpdate.

    Args:
        machine_info (MachineInfo): Объект информации о станке.

    Returns:
        dict: Словарь с данными станка.
    """
    return MachineUpdate(
        name=machine_info['name'],
        group=machine_info['group'],
        type=machine_info['type'],
        power=machine_info['power'],
        efficiency=machine_info['efficiency'],
        accuracy=machine_info['accuracy'],
        automation=machine_info['automation'],
        specialization=machine_info['specialization'],
        weight=machine_info['weight'],
        weight_class=machine_info['weight_class'],
        machine_type=machine_info['machine_type'],
        dimensions=machine_info['dimensions'],
        location=machine_info['location'],
        technical_requirements=machine_info['technical_requirements'],
    )


def update(info: Union[MachineInfo, MachineUpdate, Dict[str, Any]]) -> bool:
    """Обновляет информацию о станке в БД
    Args:
        info: MachineInfo или MachineUpdate - информация о станке
    Returns:
        bool: True, если обновление прошло успешно, False - иначе
    """
    if isinstance(info, MachineInfo):
        return update_by_machine_info(info)
    elif isinstance(info, MachineUpdate):
        return update_by_machine_update(info)
    elif isinstance(info, dict):
        info = _dict_to_machine_update(info)
        return update_by_machine_update(info)
    else:
        raise ValueError("info должен быть экземпляром MachineInfo или MachineUpdate")


if __name__ == "__main__":
    print(find_names("16К20"))
    machine = get_machine_info_by_name("16К20")
    print(machine)
    machine.power = 20
    update(machine)
    machine = get_machine_info_by_name("16К20")
    print(machine)
