#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import logging.config

from service_for_my_projects import timeit, timeit_property

from machine_tools.obj.containers import MachineToolsContainer as Container
from machine_tools.logger_settings import config

import os.path
if not os.path.exists("logs/"):
    os.makedirs("logs/")

logging.config.dictConfig(config)


def main():
    creator = Container().creator()
    create = creator.by_name
    timeit("Время запроса одного станка: {}")(create)("16К20Ф3")

    result = creator.default(type_processing="Фрезерование")
    print(result)

    lister = Container().lister()
    result = timeit_property("Время запроса всех станков: {}")(lister)("all")
    print(len(result))

    create = lister.by_type_and_group
    result = timeit("Время запроса станков по типу и группе: {}")(create)(machine_type=1, group=1)
    print(len(result))

    machine_tools = creator.by_name("16К20Ф3")
    print(machine_tools.length)
    print(machine_tools.width)
    print(machine_tools.height)


if __name__ == '__main__':
    main()
