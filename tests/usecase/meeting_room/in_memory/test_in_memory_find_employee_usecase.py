import pytest

from src.domain.employee.employee import Employee
from src.domain.employee.employee_domain_service import EmployeeDomainService
from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.errors import NotFoundEmployeeIdError
from src.infrastructure.employee.in_memory_employee_repository import InMemoryEmployeeRepository
from src.usecase.employee.find_employee_command import FindEmployeeCommand
from src.usecase.employee.find_employee_usecase import FindEmployeeUseCase


class TestInMemoryFindEmployeeUsecase:
    def setup(self):
        self.repository = InMemoryEmployeeRepository()
        domain_service = EmployeeDomainService(self.repository)
        self.usecase = FindEmployeeUseCase(self.repository, domain_service)

    def test_社員のIDを渡したら単一の社員情報が取得できる(self):
        employee_id = EmployeeId('001')
        employee = Employee(employee_id, 'Bob')
        self.repository.data[employee_id] = employee

        command = FindEmployeeCommand('001')
        assert employee == self.usecase.find_employee(command)

    def test_存在しない社員IDが与えられたらエラーとなる(self):
        command = FindEmployeeCommand('009')

        with pytest.raises(NotFoundEmployeeIdError):
            self.usecase.find_employee(command)
