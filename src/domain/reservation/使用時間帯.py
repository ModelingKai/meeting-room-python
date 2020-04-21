import datetime
from dataclasses import dataclass

from src.domain.reservation import 使用日時
from src.domain.reservation.errors import 使用時間帯の範囲がおかしいよError


@dataclass(frozen=True)
class 使用時間帯:
    start: 使用日時
    end: 使用日時

    def __post_init__(self):
        if not (datetime.time(10, 00) <= self.start.time() < self.end.time() <= datetime.time(19, 00)):
            raise 使用時間帯の範囲がおかしいよError('使用時間帯は10:00-19:00じゃないとダメだぞ！')

        if self.start.date() < datetime.date.today() or self.end.date() < datetime.date.today():
            raise 使用時間帯の範囲がおかしいよError('今日より過去の日付では予約できません')

        later_14_days = datetime.datetime.now() + datetime.timedelta(days=14)
        if later_14_days.date() < self.start.date() or later_14_days.date() < self.end.date():
            raise 使用時間帯の範囲がおかしいよError('予約が可能な会議室は、14日後以内です')
