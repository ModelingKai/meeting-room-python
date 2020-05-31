import datetime

import freezegun
import pytest
from orator import DatabaseManager, Model

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder
from tests.usecase.reservation.orator.migrate_in_memory import migrate_in_memory, TEST_DB_CONFIG


class TestOratorReserveMeetingRoomUsecase:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)
        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

        self.repository = OratorReservationRepository()
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ReserveMeetingRoomUsecase(self.repository, domain_service)

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation(self) -> Reservation:
        return DummyReservationBuilder(datetime.datetime.now()).build()

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_予約ができること_正常系(self, reservation):
        self.usecase.reserve_meeting_room(reservation)

        assert reservation == self.repository.find_by_id(reservation.id)
