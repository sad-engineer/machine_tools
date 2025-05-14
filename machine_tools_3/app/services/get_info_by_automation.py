#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.db.session import get_session


def get_machines_by_automation(automation: str) -> List[str]:
    """
    Получает список имен станков по уровню автоматизации.
    
    Args:
        automation (str): Уровень автоматизации (например, "Автоматизированный", "Ручной")
        
    Returns:
        List[str]: Список имен станков с указанным уровнем автоматизации
    """
    session = get_session()
    try:
        # Получаем только имена станков с указанным уровнем автоматизации
        machines = session.query(Machine.name).filter(Machine.automation == automation).all()
        return [machine[0] for machine in machines]
        
    finally:
        session.close()


if __name__ == "__main__":
    # Примеры уровней автоматизации:
    # - "Автомат"
    # - "Ручной"
    # - "Полуавтомат"
    print("Автоматизированные станки:")
    print(get_machines_by_automation("Автомат"))
    
    print("\nРучные станки:")
    print(get_machines_by_automation("Ручной"))
