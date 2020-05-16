from dataclasses import dataclass

from src.domain.employee.employee import Employee
from src.domain.employee.employee_domain_service import EmployeeDomainService
from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository
from src.domain.employee.errors import NotFoundEmployeeIdError
from src.usecase.employee.find_employee_command import FindEmployeeCommand


@dataclass
class FindEmployeeUseCase:
    repository: EmployeeRepository
    domain_service: EmployeeDomainService

    def find_employee(self, command: FindEmployeeCommand) -> Employee:
        employee_id = EmployeeId(command.employee_id)

        if not self.domain_service.exists_id(employee_id):
            raise NotFoundEmployeeIdError('そのような社員IDはないぞ')

        employee = self.repository.find_by_id(employee_id)

        assert employee

        return employee
