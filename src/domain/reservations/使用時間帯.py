import datetime
from dataclasses import dataclass

from src.domain.reservation.errors import 使用開始日時Error
from src.domain.reservations import 使用日時


@dataclass(frozen=True)
class 使用時間帯:
    start: 使用日時
    end: 使用日時

    def __post_init__(self):
        if self.start.time() < datetime.time(10, 00):
            raise 使用開始日時Error('start が 10:00より早いとOUT')
