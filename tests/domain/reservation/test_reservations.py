import uuid

import freezegun
import pytest

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.reservations import Reservations
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時


class TestReservationsTest:
    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation_0401(self) -> Reservation:
        """不正でないReservationインスタンスを作成するだけのfixture"""
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 1, 13, 00), 使用日時(2020, 4, 1, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation_0402(self) -> Reservation:
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation_0403_canceled(self) -> Reservation:
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 3, 13, 00), 使用日時(2020, 4, 3, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'),
                           ReservationStatus.Canceled)

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_キャンセル済みでは無い予約全てを取得できること(self, reservation_0401, reservation_0402, reservation_0403_canceled):
        reservations = Reservations([reservation_0401, reservation_0402, reservation_0403_canceled])

        assert reservations.not_cancels() == Reservations([reservation_0401, reservation_0402])
