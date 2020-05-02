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


@pytest.fixture(scope='function')
@freezegun.freeze_time('2020-4-1 10:00')
def reservation():
    """不正でないReservationインスタンスを作成するだけのfixture"""
    return Reservation(ReservationId(str(uuid.uuid4())),
                       TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                       NumberOfParticipants(4),
                       MeetingRoomId(str(uuid.uuid4())),
                       EmployeeId(str(uuid.uuid4())))
