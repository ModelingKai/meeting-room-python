from orator import DatabaseManager, Model

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId
from src.infrastructure.employee.orator.orator_employee_model import OratorEmployeeModel
from src.infrastructure.employee.orator.orator_employee_repository import OratorEmployeeRepository
from tests.usecase.reservation.orator.migrate_in_memory import migrate_in_memory, TEST_DB_CONFIG


class TestOratorEmployeeRepository:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)
        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

        self.repository = OratorEmployeeRepository()

    def test_find_by_id(self):
        employee = Employee(EmployeeId('001'), 'Bob')

        OratorEmployeeModel.to_orator_model(employee).save()

        assert self.repository.find_by_id(employee.id) == employee

    def test_find_by_id_return_None_when_not_exist_id(self):
        assert self.repository.find_by_id(EmployeeId('999')) is None

    def test_find_all(self):
        employee_a = Employee(EmployeeId('001'), 'Bob')
        employee_b = Employee(EmployeeId('002'), 'Tom')
        employee_c = Employee(EmployeeId('003'), 'Ken')

        OratorEmployeeModel.to_orator_model(employee_a).save()
        OratorEmployeeModel.to_orator_model(employee_b).save()
        OratorEmployeeModel.to_orator_model(employee_c).save()

        assert self.repository.find_all() == [employee_a, employee_b, employee_c]
