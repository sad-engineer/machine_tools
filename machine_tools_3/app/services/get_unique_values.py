#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict, Any

from machine_tools_3.app.models.machine import Machine
from machine_tools_3.app.db.session import get_session


def get_unique_values() -> Dict[str, List[Any]]:
    """
    Получает уникальные значения из всех колонок таблицы станков.
    
    Returns:
        Dict[str, List[Any]]: Словарь с уникальными значениями по каждой колонке
    """
    session = get_session()
    try:
        # Получаем все уникальные значения для каждой колонки
        result = {
            "groups": [g[0] for g in session.query(Machine.group).distinct().all() if g[0] is not None],
            "types": [t[0] for t in session.query(Machine.type).distinct().all() if t[0] is not None],
            "powers": [p[0] for p in session.query(Machine.power).distinct().all() if p[0] is not None],
            "efficiencies": [e[0] for e in session.query(Machine.efficiency).distinct().all() if e[0] is not None],
            "accuracies": [a[0] for a in session.query(Machine.accuracy).distinct().all() if a[0] is not None],
            "automations": [a[0] for a in session.query(Machine.automation).distinct().all() if a[0] is not None],
            "specializations": [s[0] for s in session.query(Machine.specialization).distinct().all() if s[0] is not None],
            "weight_classes": [w[0] for w in session.query(Machine.weight_class).distinct().all() if w[0] is not None],
            "cities": [c[0] for c in session.query(Machine.city).distinct().all() if c[0] is not None],
            "manufacturers": [m[0] for m in session.query(Machine.manufacturer).distinct().all() if m[0] is not None],
            "machine_types": [mt[0] for mt in session.query(Machine.machine_type).distinct().all() if mt[0] is not None]
        }
        
        # Сортируем числовые значения
        for key in ["groups", "types", "powers", "efficiencies"]:
            result[key].sort()
            
        # Сортируем строковые значения
        for key in ["accuracies", "automations", "specializations", "weight_classes", 
                   "cities", "manufacturers", "machine_types"]:
            result[key].sort(key=lambda x: str(x).lower())
            
        return result
        
    finally:
        session.close()


if __name__ == "__main__":
    values = get_unique_values()
    
    print("Уникальные группы станков:")
    print(values["groups"])
    
    print("\nУникальные типы станков:")
    print(values["types"])
    
    print("\nУникальные значения мощности (кВт):")
    print(values["powers"])
    
    print("\nУникальные значения КПД:")
    print(values["efficiencies"])
    
    print("\nУникальные классы точности:")
    print(values["accuracies"])
    
    print("\nУникальные уровни автоматизации:")
    print(values["automations"])
    
    print("\nУникальные специализации:")
    print(values["specializations"])
    
    print("\nУникальные классы по массе:")
    print(values["weight_classes"])
    
    print("\nУникальные города производителей:")
    print(values["cities"])
    
    print("\nУникальные производители:")
    print(values["manufacturers"])
    
    print("\nУникальные типы станков:")
    print(values["machine_types"]) 