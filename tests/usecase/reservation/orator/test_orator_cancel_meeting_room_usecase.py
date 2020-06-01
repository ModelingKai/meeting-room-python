import dataclasses

from orator import DatabaseManager, Model

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.reservation_status import ReservationStatus
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.cancel_meeting_room_usecase import CancelMeetingRoomUsecase
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder
from tests.usecase.reservation.orator.migrate_in_memory import TEST_DB_CONFIG, migrate_in_memory


class TestOratorCancelMeetingRoomUsecase:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)

        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

        self.repository = OratorReservationRepository()
        self.usecase = CancelMeetingRoomUsecase(self.repository)

    def test_指定した予約のみがキャンセルとなること(self):
        builder = DummyReservationBuilder()
        reservation_A = builder.with_meeting_room_id(MeetingRoomId('A')).build()
        reservation_B = builder.with_meeting_room_id(MeetingRoomId('B')).build()
        reservation_C = builder.with_meeting_room_id(MeetingRoomId('C')).build()

        self.repository.reserve_new_meeting_room(reservation_A)
        self.repository.reserve_new_meeting_room(reservation_B)
        self.repository.reserve_new_meeting_room(reservation_C)

        self.usecase.cancel_meeting_room(reservation_B.id)

        expected = [reservation_A,
                    dataclasses.replace(reservation_B, reservation_status=ReservationStatus.Canceled),
                    reservation_C]

        actual = [self.repository.find_by_id(reservation_A.id),
                  self.repository.find_by_id(reservation_B.id),
                  self.repository.find_by_id(reservation_C.id)]

        assert actual == expected
