from dataclasses import dataclass

from src.domain.employee.employee_id import EmployeeId


@dataclass
class Employee:
    id: EmployeeId
    name: str