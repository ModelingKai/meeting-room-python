from __future__ import annotations

from orator import Model

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId


class OratorEmployeeModel(Model):
    __table__ = 'meeting_rooms'

    def __repr__(self) -> str:
        # ださいけど、情報がわかりやすくなるので実装している
        tmp = ', '.join([f'{k}={v}' for k, v in self.to_dict().items()])
        repr_like_dataclass = f'{self.__class__.__name__}({tmp})'

        return repr_like_dataclass

    @classmethod
    def to_employee(cls, source: OratorEmployeeModel) -> Employee:
        return Employee(EmployeeId(source.id), source.name)

    @classmethod
    def to_orator_model(cls, employee: Employee) -> OratorEmployeeModel:
        orator_employee = OratorEmployeeModel()
        orator_employee.id = employee.id.value
        orator_employee.name = employee.name

        return orator_employee
