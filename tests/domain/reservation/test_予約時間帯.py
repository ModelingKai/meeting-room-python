import freezegun
import pytest

from src.domain.reservation.errors import 使用時間帯の範囲がおかしいよError, 予約時間が長すぎError
from src.domain.reservation.予約時間帯 import 予約時間帯
from src.domain.reservation.使用日時 import 使用日時


@freezegun.freeze_time('2020-4-1 10:00')
class Test予約時間帯:
    @pytest.mark.parametrize('expected, start1, end1, start2, end2', [
        pytest.param(False,
                     (2020, 4, 1, 10, 00), (2020, 4, 1, 12, 00),  # |========        |
                     (2020, 4, 1, 12, 00), (2020, 4, 1, 14, 00),  # |        ========|
                     id='Not overlap 01'),
        pytest.param(False,
                     (2020, 4, 1, 12, 00), (2020, 4, 1, 14, 00),  # |        ========|
                     (2020, 4, 1, 10, 00), (2020, 4, 1, 12, 00),  # |========        |
                     id='Not overlap 02'),
        pytest.param(True,
                     (2020, 4, 1, 10, 00), (2020, 4, 1, 12, 00),  # |========    |
                     (2020, 4, 1, 11, 00), (2020, 4, 1, 13, 00),  # |    ========|
                     id='Overlap 01'),
        pytest.param(True,
                     (2020, 4, 1, 11, 00), (2020, 4, 1, 13, 00),  # |    ========|
                     (2020, 4, 1, 10, 00), (2020, 4, 1, 12, 00),  # |========    |
                     id='Overlap 02'),
        pytest.param(True,
                     (2020, 4, 1, 10, 00), (2020, 4, 1, 12, 00),  # |========|
                     (2020, 4, 1, 10, 30), (2020, 4, 1, 11, 30),  # |  ====  |
                     id='Overlap 03'),
        pytest.param(True,
                     (2020, 4, 1, 10, 30), (2020, 4, 1, 11, 30),  # |  ====  |
                     (2020, 4, 1, 10, 00), (2020, 4, 1, 12, 00),  # |========|
                     id='Overlap 04'),
    ])
    def test_予約時間帯が重なっているかを判断できる(self, expected, start1, end1, start2, end2):
        time_range1 = 予約時間帯(使用日時(*start1), 使用日時(*end1))
        time_range2 = 予約時間帯(使用日時(*start2), 使用日時(*end2))

        assert expected is time_range1.is_overlap(time_range2)

    @pytest.mark.parametrize('start, end', [
        pytest.param((2020, 4, 2, 9, 00), (2020, 4, 2, 11, 00), id='[Invalid] start time is earlier than 10:00'),
        pytest.param((2020, 4, 2, 19, 15), (2020, 4, 2, 19, 30), id='[Invalid] start time is later than 19:00'),
        pytest.param((2020, 4, 2, 18, 00), (2020, 4, 2, 19, 30), id='[Invalid] end time is later than 19:00'),
        pytest.param((2020, 4, 2, 18, 00), (2020, 4, 2, 11, 00), id='[Invalid] end time is earlier than start time'),
    ])
    def test_予約できる時間帯は1000から1900までであること(self, start, end):
        with pytest.raises(使用時間帯の範囲がおかしいよError):
            予約時間帯(使用日時(*start), 使用日時(*end))

    def test_1回の予約における使用時間は最大で2時間でなければならない(self):
        with pytest.raises(予約時間が長すぎError):
            予約時間帯(使用日時(2020, 4, 1, 10, 00), 使用日時(2020, 4, 1, 12, 15))
