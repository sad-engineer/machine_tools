#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List, Optional, Union

from sqlalchemy.orm import Session

from machine_tools.app.db.query_builder import QueryBuilder
from machine_tools.app.db.session_manager import session_manager
from machine_tools.app.formatters import (
    ListMachineInfoFormatter,
    ListNameFormatter,
    MachineFormatter,
)


class MachineFinder:
    """
    Класс для поиска станков по различным критериям.
    """

    def __init__(
        self,
        session: Optional[Session] = None,
        limit: Optional[int] = None,
        formatter: Optional[MachineFormatter] = None,
    ):
        """
        Инициализация поисковика.

        Args:
            session (Session, optional): Сессия БД. Если не указана, будет создана новая.
            limit (int, optional): Глобальный лимит для всех запросов
            formatter (MachineFormatter, optional): Форматтер для результатов. По умолчанию ListNameFormatter
        """
        self.session: Session = session or session_manager.get_session()
        self._builder: QueryBuilder = QueryBuilder(self.session)
        self._global_limit: int = limit
        self._formatter: MachineFormatter = formatter or ListNameFormatter()

        if self._global_limit:
            self._builder.limit(self._global_limit)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            session_manager.close_session()

    def set_limit(self, limit: Optional[int]) -> "MachineFinder":
        """
        Устанавливает глобальный лимит для всех запросов.

        Args:
            limit (int, optional): Новое значение лимита. None для отключения лимита.

        Returns:
            MachineFinder: self для цепочки вызовов
        """
        self._global_limit = limit
        return self

    def get_limit(self) -> Optional[int]:
        """
        Возвращает текущее значение глобального лимита.

        Returns:
            Optional[int]: Текущее значение лимита
        """
        return self._global_limit

    def _apply_limit(self, limit: Optional[int] = None) -> "MachineFinder":
        """
        Применяет лимит к запросу.

        Args:
            limit (int, optional): Локальный лимит для текущего запроса

        Returns:
            MachineFinder: self для цепочки вызовов
        """
        # Используем локальный лимит, если он указан, иначе глобальный
        actual_limit = limit if limit is not None else self._global_limit
        if actual_limit is not None:
            self._builder.limit(actual_limit)
        return self

    def set_formatter(self, formatter: MachineFormatter) -> "MachineFinder":
        """
        Устанавливает форматтер для результатов запросов.

        Args:
            formatter (MachineFormatter): Экземпляр форматтера

        Returns:
            MachineFinder: self для цепочки вызовов
        """
        self._formatter = formatter
        return self

    def find_by_power(
        self,
        min_power: float = None,
        max_power: float = None,
        order_by_power: bool = False,
        descending: bool = False,
        limit: int = None,
    ) -> List[Any]:
        """Получение станков по мощности"""
        builder = self._builder.filter_by_power(min_power=min_power, max_power=max_power)

        if order_by_power:
            builder = builder.order_by("power", descending=descending)

        if limit:
            builder = builder.limit(limit)

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)

    def find_by_efficiency(
        self,
        min_efficiency: float = None,
        max_efficiency: float = None,
        order_by_efficiency: bool = False,
        descending: bool = False,
        limit: int = None,
    ) -> List[Any]:
        """Получение станков по КПД"""
        builder = self._builder.filter_by_efficiency(min_efficiency=min_efficiency, max_efficiency=max_efficiency)

        if order_by_efficiency:
            builder = builder.order_by("efficiency", descending=descending)

        if limit:
            builder = builder.limit(limit)

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)

    def find_by_accuracy(self, accuracy: Union[str, List[str]], limit: int = None) -> List[Any]:
        """Получение станков по классу точности"""
        builder = self._builder.filter_by_accuracy(accuracy)

        if limit:
            builder = builder.limit(limit)

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)

    def find_by_automation(self, automation: Union[str, List[str]], limit: int = None) -> List[Any]:
        """Получение станков по уровню автоматизации"""
        builder = self._builder.filter_by_automation(automation)

        if limit:
            builder = builder.limit(limit)

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)

    def find_by_specialization(self, specialization: Union[str, List[str]], limit: int = None) -> List[Any]:
        """Получение станков по специализации"""
        builder = self._builder.filter_by_specialization(specialization)

        if limit:
            builder = builder.limit(limit)

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)

    def find_by_name(
        self, name: str, case_sensitive: bool = False, exact_match: bool = True, limit: int = None
    ) -> List[Any]:
        """Поиск станков по имени

        Args:
            name (str): Имя станка для поиска
            case_sensitive (bool, optional): Учитывать регистр. По умолчанию False
            exact_match (bool, optional): Точное совпадение. По умолчанию True
            limit (int, optional): Ограничение количества результатов
        """
        builder = self._builder.filter_by_name(name=name, case_sensitive=case_sensitive, exact_match=exact_match)

        if limit:
            builder = builder.limit(limit)

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)

    def find_by_software_control(self, software_control: Union[str, List[str]], limit: int = None) -> List[Any]:
        """Получение станков по наличию системы управления"""
        builder = self._builder.filter_by_software_control(software_control)

        if limit:
            builder = builder.limit(limit)

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)

    def find_by_group(self, group: Union[int, List[int]], limit: int = None) -> List[Any]:
        """Получение станков по группе"""
        group = [str(g) for g in group] if isinstance(group, list) else str(group)
        builder = self._builder.filter_by_group(group)

        if limit:
            builder = builder.limit(limit)

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)
    
    def find_by_type(self, type: Union[int, List[int]], limit: int = None) -> List[Any]:
        """Получение станков по типу"""
        type = [str(t) for t in type] if isinstance(type, list) else str(type)
        builder = self._builder.filter_by_type(type)

        if limit:
            builder = builder.limit(limit)  

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)    

    def find_all(self, limit: int = None) -> List[Any]:
        """Получение всех станков"""
        builder = self._builder

        if limit:
            builder = builder.limit(limit)

        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)
    
    def reset_builder(self):
        """Сброс всех параметров поиска"""
        self._builder = QueryBuilder(self.session)
        self._builder.limit(self._global_limit)


