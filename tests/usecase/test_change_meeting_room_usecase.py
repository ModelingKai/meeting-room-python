import uuid

import freezegun
import pytest

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reservation.change_meeting_room_usecase import ChangeMeetingRoomUseCase
from src.usecase.reservation.errors import NotFoundReservationError


class TestChangeMeetingRoomUsecase:
    @freezegun.freeze_time('2020-4-1 10:00')
    def test_既存の予約を別の会議室に変更ができること(self):
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

        new_meeting_room_id = MeetingRoomId(str(uuid.uuid4()))
        expected = Reservation(reservation_id,
                               time_range_to_reserve,
                               reservation_人数,
                               new_meeting_room_id,
                               reserver_id)

        repository = InMemoryReservationRepository()
        repository.data[reservation.id] = reservation
        usecase = ChangeMeetingRoomUseCase(repository)
        usecase.change_meeting_room(reservation.id, new_meeting_room_id)

        assert expected == repository.data[reservation.id]

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_存在しない予約に対する会議室変更依頼はダメだよ(self):
        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                  NumberOfParticipants(4),
                                  MeetingRoomId(str(uuid.uuid4())),
                                  EmployeeId(str(uuid.uuid4())))

        reservation_repository = InMemoryReservationRepository()
        usecase = ChangeMeetingRoomUseCase(reservation_repository)

        with pytest.raises(NotFoundReservationError):
            usecase.change_meeting_room(reservation.id, MeetingRoomId(str(uuid.uuid4())))
