from dataclasses import dataclass

from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository


@dataclass
class EmployeeDomainService:
    repository: EmployeeRepository

    def exists_id(self, employee_id: EmployeeId) -> bool:
        exist_employees = self.repository.find_all()

        for exist_employee in exist_employees:
            if exist_employee.id == employee_id:
                return True

        return False
