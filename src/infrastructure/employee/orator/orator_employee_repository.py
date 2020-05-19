from typing import Optional, List

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository
from src.infrastructure.employee.orator.orator_employee_model import OratorEmployeeModel


class OratorEmployeeRepository(EmployeeRepository):

    def find_by_id(self, employee_id: EmployeeId) -> Optional[Employee]:
        orator_employee = OratorEmployeeModel.find(employee_id.value)

        if orator_employee is None:
            return None

        return OratorEmployeeModel.to_employee(orator_employee)

    def find_all(self) -> List[Employee]:
        return list(map(OratorEmployeeModel.to_employee, OratorEmployeeModel.all()))