# Пример использования:
if __name__ == "__main__":
    # Использование как контекстный менеджер
    with MachineFinder(limit=5) as finder:  # Устанавливаем глобальный лимит
        # Получение только имен станков (по умолчанию)
        powerful_machines = finder.find_by_power(min_power=10.0, order_by_power=True, descending=True)
        print("Топ-5 самых мощных станков (только имена):", powerful_machines)

        # Переключение на полную информацию
        finder.set_formatter(ListMachineInfoFormatter())
        efficient_machines = finder.find_by_efficiency(min_efficiency=0.5, order_by_efficiency=True, descending=True)
        print("\nСтанки с КПД > 50% (полная информация):")
        for machine in efficient_machines:
            print(f"- {machine.name}: мощность={machine.power}кВт, КПД={machine.efficiency}")

        # Возврат к именам
        finder.set_formatter(ListNameFormatter())
        print("\nВсе станки (только имена):", finder.find_all())

        finder.set_formatter(ListMachineInfoFormatter())
        machine = finder.find_by_name(name="16К20Ф3", exact_match=True)
        print(machine)

        print("Поиск по нескольким типам:", finder.find_by_type([0, 1, 2]))


    with MachineFinder() as finder:
        finder.set_formatter(ListMachineInfoFormatter())
        # получение информации о станках
        machines = finder.find_all()

        # получение информации о станке по имени
        machines = finder.find_by_name(name="16К20Ф3", exact_match=True)
        if len(machines) == 1:
            machine_info = machines[0]
            if machine_info:
                print(f"Станок: {machine_info.name}")
                print(f"Тип: {machine_info.machine_type}")
                print(f"Мощность: {machine_info.power} кВт")
                print(f"Точность: {machine_info.accuracy}")
                print(f"Автоматизация: {machine_info.automation}")
                print("\nГабариты:")
                print(f"Длина: {machine_info.dimensions.length} мм")
                print(f"Ширина: {machine_info.dimensions.width} мм")
                print(f"Высота: {machine_info.dimensions.height} мм")
                print("\nТехнические требования:")
                for req, value in machine_info.technical_requirements.items():
                    print(f"{req}: {value}")
            else:
                print("Станок не найден")

        #  Поддерживает все фильтрации и сортировки
        machines = finder.find_by_power(min_power=10.0, order_by_power=True, descending=True)
        print(machines)
        