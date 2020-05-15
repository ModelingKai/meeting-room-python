class EmployeeDomainObjectError(Exception):
    pass


class NotFoundEmployeeIdError(EmployeeDomainObjectError):
    pass
