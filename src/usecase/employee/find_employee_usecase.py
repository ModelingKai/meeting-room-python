from dataclasses import dataclass

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository
from src.usecase.employee.errors import NotFoundEmployeeError


@dataclass
class FindEmployeeUseCase:
    repository: EmployeeRepository

    def find_by_id(self, employee_id: EmployeeId) -> Employee:
        employee = self.repository.find_by_id(employee_id)

        if employee is None:
            raise NotFoundEmployeeError('そんな会議室はありませんぜ')

        return employee
