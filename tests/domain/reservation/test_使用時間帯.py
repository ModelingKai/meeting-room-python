import pytest

from src.domain.reservations.使用日時 import 使用日時


def test_使用日時が15分単位であること_正常系():
    assert 使用日時(2020, 4, 20, 10, 15).minute % 15 == 0


def test_使用日時が15分単位であること_異常系():
    with pytest.raises(ValueError):
        使用日時(2020, 4, 20, 10, 34).minute % 15 == 0
