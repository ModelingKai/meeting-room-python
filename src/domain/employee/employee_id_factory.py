from dataclasses import dataclass

from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository
from src.domain.employee.errors import NotFoundEmployeeIdError


@dataclass
class EmployeeIdFactory:
    employee_repository: EmployeeRepository

    def create(self, employee_id_str: str) -> EmployeeId:
        employees = self.employee_repository.find_all()

        for employee in employees:
            if employee.id.value == employee_id_str:
                return employee.id

        raise NotFoundEmployeeIdError('そんな社員IDはありませんよ')
