#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.db.session import get_session


def get_all_machines() -> List[str]:
    """
    Получает список всех имен станков из базы данных.
    
    Returns:
        List[str]: Список имен всех станков
    """
    session = get_session()
    try:
        # Получаем только имена всех станков
        machines = session.query(Machine.name).all()
        return [machine[0] for machine in machines]
        
    finally:
        session.close()


if __name__ == "__main__":
    print(get_all_machines())
