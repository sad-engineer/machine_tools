#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.db.session import get_session


def get_machines_by_accuracy(accuracy: str) -> List[str]:
    """
    Получает список имен станков по классу точности.
    
    Args:
        accuracy (str): Класс точности станка (например, "Н", "П", "В", "А", "С")
        
    Returns:
        List[str]: Список имен станков указанного класса точности
    """
    session = get_session()
    try:
        # Получаем только имена станков указанного класса точности
        machines = session.query(Machine.name).filter(Machine.accuracy == accuracy).all()
        return [machine[0] for machine in machines]
        
    finally:
        session.close()


if __name__ == "__main__":
    # Примеры классов точности:
    # Н - нормальная точность
    # П - повышенная точность
    # В - высокая точность
    # А - особо высокая точность
    # С - особо точные станки
    
    print("Станки нормальной точности (Н):")
    print(get_machines_by_accuracy("Н"))
    
    print("\nСтанки повышенной точности (П):")
    print(get_machines_by_accuracy("П"))
    
    print("\nСтанки высокой точности (В):")
    print(get_machines_by_accuracy("В"))
    
    print("\nСтанки особо высокой точности (А):")
    print(get_machines_by_accuracy("А"))
    
    print("\nСтанки особо точные (С):")
    print(get_machines_by_accuracy("С"))
