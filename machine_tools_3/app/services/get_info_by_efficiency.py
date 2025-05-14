#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.db.session import get_session


def get_machines_by_efficiency(
    min_efficiency: float = None, 
    max_efficiency: float = None,
    efficiency: float = None
) -> List[str]:
    """
    Получает список имен станков по КПД.
    
    Args:
        min_efficiency (float, optional): Минимальный КПД (от 0 до 1)
        max_efficiency (float, optional): Максимальный КПД (от 0 до 1)
        efficiency (float, optional): Точное значение КПД (от 0 до 1)
        
    Returns:
        List[str]: Список имен станков по указанным критериям КПД
    """
    session = get_session()
    try:
        query = session.query(Machine.name)
        
        if efficiency is not None:
            # Поиск по точному соответствию
            query = query.filter(Machine.efficiency == efficiency)
        else:
            # Поиск по диапазону
            if min_efficiency is not None:
                query = query.filter(Machine.efficiency >= min_efficiency)
            if max_efficiency is not None:
                query = query.filter(Machine.efficiency <= max_efficiency)
            
        machines = query.all()
        return [machine[0] for machine in machines]
        
    finally:
        session.close()


if __name__ == "__main__":
    # Примеры запросов:
    print("Станки с КПД до 0.5:")
    print(get_machines_by_efficiency(max_efficiency=0.5))
    
    print("\nСтанки с КПД от 0.7 до 0.9:")
    print(get_machines_by_efficiency(min_efficiency=0.7, max_efficiency=0.9))
    
    print("\nСтанки с КПД от 0.8:")
    print(get_machines_by_efficiency(min_efficiency=0.8))

    print("\nСтанки с КПД 0.75:")
    print(get_machines_by_efficiency(efficiency=0.75))
