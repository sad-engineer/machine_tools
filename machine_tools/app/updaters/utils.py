#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools.app.schemas import MachineInfo, MachineUpdate
from machine_tools.app.updaters.updater import MachineUpdater


def update_by_machine_update(info: MachineUpdate):
    """Обновляет информацию о станке в БД
    Args:
        info: MachineUpdate - информация о станке
    Returns:
        bool: True, если обновление прошло успешно, False - иначе
    """
    if not isinstance(info, MachineUpdate):
        raise ValueError("info должен быть экземпляром MachineUpdate")
    updater = MachineUpdater()
    updated_count = updater.update_by_name(info.name, info.get_flat_dict())
    if updated_count > 0:
        return True
    else:
        return False


def update_by_machine_info(info: MachineInfo):
    """Обновляет информацию о станке в БД
    Args:
        info: MachineInfo или Dict[str, Any] - информация о станке
    Returns:
        bool: True, если обновление прошло успешно, False - иначе
    """
    if not isinstance(info, MachineInfo):
        raise ValueError("info должен быть экземпляром MachineInfo или словарём")
    return update_by_machine_update(MachineUpdate(**info.model_dump()))
