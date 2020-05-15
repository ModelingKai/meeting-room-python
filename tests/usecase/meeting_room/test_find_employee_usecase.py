import pytest

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id_factory import EmployeeIdFactory
from src.infrastructure.employee.in_memory_employee_repository import InMemoryEmployeeRepository
from src.usecase.employee.errors import NotFoundEmployeeError
from src.usecase.employee.find_employee_usecase import FindEmployeeUseCase


class TestFindEmployeeUsecase:
    def setup(self):
        self.repository = InMemoryEmployeeRepository()
        self.factory = EmployeeIdFactory(self.repository)
        self.usecase = FindEmployeeUseCase(self.repository)

    def test_社員のIDを渡したら単一の社員情報が取得できる(self):
        employee_id = self.factory.create('001')
        employee = Employee(employee_id, 'Bob')

        self.repository.data[employee_id] = employee

        assert employee == self.usecase.find_employee(employee_id)

    def test_存在しない社員IDが与えられたらエラーとなる(self):
        employee_id = self.factory.create('NotExistId')

        with pytest.raises(NotFoundEmployeeError):
            self.usecase.find_employee(employee_id)
