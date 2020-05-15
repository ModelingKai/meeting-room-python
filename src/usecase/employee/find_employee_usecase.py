from dataclasses import dataclass

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id_factory import EmployeeIdFactory
from src.domain.employee.employee_repository import EmployeeRepository
from src.usecase.employee.find_employee_command import FindEmployeeCommand


@dataclass
class FindEmployeeUseCase:
    repository: EmployeeRepository
    id_factory: EmployeeIdFactory

    def find_employee(self, command: FindEmployeeCommand) -> Employee:
        employee_id = self.id_factory.create(command.employee_id)

        return self.repository.find_by_id(employee_id)
