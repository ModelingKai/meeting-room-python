import uuid

import freezegun
import pytest

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reservation.cancel_meeting_room_usecase import CancelMeetingRoomUsecase
from src.usecase.reservation.errors import NotFoundReservationError


@freezegun.freeze_time('2020-4-1 10:00')
class TestCancelMeetingRoomUsecase:

    def test_予約をキャンセルができること(self):
        reservation_id = ReservationId(str(uuid.uuid4()))

        time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00))
        reservation_人数 = NumberOfParticipants(4)
        meeting_room_id = MeetingRoomId(str(uuid.uuid4()))
        reserver_id = EmployeeId(str(uuid.uuid4()))

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

    def test_存在しない予約に対してキャンセルするのはダメだよ(self):
        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                  NumberOfParticipants(4),
                                  MeetingRoomId(str(uuid.uuid4())),
                                  EmployeeId(str(uuid.uuid4())))

        reservation_repository = InMemoryReservationRepository()

        usecase = CancelMeetingRoomUsecase(reservation_repository)

        with pytest.raises(NotFoundReservationError):
            usecase.cancel_meeting_room(reservation.id)
