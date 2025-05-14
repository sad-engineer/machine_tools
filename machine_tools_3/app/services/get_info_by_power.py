#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.db.session import get_session


def get_machines_by_power(
    min_power: float = None, 
    max_power: float = None,
    power: float = None
) -> List[str]:
    """
    Получает список имен станков по мощности.
    
    Args:
        min_power (float, optional): Минимальная мощность в кВт
        max_power (float, optional): Максимальная мощность в кВт
        power (float, optional): Точная мощность в кВт
        
    Returns:
        List[str]: Список имен станков по указанным критериям мощности
    """
    session = get_session()
    try:
        query = session.query(Machine.name)
        
        if power is not None:
            # Поиск по точному соответствию
            query = query.filter(Machine.power == power)
        else:
            # Поиск по диапазону
            if min_power is not None:
                query = query.filter(Machine.power >= min_power)
            if max_power is not None:
                query = query.filter(Machine.power <= max_power)
            
        machines = query.all()
        return [machine[0] for machine in machines]
        
    finally:
        session.close()


if __name__ == "__main__":
    # Примеры запросов:
    print("Станки мощностью до 10 кВт:")
    print(get_machines_by_power(max_power=10))
    
    print("\nСтанки мощностью от 5 до 15 кВт:")
    print(get_machines_by_power(min_power=5, max_power=15))
    
    print("\nСтанки мощностью от 20 кВт:")
    print(get_machines_by_power(min_power=20))

    print("\nСтанки мощностью 0,75 кВт:")
    print(get_machines_by_power(power=0.75))
