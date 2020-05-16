class EmployeeDomainObjectError(Exception):
    pass


class NotFoundEmployeeIdError(EmployeeDomainObjectError):
    pass


class InvalidFormatEmployeeIdError(EmployeeDomainObjectError):
    pass
