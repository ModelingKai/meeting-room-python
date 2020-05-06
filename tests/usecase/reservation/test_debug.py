import freezegun
from orator import Schema, DatabaseManager
from orator.schema import Blueprint

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase


class TestDebug:
    DEBUG_DB_CONFIG = {
        'test': {
            'driver': 'sqlite',
            'database': 'debug_orator_db.sqlite3',
        }
    }

    def init_debug_db(self):
        schema = Schema(DatabaseManager(self.DEBUG_DB_CONFIG))

        table_name = 'reservation'
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
        self.init_debug_db()
        database_manager = DatabaseManager(self.DEBUG_DB_CONFIG)

        self.repository = OratorReservationRepository(database_manager)
        self.domain_service = ReservationDomainService(self.repository)
        self.usecase = ReserveMeetingRoomUsecase(self.repository, self.domain_service)

    def teardown(self):
        schema = Schema(DatabaseManager(self.DEBUG_DB_CONFIG))

        table_name = 'reservation'
        schema.drop_if_exists(table_name)

    @freezegun.freeze_time('2020-6-1 10:00')
    def test_再現(self):
        @freezegun.freeze_time('2020-4-1 10:00')
        def 過去のデータを混入させる():
            r_0402 = Reservation(ReservationId('過去の予約ID'),
                                 TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                 NumberOfParticipants(4),
                                 MeetingRoomId('RoomA'),
                                 EmployeeId('001'))

            self.usecase.reserve_meeting_room(r_0402)

        過去のデータを混入させる()

        # 未来かつ、キャンセル済みでない、予約がすべて取れればよい！
        self.repository.find_all()
