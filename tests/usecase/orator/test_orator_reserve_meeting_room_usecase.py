import uuid

import freezegun
import pytest
from orator import DatabaseManager

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.init_db import DB_CONFIG
from src.infrastructure.reservation.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase


class TestReserveMeetingRoomUsecase:
    def setup(self):
        database_manager = DatabaseManager(DB_CONFIG)

        self.reservation_repository = OratorReservationRepository(database_manager)
        domain_service = ReservationDomainService(self.reservation_repository)
        self.usecase = ReserveMeetingRoomUsecase(self.reservation_repository, domain_service)

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation(self) -> Reservation:
        """不正でないReservationインスタンスを作成するだけのfixture"""
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId(str(uuid.uuid4())),
                           EmployeeId(str(uuid.uuid4())))

    def test_予約ができること_正常系_(self, reservation):
        self.usecase.reserve_meeting_room(reservation)
