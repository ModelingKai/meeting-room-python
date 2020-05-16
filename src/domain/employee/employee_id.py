import re
from dataclasses import dataclass

from src.domain.employee.errors import InvalidFormatEmployeeIdError


@dataclass(frozen=True)
class EmployeeId:
    value: str

    def __post_init__(self):
        pattern = r'[0-9]{3}'

        if not re.fullmatch(pattern, self.value):
            raise InvalidFormatEmployeeIdError('社員IDは0埋めの3桁の数字でなければなりません')
