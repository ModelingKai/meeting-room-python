import dataclasses
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
    def setup(self):
        self.reservation_repository = InMemoryReservationRepository()
        self.usecase = CancelMeetingRoomUsecase(self.reservation_repository)

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation(self) -> Reservation:
        """不正でないReservationインスタンスを作成するだけのfixture"""
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    def test_予約をキャンセルができること(self, reservation):
        expected = dataclasses.replace(reservation, reservation_status=ReservationStatus.Canceled)

        self.reservation_repository.data[reservation.id] = reservation

        self.usecase.cancel_meeting_room(reservation.id)

        assert expected == self.reservation_repository.data[reservation.id]

    def test_存在しない予約に対してキャンセルするのはダメだよ(self, reservation):
        with pytest.raises(NotFoundReservationError):
            self.usecase.cancel_meeting_room(reservation.id)

    def test_キャンセル済みに対してキャンセルするのもダメだよ(self, reservation):
        canceled_reservation = dataclasses.replace(reservation, reservation_status=ReservationStatus.Canceled)

        self.reservation_repository.data[canceled_reservation.id] = canceled_reservation

        with pytest.raises(ValueError):
            self.usecase.cancel_meeting_room(canceled_reservation.id)
