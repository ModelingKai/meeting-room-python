from datetime import datetime

from src.domain.reservation.errors import Not15分単位Error, 過去の日付は予約できないよError


class 使用日時(datetime):

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):
        if datetime(year, month, day, hour, minute, 0) < datetime.now():
            raise 過去の日付は予約できないよError('今日より過去の日付では予約できません')

        if minute not in [00, 15, 30, 45]:  # この指定の方が余り演算より明示的なので採用
            raise Not15分単位Error('使用日時は15分単位でなければなりません')
