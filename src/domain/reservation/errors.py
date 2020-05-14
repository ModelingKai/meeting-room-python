class ReservationDomainObjectError(Exception):
    pass


class Not15分単位Error(ReservationDomainObjectError):
    pass


class 使用時間帯の範囲がおかしいよError(ReservationDomainObjectError):
    pass


class 未来過ぎて予約できないよError(ReservationDomainObjectError):
    pass


class 使用日時は過去であってはいけないんだよError(ReservationDomainObjectError):
    pass


class 予約時間が長すぎError(ReservationDomainObjectError):
    pass
