from dataclasses import field, dataclass
from typing import Dict, Optional, List

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository


@dataclass
class InMemoryEmployeeRepository(EmployeeRepository):
    data: Dict[EmployeeId, Employee] = field(default_factory=dict)

    def find_by_id(self, employee_id: EmployeeId) -> Optional[Employee]:
        return self.data.get(employee_id)

    def find_all(self) -> List[Employee]:
        return list(self.data.values())
