import datetime

import freezegun
import pytest

from src.domain.reservation.errors import 使用時間帯の範囲がおかしいよError, 未来過ぎて予約できないよError
from src.domain.reservation.予約時間帯 import 予約時間帯
from src.domain.reservation.使用日時 import 使用日時


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約できる時間帯は1000から1900までであること_異常系():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        予約時間帯(使用日時(2020, 4, 2, 9, 00), 使用日時(2020, 4, 2, 11, 00))


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約できる時間帯は1000から1900までであること_異常系2():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        予約時間帯(使用日時(2020, 4, 2, 19, 15), 使用日時(2020, 4, 2, 19, 30))


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約できる時間帯は1000から1900までであること_異常系3():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        予約時間帯(使用日時(2020, 4, 2, 18, 0), 使用日時(2020, 4, 2, 19, 30))


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約できる時間帯は1000から1900までであること_異常系4_前後関係がおかしい():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        予約時間帯(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 11, 00))


@freezegun.freeze_time('2020-4-1 10:00')
def test_申請日を1日目として15日目より先の予約はできないこと():
    later_15_date = datetime.datetime.today() + datetime.timedelta(days=15)
    yyyy, mm, dd = later_15_date.year, later_15_date.month, later_15_date.day

    with pytest.raises(未来過ぎて予約できないよError):
        予約時間帯(使用日時(yyyy, mm, dd, 13, 00), 使用日時(yyyy, mm, dd, 14, 00))
