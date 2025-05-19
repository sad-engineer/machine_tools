#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Optional

from machine_tools.app.containers import FinderContainer
from machine_tools.app.schemas import MachineInfo


def find_names(substring: str) -> List[str]:
    """Запрашивает из БД список имен станков, соответствующих подстроке
    Args:
        substring: подстрока, по которой производится поиск
    Returns:
        список имен станков, соответствующих подстроке
    """
    container = FinderContainer()
    finder = container.finder_with_list_names()
    return finder.by_name(substring, exact_match=False)


def get_machine_info_by_name(name: str) -> Optional[MachineInfo]:
    """Запрашивает из БД информацию о станке по его имени
    Args:
        name: имя станка
    Returns:
        информация о станке, если она найдена, иначе None
    """
    container = FinderContainer()
    finder = container.finder_with_list_info()
    result = finder.by_name(name, exact_match=True)
    if len(result) > 0:
        return result[0]
    else:
        return None


if __name__ == "__main__":
    print(find_names("16К20"))
    print(get_machine_info_by_name("16К20"))
