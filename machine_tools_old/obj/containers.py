#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dependency_injector import containers, providers
from service_for_my_projects import Requester as RequesterContainer

from machine_tools_old.obj.constants import DEFAULT_SETTINGS_FOR_DB
from machine_tools_old.obj.creators import MachineToolsCreator
from machine_tools_old.obj.entities import MachineTool
from machine_tools_old.obj.finders import MachineToolsFinder
from machine_tools_old.obj.listers import MachineToolsLister


class MachineToolsContainer(containers.DeclarativeContainer):
    default_settings = providers.Object({"for_machine_tools": DEFAULT_SETTINGS_FOR_DB})
    config = providers.Configuration()
    config.from_dict(default_settings())

    container_for_DB = providers.Container(
        RequesterContainer,
        config=config.for_machine_tools,
    )

    finder = providers.Factory(
        MachineToolsFinder,
        record_requester=container_for_DB.requester.provider,
    )

    creator = providers.Factory(MachineToolsCreator, finder_provider=finder.provider)

    lister = providers.Factory(
        MachineToolsLister,
        creator_provider=creator.provider,
        finder_provider=finder.provider,
    )

    machine_tool = providers.Factory(MachineTool)
