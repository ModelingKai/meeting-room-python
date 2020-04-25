import uuid

import freezegun

from src.domain.employee.社員ID import 社員ID
from src.domain.meeting_room.会議室ID import 会議室ID
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.予約時間帯 import 予約時間帯
from src.domain.reservation.使用人数 import 使用人数
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase


@freezegun.freeze_time('2020-4-1 10:00')
def test_会議室を予約する_正常系():
    expected = Reservation(予約時間帯(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           使用人数(4),
                           会議室ID(str(uuid.uuid4())),
                           reserver_id=社員ID(str(uuid.uuid4())))

    reservation_repository = InMemoryReservationRepository()
    usecase = ReserveMeetingRoomUsecase(reservation_repository)

    usecase.reserve_meeting_room(expected)

    assert expected == reservation_repository.data[expected.id]
