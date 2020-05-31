import dataclasses

import freezegun
from orator import DatabaseManager, Model

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.change_time_range_usecase import ChangeTimeRangeUsecase
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder
from tests.usecase.reservation.orator.migrate_in_memory import migrate_in_memory, TEST_DB_CONFIG


class TestOratorChangeTimeRangeUsecase:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)
        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

        self.repository = OratorReservationRepository()
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ChangeTimeRangeUsecase(self.repository, domain_service)

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_指定した予約の予約時間帯を変更できること(self):
        builder = DummyReservationBuilder()
        reservation_A = builder.with_meeting_room_id(MeetingRoomId('A')).build()
        reservation_B = builder.with_meeting_room_id(MeetingRoomId('B')).build()
        reservation_C = builder.with_meeting_room_id(MeetingRoomId('C')).build()

        self.repository.reserve_new_meeting_room(reservation_A)
        self.repository.reserve_new_meeting_room(reservation_B)
        self.repository.reserve_new_meeting_room(reservation_C)

        new_time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 9, 15, 00), 使用日時(2020, 4, 9, 17, 00))
        self.usecase.change_time_range(reservation_B.id, new_time_range_to_reserve)

        expected = [reservation_A,
                    dataclasses.replace(reservation_B, time_range_to_reserve=new_time_range_to_reserve),
                    reservation_C]

        actual = [self.repository.find_by_id(reservation_A.id),
                  self.repository.find_by_id(reservation_B.id),
                  self.repository.find_by_id(reservation_C.id)]

        assert actual == expected
