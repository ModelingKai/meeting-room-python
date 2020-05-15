from dataclasses import dataclass

from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository


@dataclass
class EmployeeIdFactory(object):
    repository: EmployeeRepository

    def create(self, param) -> EmployeeId:
        pass
