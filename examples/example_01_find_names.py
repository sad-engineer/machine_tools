#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Union

from machine_tools import Finder, Accuracy, Automation, Specialization, SoftwareControl


limit = 5
with Finder(limit=limit) as finder:
    print(f"1). {finder.find_all()}")

    name: str = "16К20"
    print(f"2). {finder.find_by_name(name)}")

    power: float = 10.0
    min_power: float = 5.0
    max_power: float = 20.0
    print(f"3). {finder.find_by_power(power)}")
    print(f"4). {finder.find_by_power(min_power=min_power, max_power=max_power)}")

    efficiency: float = 0.75
    print(f"5). {finder.find_by_efficiency(efficiency)}")

    min_efficiency: float = 0.6
    max_efficiency: float = 0.9
    print(f"6). {finder.find_by_efficiency(min_efficiency=min_efficiency, max_efficiency=max_efficiency,)}")

    accuracy = Accuracy.A.value
    print(f"7). {finder.find_by_accuracy(accuracy)}")

    automation = Automation.AUTOMATIC.value
    print(f"8). {finder.find_by_automation(automation)}")

    specialization = Specialization.UNIVERSAL.value
    print(f"9). {finder.find_by_specialization(specialization)}")

    software_control = SoftwareControl.CNC.value
    print(f"10). {finder.find_by_software_control(software_control)}")

    group: Union[int, List[int]] = 2
    print(f"11). {finder.find_by_group(group)}")
    print(f"12). {finder.find_by_group([1, 2, 3])}")

    type_: Union[int, List[int]] = 1
    print(f"13). {finder.find_by_type(type_)}")
    print(f"14). {finder.find_by_type([0, 1, 2])}")


