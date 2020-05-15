from dataclasses import dataclass


@dataclass(frozen=True)
class EmployeeId:
    value: str
