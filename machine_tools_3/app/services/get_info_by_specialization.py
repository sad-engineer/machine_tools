#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.db.session import get_session


def get_machines_by_specialization(specialization: str) -> List[str]:
    """
    Получает список имен станков по специализации.
    
    Args:
        specialization (str): Специализация станка (например, "Универсальный", "Специализированный", "Специальный")
        
    Returns:
        List[str]: Список имен станков указанной специализации
    """
    session = get_session()
    try:
        # Получаем только имена станков указанной специализации
        machines = session.query(Machine.name).filter(Machine.specialization == specialization).all()
        return [machine[0] for machine in machines]
        
    finally:
        session.close()


if __name__ == "__main__":
    # Примеры специализаций:
    # Универсальный - для широкого круга работ
    # Специализированный - для определенного вида работ
    # Специальный - для конкретной операции
    
    print("Универсальные станки:")
    print(get_machines_by_specialization("Универсальный"))
    
    print("\nСпециализированные станки:")
    print(get_machines_by_specialization("Специализированный"))
    
    print("\nСпециальные станки:")
    print(get_machines_by_specialization("Специальный"))
