import pytest

from src.domain.reservation.errors import 使用時間帯の範囲がおかしいよError
from src.domain.reservation.使用日時 import 使用日時
from src.domain.reservation.使用時間帯 import 使用時間帯


def test_予約できる時間帯は1000から1900までであること_異常系():
    start = 使用日時(2020, 4, 20, 9, 00)
    end = 使用日時(2020, 4, 20, 11, 00)

    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(start, end)


def test_予約できる時間帯は1000から1900までであること_異常系2():
    start = 使用日時(2020, 4, 20, 19, 15)
    end = 使用日時(2020, 4, 20, 19, 30)

    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(start, end)


def test_予約できる時間帯は1000から1900までであること_異常系3():
    start = 使用日時(2020, 4, 20, 18, 0)
    end = 使用日時(2020, 4, 20, 19, 30)

    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(start, end)


def test_予約できる時間帯は1000から1900までであること_異常系4_前後関係がおかしい():
    # start が end より 後になっている
    start = 使用日時(2020, 4, 20, 13, 00)
    end = 使用日時(2020, 4, 20, 11, 00)

    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(start, end)
