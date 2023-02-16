#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dependency_injector import containers, providers
from service import Requester as RequesterContainer

from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_DB
from machine_tools.obj.finders import Finder
from machine_tools.obj.entities import MachineTool


class Container(containers.DeclarativeContainer):
    default_settings = providers.Object(
        {'for_machine_tools': DEFAULT_SETTINGS_FOR_DB}
    )
    config = providers.Configuration()
    config.from_dict(default_settings())

    container_for_DB = providers.Container(
        RequesterContainer,
        config=config.for_machine_tools,
    )

    finder = providers.Factory(
        Finder,
        record_requester=container_for_DB.requester,
    )

    machine_tool = providers.Factory(
        MachineTool
    )



if __name__ == '__main__':
    print(DEFAULT_SETTINGS_FOR_DB)
    container = Container()
    print(container.config())

    container.config.from_dict(DEFAULT_SETTINGS_FOR_DB)
    finder = container.finder()
    print(finder.by_name("1К62"))

    available_values = finder.available_values
    print(available_values.keys())
    print(available_values['Тип'])

    machine_tool = container.machine_tool(name="16К20")
    print(machine_tool)

