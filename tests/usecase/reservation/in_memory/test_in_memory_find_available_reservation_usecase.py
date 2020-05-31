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
from src.usecase.reservation.find_avalible_reservation_usecase import FindAvailableReservationsUsecase


class TestInMemoryFindAvailableReservationsUsecase:
    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation_0402(self) -> Reservation:
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    @pytest.fixture
    @freezegun.freeze_time('2020-3-1 10:00')
    def reservation_0301(self) -> Reservation:
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 3, 2, 13, 00), 使用日時(2020, 3, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_find_available_reservations(self, reservation_0402: Reservation, reservation_0301: Reservation):
        repository = InMemoryReservationRepository()
        usecase = FindAvailableReservationsUsecase(repository)

        cancelled_reservation = dataclasses.replace(reservation_0402,
                                                    id=ReservationId(str(uuid.uuid4())),
                                                    reservation_status=ReservationStatus.Canceled)

        repository.data[reservation_0402.id] = reservation_0402
        repository.data[reservation_0301.id] = reservation_0301
        repository.data[cancelled_reservation.id] = cancelled_reservation

        assert usecase.find_available_reservations() == [reservation_0402]