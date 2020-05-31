import dataclasses
import datetime

import freezegun
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

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_指定した予約のみがキャンセルとなること(self):
        builder = DummyReservationBuilder(datetime.datetime.now())
        reservation_0402_A = builder.with_meeting_room_id(MeetingRoomId('A')).build()
        reservation_0402_B = builder.with_meeting_room_id(MeetingRoomId('B')).build()
        reservation_0402_C = builder.with_meeting_room_id(MeetingRoomId('C')).build()

        self.repository.reserve_new_meeting_room(reservation_0402_A)
        self.repository.reserve_new_meeting_room(reservation_0402_B)
        self.repository.reserve_new_meeting_room(reservation_0402_C)

        self.usecase.cancel_meeting_room(reservation_0402_B.id)

        expected = [reservation_0402_A,
                    dataclasses.replace(reservation_0402_B, reservation_status=ReservationStatus.Canceled),
                    reservation_0402_C]

        actual = [self.repository.find_by_id(reservation_0402_A.id),
                  self.repository.find_by_id(reservation_0402_B.id),
                  self.repository.find_by_id(reservation_0402_C.id)]

        assert actual == expected
