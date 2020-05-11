from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId
from src.usecase.employee.find_employee_usecase import FindEmployeeUseCase


class MockFindEmployeeUseCase(FindEmployeeUseCase):
    # TODO: 命名は InMemory かもしれない
    def find_by_id(self, employee_id: EmployeeId) -> Employee:
        return Employee(employee_id, name='Bob')
