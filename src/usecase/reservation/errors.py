class ReservationUsecaseError(Exception):
    pass


class その会議室はその時間帯では予約ができませんよエラー(ReservationUsecaseError):
    pass


class NotFoundReservationError(ReservationUsecaseError):
    pass
