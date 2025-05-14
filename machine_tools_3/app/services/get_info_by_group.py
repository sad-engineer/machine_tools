#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.db.session import get_session


def get_machines_by_group(group: float) -> List[str]:
    """
    Получает список имен станков по группе.
    
    Args:
        group (float): Группа станка (от 0 до 9)
        
    Returns:
        List[str]: Список имен станков указанной группы
    """
    session = get_session()
    try:
        # Получаем только имена станков указанной группы
        machines = session.query(Machine.name).filter(Machine.group == group).all()
        return [machine[0] for machine in machines]
        
    finally:
        session.close()


if __name__ == "__main__":
    # Уникальные группы станков:
    # [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    print(get_machines_by_group(1))
