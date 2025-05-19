#!/usr/bin/env python
# -*- coding: utf-8 -*-

from machine_tools.app.containers.finder_container import FinderContainer


def main():
    # Создаем контейнер
    container = FinderContainer()

    # Получаем разные варианты finder'а
    list_name_finder = container.finder_with_list_names()
    list_info_finder = container.finder_with_list_info()
    dict_name_finder = container.finder_with_dict_names()
    dict_info_finder = container.finder_with_dict_info()
    indexed_name_finder = container.finder_with_indexed_names()
    indexed_info_finder = container.finder_with_indexed_info()

    # Пример использования finder'а со списком имен
    with list_name_finder as finder:
        machines = finder.by_power(min_power=10.0, order_by_power=True, descending=True)
        print("Список имен мощных станков:", machines)

    # Пример использования finder'а с полной информацией
    with list_info_finder as finder:
        machines = finder.by_efficiency(min_efficiency=0.8, order_by_efficiency=True, descending=True)
        print("\nСписок станков с высоким КПД:")
        for machine in machines:
            print(f"- {machine.name}: мощность={machine.power}кВт, КПД={machine.efficiency}")

    # Пример использования finder'а со словарем имен
    with dict_name_finder as finder:
        machines = finder.by_accuracy("Н")
        print("\nСловарь имен точных станков:", machines)

    # Пример использования finder'а со словарем полной информации
    with dict_info_finder as finder:
        machines = finder.by_automation("ЧПУ")
        print("\nСловарь станков с ЧПУ:")
        for name, info in machines.items():
            print(f"- {name}: мощность={info.power}кВт, КПД={info.efficiency}")

    # Пример использования finder'а с индексированным списком имен
    with indexed_name_finder as finder:
        machines = finder.by_specialization("Токарная обработка")
        print("\nИндексированный список токарных станков:", machines)

    # Пример использования finder'а с индексированной полной информацией
    with indexed_info_finder as finder:
        machines = finder.all()
        print("\nИндексированный список всех станков:")
        for idx, info in machines.items():
            print(f"{idx}. {info.name}: мощность={info.power}кВт, КПД={info.efficiency}")


if __name__ == "__main__":
    main()
