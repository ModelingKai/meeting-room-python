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
from src.presentation.cli.cli_util.success_message_builder import SuccessMessageBuilder


class TestSuccessMessageBuilder:
    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation(self) -> Reservation:
        """不正でないReservationインスタンスを作成するだけのfixture"""
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    def test_1(self, reservation: Reservation):
        expected = 'Bobさん名義で、2020年04月02日 13:00-14:00 大会議室 を 4名で 予約しましたよ'

        success_message_builder = SuccessMessageBuilder()
        success_message = success_message_builder.build(reservation)

        assert expected == str(success_message)
