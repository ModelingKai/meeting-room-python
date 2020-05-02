from __future__ import annotations

import datetime
from dataclasses import dataclass

from src.domain.reservation import 使用日時
from src.domain.reservation.errors import 使用時間帯の範囲がおかしいよError, 使用日時は過去であってはいけないんだよError, 予約時間が長すぎError


@dataclass(frozen=True)
class TimeRangeToReserve:
    start_datetime: 使用日時
    end_datetime: 使用日時

    def __post_init__(self):
        if not (datetime.time(10, 00) <= self.start_datetime.time() < self.end_datetime.time() <= datetime.time(19,
                                                                                                                00)):
            raise 使用時間帯の範囲がおかしいよError('使用時間帯は10:00-19:00じゃないとダメだぞ！')

        if self.start_datetime.date() < datetime.date.today() or self.end_datetime.date() < datetime.date.today():
            raise 使用日時は過去であってはいけないんだよError('今日より過去の日付では予約できません')

        if self._is_over_maximum_available_time():
            raise 予約時間が長すぎError('予約時間なげーよ')

    def _is_over_maximum_available_time(self) -> bool:
        MAXIMUM_SECONDS = 60 * 60 * 2

        return MAXIMUM_SECONDS < (self.end_datetime - self.start_datetime).total_seconds()

    def is_overlap(self, other: TimeRangeToReserve) -> bool:
        # 重なりがある場合を考えるのが難しかったので、重ならない場合の余事象を考えた
        is_先後_かぶりなし = (self.start_datetime < self.end_datetime <= other.start_datetime < other.end_datetime)
        is_後先_かぶりなし = (other.start_datetime < other.end_datetime <= self.start_datetime < self.end_datetime)

        is_かぶりなし = is_先後_かぶりなし or is_後先_かぶりなし

        return not is_かぶりなし
