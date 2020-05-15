from dataclasses import dataclass

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository


@dataclass
class FindEmployeeUseCase:
    repository: EmployeeRepository

    def find_by_id(self, employee_id: EmployeeId) -> Employee:
        pass
