import uuid

import freezegun
import pytest

from src.domain.employee.社員ID import 社員ID
from src.domain.meeting_room.会議室ID import 会議室ID
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用人数 import 使用人数
from src.domain.reservation.使用日時 import 使用日時


@freezegun.freeze_time('2020-4-1 10:00')
def test_reservation():
    sut = Reservation(ReservationId(str(uuid.uuid4())),
                      TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                      使用人数(4),
                      会議室ID(str(uuid.uuid4())),
                      reserver_id=社員ID(str(uuid.uuid4())))

    assert sut is not None


@freezegun.freeze_time('2020-4-1 10:00')
def test_予約ステータスをキャンセル済に変更できる():
    reservation_id = ReservationId(str(uuid.uuid4()))
    meeting_room_id = 会議室ID(str(uuid.uuid4()))
    reserver_id = 社員ID(str(uuid.uuid4()))
    reservation_予約時間帯 = TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00))
    reservation_使用人数 = 使用人数(4)

    reservation = Reservation(reservation_id,
                              reservation_予約時間帯,
                              reservation_使用人数,
                              meeting_room_id,
                              reserver_id)

    expected = Reservation(reservation_id,
                           reservation_予約時間帯,
                           reservation_使用人数,
                           meeting_room_id,
                           reserver_id,
                           reservation_status=ReservationStatus.Canceled)

    assert expected == reservation.cancel()


@freezegun.freeze_time('2020-4-1 10:00')
def test_キャンセル済みの予約をもう一度キャンセルしようとしてエラーになること():
    sut = Reservation(ReservationId(str(uuid.uuid4())),
                      TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                      使用人数(4),
                      会議室ID(str(uuid.uuid4())),
                      reserver_id=社員ID(str(uuid.uuid4())))

    with pytest.raises(ValueError):
        sut.cancel().cancel()
