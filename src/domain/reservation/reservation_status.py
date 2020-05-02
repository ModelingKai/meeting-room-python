from __future__ import annotations

from enum import Enum


class ReservationStatus(Enum):
    Canceled = 'キャンセル済み'
    Reserved = '予約中'

    @classmethod
    def from_str(cls, value: str) -> ReservationStatus:
        if value == cls.Canceled.value:
            return cls.Canceled

        if value == cls.Reserved.value:
            return cls.Reserved

        raise ValueError('指定された文字列はありません')
