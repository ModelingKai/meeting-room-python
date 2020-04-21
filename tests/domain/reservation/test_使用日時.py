import pytest

from src.domain.reservation.errors import Not15分単位Error, 使用日時は過去であってはいけないんだよError
from src.domain.reservation.使用日時 import 使用日時


def test_使用日時が15分単位であること_正常系():
    assert 使用日時(2020, 4, 20, 10, 15).minute % 15 == 0


def test_使用日時が15分単位であること_異常系():
    with pytest.raises(Not15分単位Error):
        使用日時(2020, 4, 20, 10, 34).minute % 15 == 0


def test_使用日時は過去であってはならないこと():
    with pytest.raises(使用日時は過去であってはいけないんだよError):
        使用日時(1970, 1, 1, 10, 00)
