import pytest

from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.errors import InvalidFormatEmployeeIdError


class TestEmployeeId:
    @pytest.mark.parametrize('value', ['1', '01', '0001', '-1', 'A', 'AB'])
    def test_社員IDは0埋めの3桁の数字でなければなりません(self, value: str):
        with pytest.raises(InvalidFormatEmployeeIdError):
            EmployeeId(value)
