#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from machine_tools.app.db.query_builder import QueryBuilder
from machine_tools.app.db.session_manager import session_manager
from machine_tools.app.schemas.machine import MachineUpdate


class MachineUpdater:
    """
    Класс для обновления данных станков в базе данных.
    """

    def __init__(self, session: Optional[Session] = None):
        """
        Инициализация обновлятора.

        Args:
            session (Session, optional): Сессия БД. Если не указана, будет создана новая.
        """
        self.session: Session = session or session_manager.get_session()
        self._builder: QueryBuilder = QueryBuilder(self.session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            session_manager.close_session()

    def update_by_id(self, machine_id: int, update_data: Union[MachineUpdate, Dict[str, Any]]) -> bool:
        """
        Обновляет данные станка по его ID.

        Args:
            machine_id (int): ID станка для обновления
            update_data (Union[MachineUpdate, Dict[str, Any]]): Данные для обновления

        Returns:
            bool: True если обновление прошло успешно, False если станок не найден
        """
        if isinstance(update_data, dict):
            update_data = MachineUpdate(**update_data)

        builder = self._builder.filter_by_id(machine_id)
        result = builder.update(update_data.model_dump(exclude_unset=True))
        return result > 0

    def update_by_name(
        self,
        name: str,
        update_data: Dict[str, Any],
        case_sensitive: bool = True,
        exact_match: bool = True,
    ) -> int:
        """
        Обновляет данные станков по имени.

        Args:
            name (str): Имя станка для поиска
            update_data Dict[str, Any]: Данные для обновления
            case_sensitive (bool, optional): Учитывать регистр. По умолчанию True
            exact_match (bool, optional): Точное совпадение. По умолчанию True

        Returns:
            int: Количество обновленных станков
        """
        builder = self._builder.filter_by_name(name, case_sensitive, exact_match)
        return builder.update(update_data)

    def update_by_power(
        self,
        update_data: Union[MachineUpdate, Dict[str, Any]],
        min_power: float = None,
        max_power: float = None,
    ) -> int:
        """
        Обновляет данные станков по диапазону мощности.

        Args:
            update_data (Union[MachineUpdate, Dict[str, Any]]): Данные для обновления
            min_power (float, optional): Минимальная мощность
            max_power (float, optional): Максимальная мощность

        Returns:
            int: Количество обновленных станков
        """
        if isinstance(update_data, dict):
            update_data = MachineUpdate(**update_data)

        builder = self._builder.filter_by_power(min_power=min_power, max_power=max_power)
        return builder.update(update_data.model_dump(exclude_unset=True))

    def update_by_efficiency(
        self,
        update_data: Union[MachineUpdate, Dict[str, Any]],
        min_efficiency: float = None,
        max_efficiency: float = None,
    ) -> int:
        """
        Обновляет данные станков по диапазону КПД.

        Args:
            update_data (Union[MachineUpdate, Dict[str, Any]]): Данные для обновления
            min_efficiency (float, optional): Минимальный КПД
            max_efficiency (float, optional): Максимальный КПД

        Returns:
            int: Количество обновленных станков
        """
        if isinstance(update_data, dict):
            update_data = MachineUpdate(**update_data)

        builder = self._builder.filter_by_efficiency(min_efficiency=min_efficiency, max_efficiency=max_efficiency)
        return builder.update(update_data.model_dump(exclude_unset=True))

    def update_by_accuracy(
        self,
        update_data: Union[MachineUpdate, Dict[str, Any]],
        accuracy: str,
    ) -> int:
        """
        Обновляет данные станков по классу точности.

        Args:
            update_data (Union[MachineUpdate, Dict[str, Any]]): Данные для обновления
            accuracy (str): Класс точности

        Returns:
            int: Количество обновленных станков
        """
        if isinstance(update_data, dict):
            update_data = MachineUpdate(**update_data)

        builder = self._builder.filter_by_accuracy(accuracy)
        return builder.update(update_data.model_dump(exclude_unset=True))

    def update_by_automation(
        self,
        update_data: Union[MachineUpdate, Dict[str, Any]],
        automation: str,
    ) -> int:
        """
        Обновляет данные станков по уровню автоматизации.

        Args:
            update_data (Union[MachineUpdate, Dict[str, Any]]): Данные для обновления
            automation (str): Уровень автоматизации

        Returns:
            int: Количество обновленных станков
        """
        if isinstance(update_data, dict):
            update_data = MachineUpdate(**update_data)

        builder = self._builder.filter_by_automation(automation)
        return builder.update(update_data.model_dump(exclude_unset=True))

    def update_by_specialization(
        self,
        update_data: Union[MachineUpdate, Dict[str, Any]],
        specialization: str,
    ) -> int:
        """
        Обновляет данные станков по специализации.

        Args:
            update_data (Union[MachineUpdate, Dict[str, Any]]): Данные для обновления
            specialization (str): Специализация

        Returns:
            int: Количество обновленных станков
        """
        if isinstance(update_data, dict):
            update_data = MachineUpdate(**update_data)

        builder = self._builder.filter_by_specialization(specialization)
        return builder.update(update_data.model_dump(exclude_unset=True))


# Пример использования:
if __name__ == "__main__":
    # Использование как контекстный менеджер
    with MachineUpdater() as updater:
        # Обновление станка по ID
        success = updater.update_by_id(
            1,
            {
                "power": 15.0,
                "efficiency": 0.85,
            },
        )
        print(f"Обновление по ID: {'успешно' if success else 'не найдено'}")

        # Обновление станков по имени
        updated_count = updater.update_by_name(
            "16К20",
            {
                "weight": 2000,
                "weight_class": "HEAVY",
            },
            exact_match=True,
        )
        print(f"Обновлено станков по имени: {updated_count}")

        # Обновление станков по мощности
        updated_count = updater.update_by_power(
            {
                "automation": "SEMI_AUTO",
            },
            min_power=10.0,
            max_power=20.0,
        )
        print(f"Обновлено станков по мощности: {updated_count}")
