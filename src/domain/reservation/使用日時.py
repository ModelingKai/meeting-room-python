from datetime import datetime, timedelta

from src.domain.reservation.errors import Not15分単位Error, 使用日時は過去であってはいけないんだよError, 未来過ぎて予約できないよError


class 使用日時(datetime):

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):
        if datetime(year, month, day, hour, minute, 0) < datetime.now():
            raise 使用日時は過去であってはいけないんだよError('今日より過去の日付では予約できません')

        if minute not in [00, 15, 30, 45]:  # この指定の方が余り演算より明示的なので採用
            raise Not15分単位Error('使用日時は15分単位でなければなりません')

        if self._is_over_limit_available_date():
            raise 未来過ぎて予約できないよError('指定された日にちは予約できません。予約できるのは、申請日を1日目として15日目以内です')

    def _is_over_limit_available_date(self):
        LIMIT_AVAILABLE_DAYS = 15

        limit_available_date = (datetime.today() + timedelta(days=LIMIT_AVAILABLE_DAYS)).date()

        return limit_available_date <= self.date()
