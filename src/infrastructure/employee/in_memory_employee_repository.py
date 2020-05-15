from dataclasses import field, dataclass
from typing import Dict

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository


@dataclass
class InMemoryEmployeeRepository(EmployeeRepository):
    data: Dict[EmployeeId, Employee] = field(default_factory=dict)
