#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dependency_injector import containers, providers

from machine_tools.app.db.session_manager import session_manager
from machine_tools.app.finders.finder import MachineFinder
from machine_tools.app.formatters import (
    DictMachineInfoFormatter,
    DictNameFormatter,
    IndexedMachineInfoFormatter,
    IndexedNameFormatter,
    ListMachineInfoFormatter,
    ListNameFormatter,
)


class FinderContainer(containers.DeclarativeContainer):
    """Контейнер для MachineFinder и его форматтеров"""

    # Провайдеры для форматтеров
    list_name_formatter = providers.Singleton(ListNameFormatter)
    list_machine_info_formatter = providers.Singleton(ListMachineInfoFormatter)
    dict_name_formatter = providers.Singleton(DictNameFormatter)
    dict_machine_info_formatter = providers.Singleton(DictMachineInfoFormatter)
    indexed_name_formatter = providers.Singleton(IndexedNameFormatter)
    indexed_machine_info_formatter = providers.Singleton(IndexedMachineInfoFormatter)

    # Провайдер для сессии БД
    session = providers.Singleton(session_manager.get_session)

    # Провайдер для MachineFinder с разными форматтерами
    finder_with_list_names = providers.Factory(
        MachineFinder,
        session=session,
        formatter=list_name_formatter,
    )

    finder_with_list_info = providers.Factory(
        MachineFinder,
        session=session,
        formatter=list_machine_info_formatter,
    )

    finder_with_dict_names = providers.Factory(
        MachineFinder,
        session=session,
        formatter=dict_name_formatter,
    )

    finder_with_dict_info = providers.Factory(
        MachineFinder,
        session=session,
        formatter=dict_machine_info_formatter,
    )

    finder_with_indexed_names = providers.Factory(
        MachineFinder,
        session=session,
        formatter=indexed_name_formatter,
    )

    finder_with_indexed_info = providers.Factory(
        MachineFinder,
        session=session,
        formatter=indexed_machine_info_formatter,
    )
