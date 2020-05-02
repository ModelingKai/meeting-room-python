import uuid
from pathlib import Path

import freezegun
import pytest
from orator import DatabaseManager, Schema
from orator.schema import Blueprint

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase


class TestOratorReserveMeetingRoomUsecase:
    TEST_DB_CONFIG = {
        'test': {
            'driver': 'sqlite',
            'database': 'test_orator_db.sqlite3',
        }
    }

    def init_test_db(self):
        schema = Schema(DatabaseManager(self.TEST_DB_CONFIG))

        table_name = 'reservations'
        schema.drop_if_exists(table_name)

        with schema.create(table_name) as table:
            table: Blueprint

            table.string('id').unique()
            table.string('meeting_room_id')
            table.string('reserver_id')
            table.enum('reservation_status', ['予約中', 'キャンセル済み'])
            table.integer('number_of_participants')
            table.datetime('start_datetime')
            table.datetime('end_datetime')

            table.datetime('created_at')
            table.datetime('updated_at')

    def setup(self):
        self.init_test_db()
        database_manager = DatabaseManager(self.TEST_DB_CONFIG)

        self.repository = OratorReservationRepository(database_manager)
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ReserveMeetingRoomUsecase(self.repository, domain_service)

    def teardown(self):
        Path(self.TEST_DB_CONFIG['test']['database']).unlink()

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation(self) -> Reservation:
        """不正でないReservationインスタンスを作成するだけのfixture"""
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId(str(uuid.uuid4())),
                           EmployeeId(str(uuid.uuid4())))

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_予約ができること_正常系(self, reservation):
        self.usecase.reserve_meeting_room(reservation)

        assert reservation == self.repository.find_by_id(reservation.id)
