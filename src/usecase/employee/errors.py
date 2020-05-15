class EmployeeUsecaseError(Exception):
    pass


class NotFoundEmployeeError(EmployeeUsecaseError):
    pass