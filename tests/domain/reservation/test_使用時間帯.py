import datetime

import freezegun
import pytest

from src.domain.reservation.errors import 使用時間帯の範囲がおかしいよError, 未来過ぎて予約できないよError, 過去の日付は予約できないよError
from src.domain.reservation.使用日時 import 使用日時
from src.domain.reservation.使用時間帯 import 使用時間帯


@freezegun.freeze_time('2020-4-18 10:00')
def test_予約できる時間帯は1000から1900までであること_異常系():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        someday = datetime.date.today()
        yyyy, mm, dd = someday.year, someday.month, someday.day

        使用時間帯(使用日時(yyyy, mm, dd, 9, 00), 使用日時(yyyy, mm, dd, 11, 00))


def test_予約できる時間帯は1000から1900までであること_異常系2():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(使用日時(2020, 4, 20, 19, 15), 使用日時(2020, 4, 20, 19, 30))


def test_予約できる時間帯は1000から1900までであること_異常系3():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(使用日時(2020, 4, 20, 18, 0), 使用日時(2020, 4, 20, 19, 30))


def test_予約できる時間帯は1000から1900までであること_異常系4_前後関係がおかしい():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(使用日時(2020, 4, 20, 13, 00), 使用日時(2020, 4, 20, 11, 00))


def test_過去の日時で会議室は予約できないこと():
    with pytest.raises(過去の日付は予約できないよError):
        使用時間帯(使用日時(1999, 1, 1, 13, 00), 使用日時(1999, 1, 1, 14, 00))


@freezegun.freeze_time('2020-5-1 10:00')
def test_今日から14日より先の予約は不可能であること():
    # TODO:テストメソッド名が、システムよりというか、なんかわかりづらい気がする
    with pytest.raises(未来過ぎて予約できないよError):
        使用時間帯(使用日時(2020, 5, 16, 13, 00), 使用日時(2020, 5, 16, 14, 00))


@freezegun.freeze_time('2020-5-1 10:00')
def test_今日から14日後の予約は可能であること():
    term = 使用時間帯(使用日時(2020, 5, 15, 13, 00), 使用日時(2020, 5, 15, 14, 00))
    assert term is not None
