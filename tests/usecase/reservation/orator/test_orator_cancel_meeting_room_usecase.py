import dataclasses

import freezegun
import pytest
from orator import DatabaseManager, Model

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.cancel_meeting_room_usecase import CancelMeetingRoomUsecase
from tests.usecase.reservation.orator.migrate_in_memory import TEST_DB_CONFIG, migrate_in_memory


class TestOratorCancelMeetingRoomUsecase:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)

        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

        self.repository = OratorReservationRepository()
        self.usecase = CancelMeetingRoomUsecase(self.repository)

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation_0402_A(self) -> Reservation:
        """不正でないReservationインスタンスを作成するだけのfixture"""
        return Reservation(ReservationId('0402'),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_キャンセルができること_正常系(self, reservation_0402_A):
        # 既に予約されているデータとする
        self.repository.reserve_new_meeting_room(reservation_0402_A)

        expected = dataclasses.replace(reservation_0402_A, reservation_status=ReservationStatus.Canceled)

        self.usecase.cancel_meeting_room(reservation_0402_A.id)

        assert expected == self.repository.find_by_id(reservation_0402_A.id)

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_指定した予約のみがキャンセルとなること(self, reservation_0402_A):
        reservation_0402_B = dataclasses.replace(reservation_0402_A,
                                                 id=ReservationId('0402_B'),
                                                 meeting_room_id=MeetingRoomId('B'))

        reservation_0402_C = dataclasses.replace(reservation_0402_A,
                                                 id=ReservationId('0402_C'),
                                                 meeting_room_id=MeetingRoomId('C'))

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
