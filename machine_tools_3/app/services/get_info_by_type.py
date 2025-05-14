#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.db.session import get_session


def get_machines_by_type(type_value: float) -> List[str]:
    """
    Получает список имен станков по типу.
    
    Args:
        type_value (float): Тип станка (от 0 до 9)
        
    Returns:
        List[str]: Список имен станков указанного типа
    """
    session = get_session()
    try:
        # Получаем только имена станков указанного типа
        machines = session.query(Machine.name).filter(Machine.type == type_value).all()
        return [machine[0] for machine in machines]
        
    finally:
        session.close()


if __name__ == "__main__":
    print(get_machines_by_type(1))
