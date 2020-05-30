from __future__ import annotations

from enum import Enum


class ReservationStatus(Enum):
    Canceled = 'キャンセル済み'  # 予約をしたという権利を失っている
    Available = '有効'  # その会議室、時間を使用する権利が有効である

    @classmethod
    def from_str(cls, value: str) -> ReservationStatus:
        if value == cls.Canceled.value:
            return cls.Canceled

        if value == cls.Available.value:
            return cls.Available

        raise ValueError('指定された文字列はありません')