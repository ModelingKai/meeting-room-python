import dataclasses

from orator import DatabaseManager, Model

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.change_meeting_room_usecase import ChangeMeetingRoomUseCase
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder
from tests.usecase.reservation.orator.migrate_in_memory import TEST_DB_CONFIG, migrate_in_memory


class TestOratorChangeMeetingRoomUsecase:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)
        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

        self.repository = OratorReservationRepository()
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ChangeMeetingRoomUseCase(self.repository, domain_service)

    def test_指定した予約の会議室を変更できること(self):
        builder = DummyReservationBuilder()
        reservation_A = builder.with_meeting_room_id(MeetingRoomId('A')).build()
        reservation_B = builder.with_meeting_room_id(MeetingRoomId('B')).build()
        reservation_C = builder.with_meeting_room_id(MeetingRoomId('C')).build()

        self.repository.reserve_new_meeting_room(reservation_A)
        self.repository.reserve_new_meeting_room(reservation_B)
        self.repository.reserve_new_meeting_room(reservation_C)

        meeting_room_id_Z = MeetingRoomId('Z')
        self.usecase.change_meeting_room(reservation_B.id, meeting_room_id_Z)

        expected = [reservation_A,
                    dataclasses.replace(reservation_B, meeting_room_id=meeting_room_id_Z),
                    reservation_C]

        actual = [self.repository.find_by_id(reservation_A.id),
                  self.repository.find_by_id(reservation_B.id),
                  self.repository.find_by_id(reservation_C.id)]

        assert actual == expected
