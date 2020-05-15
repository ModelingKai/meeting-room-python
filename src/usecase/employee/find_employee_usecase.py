from dataclasses import dataclass

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository
from src.domain.employee.errors import NotFoundEmployeeIdError
from src.usecase.employee.errors import NotFoundEmployeeError
from src.usecase.employee.find_employee_command import FindEmployeeCommand


@dataclass
class EmployeeIdFactory:
    employee_repository: EmployeeRepository

    def create(self, employee_id_str: str) -> EmployeeId:
        employees = self.employee_repository.find_all()

        for employee in employees:
            if employee.id.value == employee_id_str:
                return employee.id

        raise NotFoundEmployeeIdError('そんな社員IDはありませんよ')


@dataclass
class FindEmployeeUseCase:
    repository: EmployeeRepository
    id_factory: EmployeeIdFactory

    def find_employee(self, command: FindEmployeeCommand) -> Employee:
        employee_id = self.id_factory.create(command.employee_id)
        employee = self.repository.find_by_id(employee_id)

        if employee is None:
            raise NotFoundEmployeeError('そんな会議室はありませんぜ')

        return employee
