import freezegun
import pytest

from src.domain.reservation.errors import 使用時間帯の範囲がおかしいよError, 予約時間が長すぎError
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
def test_1回の予約における使用時間は最大で2時間でなければならない_異常系():
    with pytest.raises(予約時間が長すぎError):
        予約時間帯(使用日時(2020, 4, 1, 10, 00), 使用日時(2020, 4, 1, 12, 15))


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約時間帯が重なっているかを判断できる_先後かぶりパターン():
    """
    時間帯: ■■■■
    時間帯:     ■■■■
    """
    r_1000_1200 = 予約時間帯(使用日時(2020, 4, 1, 10, 00), 使用日時(2020, 4, 1, 12, 00))
    r_1100_1300 = 予約時間帯(使用日時(2020, 4, 1, 11, 00), 使用日時(2020, 4, 1, 13, 00))

    assert r_1000_1200.is_overlap(r_1100_1300)


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約時間帯が重なっているかを判断できる_後先かぶりパターン():
    """
    時間帯:     ■■■■
    時間帯: ■■■■
    """
    r_1100_1300 = 予約時間帯(使用日時(2020, 4, 1, 11, 00), 使用日時(2020, 4, 1, 13, 00))
    r_1000_1200 = 予約時間帯(使用日時(2020, 4, 1, 10, 00), 使用日時(2020, 4, 1, 12, 00))

    assert r_1100_1300.is_overlap(r_1000_1200)


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約時間帯が重なっているかを判断できる_含んでるパターン():
    """
    時間帯: ■■■■
    時間帯:   ■■
    """
    r_1000_1200 = 予約時間帯(使用日時(2020, 4, 1, 10, 00), 使用日時(2020, 4, 1, 12, 00))
    r_1030_1130 = 予約時間帯(使用日時(2020, 4, 1, 10, 30), 使用日時(2020, 4, 1, 11, 30))

    assert r_1000_1200.is_overlap(r_1030_1130)


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約時間帯が重なっているかを判断できる_含まれているパターン():
    """
    時間帯:   ■■
    時間帯: ■■■■
    """
    r_1030_1130 = 予約時間帯(使用日時(2020, 4, 1, 10, 30), 使用日時(2020, 4, 1, 11, 30))
    r_1000_1200 = 予約時間帯(使用日時(2020, 4, 1, 10, 00), 使用日時(2020, 4, 1, 12, 00))

    assert r_1030_1130.is_overlap(r_1000_1200)


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約時間帯が重なっているかを判断できる_かぶってない_先後パターン():
    """
    時間帯: ■■■■
    時間帯:        ■■■■
    """
    r_1000_1200 = 予約時間帯(使用日時(2020, 4, 1, 10, 00), 使用日時(2020, 4, 1, 12, 00))
    r_1200_1400 = 予約時間帯(使用日時(2020, 4, 1, 12, 00), 使用日時(2020, 4, 1, 14, 00))

    assert not r_1000_1200.is_overlap(r_1200_1400)


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約時間帯が重なっているかを判断できる_かぶってない_後先パターン():
    """
    時間帯:         ■■■■
    時間帯: ■■■■
    """
    r_1200_1400 = 予約時間帯(使用日時(2020, 4, 1, 12, 00), 使用日時(2020, 4, 1, 14, 00))
    r_1000_1200 = 予約時間帯(使用日時(2020, 4, 1, 10, 00), 使用日時(2020, 4, 1, 12, 00))

    assert not r_1200_1400.is_overlap(r_1000_1200)
