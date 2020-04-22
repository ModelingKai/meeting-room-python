import datetime
from dataclasses import dataclass

from src.domain.reservation import 使用日時
from src.domain.reservation.errors import 使用時間帯の範囲がおかしいよError, 未来過ぎて予約できないよError, 使用日時は過去であってはいけないんだよError


@dataclass(frozen=True)
class 予約時間帯:
    start: 使用日時
    end: 使用日時

    def __post_init__(self):
        if not (datetime.time(10, 00) <= self.start.time() < self.end.time() <= datetime.time(19, 00)):
            raise 使用時間帯の範囲がおかしいよError('使用時間帯は10:00-19:00じゃないとダメだぞ！')

        if self.start.date() < datetime.date.today() or self.end.date() < datetime.date.today():
            raise 使用日時は過去であってはいけないんだよError('今日より過去の日付では予約できません')

        later_15_date = (datetime.datetime.today() + datetime.timedelta(days=15)).date()
        if later_15_date <= self.start.date() or later_15_date <= self.end.date():
            raise 未来過ぎて予約できないよError('指定された日にちは予約できません。予約できるのは、申請日を1日目として15日目以内です')
