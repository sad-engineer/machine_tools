#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dependency_injector import containers, providers
from service import Requester as RequesterContainer

from machine_tools.obj.constants import DEFAULT_SETTINGS_FOR_DB
from machine_tools.obj.finders import Finder
from machine_tools.obj.entities import MachineTool
from machine_tools.obj.creators import Creator
from machine_tools.obj.listers import Lister


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
        record_requester=container_for_DB.requester.provider,
    )

    creator = providers.Factory(
        Creator,
        finder_provider=finder.provider
    )

    lister = providers.Factory(
        Lister,
        creator_provider=creator.provider,
        finder_provider=finder.provider
    )

    machine_tool = providers.Factory(
        MachineTool
    )
