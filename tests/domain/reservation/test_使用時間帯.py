import freezegun
import pytest

from src.domain.reservation.errors import 使用時間帯の範囲がおかしいよError, 未来過ぎて予約できないよError
from src.domain.reservation.使用日時 import 使用日時
from src.domain.reservation.使用時間帯 import 使用時間帯


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約できる時間帯は1000から1900までであること_異常系():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(使用日時(2020, 4, 2, 9, 00), 使用日時(2020, 4, 2, 11, 00))


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約できる時間帯は1000から1900までであること_異常系2():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(使用日時(2020, 4, 2, 19, 15), 使用日時(2020, 4, 2, 19, 30))


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約できる時間帯は1000から1900までであること_異常系3():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(使用日時(2020, 4, 2, 18, 0), 使用日時(2020, 4, 2, 19, 30))


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約できる時間帯は1000から1900までであること_異常系4_前後関係がおかしい():
    with pytest.raises(使用時間帯の範囲がおかしいよError):
        使用時間帯(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 11, 00))


@freezegun.freeze_time('2020-4-1 10:00')
def test_今日から14日より先の予約は不可能であること():
    # TODO:テストメソッド名が、システムよりというか、なんかわかりづらい気がする
    with pytest.raises(未来過ぎて予約できないよError):
        使用時間帯(使用日時(2020, 4, 16, 13, 00), 使用日時(2020, 4, 16, 14, 00))


