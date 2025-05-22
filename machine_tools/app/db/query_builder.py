#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict

from sqlalchemy import and_, asc, desc, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

from machine_tools.app.models import Machine, TechnicalRequirement


class QueryBuilder:
    """
    Класс для построения и управления запросами к БД.
    """

    def __init__(self, session: Session):
        self.session = session
        self._query = select(Machine)
        self._filters = []
        self._order_by = []
        self._limit = None
        self._offset = None

    def filter_by_id(self, machine_id: int) -> "QueryBuilder":
        """Фильтр по ID станка"""
        self._filters.append(Machine.id == machine_id)
        return self

    def filter_by_group(self, group: int) -> "QueryBuilder":
        """Фильтр по группе станка"""
        self._filters.append(Machine.group == group)
        return self

    def filter_by_type(self, type: int) -> "QueryBuilder":
        """Фильтр по типу станка"""
        self._filters.append(Machine.type == type)
        return self

    def filter_by_power(self, min_power: float = None, max_power: float = None) -> "QueryBuilder":
        """Фильтр по мощности"""
        if min_power is not None:
            self._filters.append(Machine.power >= min_power)
        if max_power is not None:
            self._filters.append(Machine.power <= max_power)
        return self

    def filter_by_efficiency(self, min_efficiency: float = None, max_efficiency: float = None) -> "QueryBuilder":
        """Фильтр по КПД"""
        if min_efficiency is not None:
            self._filters.append(Machine.efficiency >= min_efficiency)
        if max_efficiency is not None:
            self._filters.append(Machine.efficiency <= max_efficiency)
        return self

    def filter_by_accuracy(self, accuracy: str) -> "QueryBuilder":
        """Фильтр по классу точности"""
        self._filters.append(Machine.accuracy == accuracy)
        return self

    def filter_by_automation(self, automation: str) -> "QueryBuilder":
        """Фильтр по уровню автоматизации"""
        self._filters.append(Machine.automation == automation)
        return self

    def filter_by_specialization(self, specialization: str) -> "QueryBuilder":
        """Фильтр по специализации"""
        self._filters.append(Machine.specialization == specialization)
        return self

    def filter_by_name(self, name: str, case_sensitive: bool = False, exact_match: bool = False) -> "QueryBuilder":
        """Фильтр по имени станка

        Args:
            name (str): Имя станка для поиска
            case_sensitive (bool, optional): Учитывать регистр. По умолчанию False
            exact_match (bool, optional): Точное совпадение. По умолчанию False
        """
        if exact_match:
            if case_sensitive:
                self._filters.append(Machine.name == name)
            else:
                self._filters.append(Machine.name.ilike(name))
        else:
            if case_sensitive:
                self._filters.append(Machine.name.contains(name))
            else:
                self._filters.append(Machine.name.ilike(f"%{name}%"))
        return self

    def order_by(self, column: str, descending: bool = False) -> "QueryBuilder":
        """Сортировка по колонке"""
        column_obj = getattr(Machine, column, None)
        if column_obj is not None:
            self._order_by.append(desc(column_obj) if descending else asc(column_obj))
        return self

    def limit(self, limit: int) -> "QueryBuilder":
        """Ограничение количества результатов"""
        self._limit = limit
        return self

    def offset(self, offset: int) -> "QueryBuilder":
        """Смещение результатов"""
        self._offset = offset
        return self

    def build(self) -> Select:
        """Построение запроса"""
        # Применяем фильтры
        if self._filters:
            self._query = self._query.where(and_(*self._filters))

        # Применяем сортировку
        if self._order_by:
            self._query = self._query.order_by(*self._order_by)

        # Применяем лимит и смещение
        if self._limit is not None:
            self._query = self._query.limit(self._limit)
        if self._offset is not None:
            self._query = self._query.offset(self._offset)

        return self._query

    def execute(self) -> Any:
        """Выполнение запроса"""
        query = self.build()
        return self.session.execute(query).scalars().all()

    def update(self, update_data: Dict[str, Any]) -> int:
        """
        Обновление данных в БД.

        Args:
            update_data (Dict[str, Any]): Словарь с данными для обновления

        Returns:
            int: Количество обновленных записей
        """
        # Создаем запрос на обновление
        stmt = update(Machine)

        # Применяем фильтры
        if self._filters:
            stmt = stmt.where(and_(*self._filters))

        # Удаляем technical_requirements из данных обновления
        # так как это relationship, а не поле
        processed_data = {k: v for k, v in update_data.items() if k != 'technical_requirements'}

        # Применяем данные для обновления
        stmt = stmt.values(**processed_data)

        # Выполняем обновление
        result = self.session.execute(stmt)
        self.session.commit()

        # Если есть technical_requirements, обновляем их отдельно
        if 'technical_requirements' in update_data and update_data['technical_requirements']:
            machine_name = processed_data.get('name')
            if machine_name:
                # Удаляем старые требования
                self.session.query(TechnicalRequirement).filter(
                    TechnicalRequirement.machine_name == machine_name
                ).delete()

                # Добавляем новые требования
                for req_name, req_value in update_data['technical_requirements'].items():
                    requirement = TechnicalRequirement(
                        machine_name=machine_name,
                        requirement=req_name,
                        value=str(req_value) if req_value is not None else None,
                    )
                    self.session.add(requirement)
                self.session.commit()

        return result.rowcount

    def get_unique_values(self, column: str) -> Any:
        """Получение уникальных значений колонки"""
        column_obj = getattr(Machine, column, None)
        if column_obj is None:
            return []

        query = select(column_obj).distinct()
        if self._filters:
            query = query.where(and_(*self._filters))

        return self.session.execute(query).scalars().all()


# Пример использования:
if __name__ == "__main__":
    from machine_tools.app.db.session_manager import get_session

    session = get_session()
    try:
        # Создаем построитель запросов
        builder = QueryBuilder(session)

        # Пример сложного запроса
        machines = (
            builder.filter_by_group(1)
            .filter_by_power(min_power=0, max_power=20.0)
            .filter_by_efficiency(min_efficiency=0.5)
            .order_by("power", descending=True)
            .limit(10)
            .execute()
        )
        print([machine.name for machine in machines])

        # Получение уникальных значений
        unique_powers = builder.get_unique_values("power")
        print("Уникальные значения мощности:", unique_powers)

        # Пример обновления
        updated_count = builder.filter_by_name("16К20", exact_match=True).update({"power": 15.0, "efficiency": 0.85})
        print(f"Обновлено станков: {updated_count}")

    finally:
        session.close()
