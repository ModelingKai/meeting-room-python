import uuid

import freezegun

from src.domain.employee.社員ID import 社員ID
from src.domain.meeting_room.会議室ID import 会議室ID
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用人数 import 使用人数
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.cancel_meeting_room_usecase import CancelMeetingRoomUsecase


@freezegun.freeze_time('2020-4-1 10:00')
class TestCancelMeetingRoomUsecase:

    def test_予約をキャンセルができること(self):
        reservation_id = ReservationId(str(uuid.uuid4()))

        time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00))
        reservation_人数 = 使用人数(4)
        meeting_room_id = 会議室ID(str(uuid.uuid4()))
        reserver_id = 社員ID(str(uuid.uuid4()))

        reservation = Reservation(reservation_id,
                                  time_range_to_reserve,
                                  reservation_人数,
                                  meeting_room_id,
                                  reserver_id)

        expected = Reservation(reservation_id,
                               time_range_to_reserve,
                               reservation_人数,
                               meeting_room_id,
                               reserver_id,
                               reservation_status=ReservationStatus.Canceled)

        reservation_repository = InMemoryReservationRepository()
        reservation_repository.data[reservation.id] = reservation

        usecase = CancelMeetingRoomUsecase(reservation_repository)
        usecase.cancel_meeting_room(reservation_id)

        assert expected == reservation_repository.data[reservation_id]
