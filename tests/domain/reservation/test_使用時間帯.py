import pytest

from src.domain.reservation.errors import 使用開始日時Error, Not15分単位Error
from src.domain.reservations.使用日時 import 使用日時
from src.domain.reservations.使用時間帯 import 使用時間帯


def test_使用日時が15分単位であること_正常系():
    assert 使用日時(2020, 4, 20, 10, 15).minute % 15 == 0


def test_使用日時が15分単位であること_異常系():
    with pytest.raises(Not15分単位Error):
        使用日時(2020, 4, 20, 10, 34).minute % 15 == 0


def test_予約できる時間帯は1000から1900までであること_異常系():
    start = 使用日時(2020, 4, 20, 9, 0)
    end = 使用日時(2020, 4, 20, 12, 0)

    with pytest.raises(使用開始日時Error):
        使用時間帯(start, end)
