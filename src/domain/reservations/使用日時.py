from datetime import datetime


class 使用日時(datetime):

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int):
        if minute not in [00, 15, 30, 45]:  # この指定の方が余り演算より明示的なので採用
            raise ValueError('使用日時は15分単位でなければなりません')
