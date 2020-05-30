import uuid

import freezegun
import pytest

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.available_reservations import AvailableReservations
from src.domain.reservation.errors import NotAvailableReservationError
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時


class TestReservationsTest:
    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def canceled_reservation(self) -> Reservation:
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 3, 13, 00), 使用日時(2020, 4, 3, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'),
                           ReservationStatus.Canceled)

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_初期化時に有効ではない予約を含むリストを渡すとエラーとなる(self, canceled_reservation):
        with pytest.raises(NotAvailableReservationError):
            AvailableReservations([canceled_reservation])

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_有効ではない予約を追加時にエラーとなる(self, canceled_reservation):
        with pytest.raises(NotAvailableReservationError):
            AvailableReservations().add(canceled_reservation)
