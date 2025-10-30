from typing import Optional
from sqlalchemy.orm import Session

from machine_tools import MachineFormatter, Finder, ListNameFormatter, session_manager, SoftwareControl


with Finder(limit=3) as finder:
    finder.set_limit(3)
    print(f"BASE FINDER find_by_power:", finder.find_by_power(min_power=5.0))


class MachineFinderForAnyWere(Finder):
    def __init__(
        self,
        session: Optional[Session] = None,
        formatter: Optional[MachineFormatter] = None,
    ):
        super().__init__(
            session=session or session_manager.get_session(),
            limit=None,
            formatter=formatter or ListNameFormatter(),
        )

    def find_by_power(
        self,
        min_power: float = None,
        max_power: float = None,
        order_by_power: bool = True,
        descending: bool = True,
        limit: int = None,
    ):
        self._apply_limit(limit)
        builder = self._builder.filter_by_power(min_power=min_power, max_power=max_power)
        builder = builder.filter_by_software_control(SoftwareControl.CNC.value)
        if order_by_power:
            builder = builder.order_by("power", descending=descending)
        machines = builder.execute()
        self.reset_builder()
        return self._formatter.format(machines)


with MachineFinderForAnyWere() as finder:
    finder.set_limit(3)
    print("CUSTOM FINDER find_by_power:", finder.find_by_power(min_power=5.0))
    print("CUSTOM FINDER find_by_power (asc):", finder.find_by_power(min_power=5.0, descending=False))



