from dataclasses import dataclass

from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository


@dataclass
class EmployeeIdFactory:
    repository: EmployeeRepository

    def create(self, employee_id: str) -> EmployeeId:
        return EmployeeId('001')
