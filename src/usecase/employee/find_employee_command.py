from dataclasses import dataclass


@dataclass
class FindEmployeeCommand:
    employee_id: str
