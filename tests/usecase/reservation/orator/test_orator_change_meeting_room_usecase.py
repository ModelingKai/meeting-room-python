import dataclasses
import uuid

import freezegun
import pytest
from orator import DatabaseManager, Model

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.change_meeting_room_usecase import ChangeMeetingRoomUseCase
from tests.usecase.reservation.orator.migrate_in_memory import TEST_DB_CONFIG, migrate_in_memory


class TestOratorChangeMeetingRoomUsecase:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)
        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

        self.repository = OratorReservationRepository()
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ChangeMeetingRoomUseCase(self.repository, domain_service)

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation(self) -> Reservation:
        """不正でないReservationインスタンスを作成するだけのfixture"""
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_既存の予約を別の会議室に変更ができること(self, reservation):
        self.repository.reserve_new_meeting_room(reservation)

        expected = dataclasses.replace(reservation, meeting_room_id=MeetingRoomId('A'))

        self.usecase.change_meeting_room(reservation.id, expected.meeting_room_id)

        assert expected == self.repository.find_by_id(reservation.id)
