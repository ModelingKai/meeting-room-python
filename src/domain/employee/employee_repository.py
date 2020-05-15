from abc import ABCMeta, abstractmethod
from typing import Optional, List

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId


class EmployeeRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_id(self, employee_id: EmployeeId) -> Optional[Employee]:
        pass

    @abstractmethod
    def find_all(self) -> List[Employee]:
        pass
