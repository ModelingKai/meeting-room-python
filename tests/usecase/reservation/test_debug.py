import freezegun
from orator import Schema, DatabaseManager
from orator.schema import Blueprint

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
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

    @freezegun.freeze_time('2020-4-1 10:00')
    def setup(self):
        self.init_debug_db()
        database_manager = DatabaseManager(self.DEBUG_DB_CONFIG)

        self.repository = OratorReservationRepository(database_manager)
        self.domain_service = ReservationDomainService(self.repository)
        self.usecase = ReserveMeetingRoomUsecase(self.repository, self.domain_service)

        self.過去のデータを混入させる()
        self.有効な予約データを登録する()
        self.未来だがキャンセル済みの予約データを登録する()

    def teardown(self):
        schema = Schema(DatabaseManager(self.DEBUG_DB_CONFIG))

        table_name = 'reservation'
        schema.drop_if_exists(table_name)

    @freezegun.freeze_time('2020-4-1 10:00')
    def 過去のデータを混入させる(self):
        r_0402 = Reservation(ReservationId('過去の予約ID'),
                             TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                             NumberOfParticipants(4),
                             MeetingRoomId('RoomA'),
                             EmployeeId('001'))

        self.usecase.reserve_meeting_room(r_0402)

    @freezegun.freeze_time('2020-4-1 10:00')
    def 有効な予約データを登録する(self):
        r_0415_予約中 = Reservation(ReservationId('有効な予約'),
                                 TimeRangeToReserve(使用日時(2020, 4, 15, 13, 00), 使用日時(2020, 4, 15, 14, 00)),
                                 NumberOfParticipants(4),
                                 MeetingRoomId('RoomA'),
                                 EmployeeId('001'))

        self.usecase.reserve_meeting_room(r_0415_予約中)

    @freezegun.freeze_time('2020-4-1 10:00')
    def 未来だがキャンセル済みの予約データを登録する(self):
        r_0414_キャンセル済み = Reservation(ReservationId('未来だがキャンセル済み'),
                                     TimeRangeToReserve(使用日時(2020, 4, 14, 13, 00), 使用日時(2020, 4, 14, 14, 00)),
                                     NumberOfParticipants(4),
                                     MeetingRoomId('RoomA'),
                                     EmployeeId('001'),
                                     ReservationStatus.Canceled)

        self.usecase.reserve_meeting_room(r_0414_キャンセル済み)

    @freezegun.freeze_time('2020-4-5 10:00')
    def test_再現(self):
        expected = [Reservation(ReservationId('有効な予約'),
                                TimeRangeToReserve(使用日時(2020, 4, 15, 13, 00), 使用日時(2020, 4, 15, 14, 00)),
                                NumberOfParticipants(4),
                                MeetingRoomId('RoomA'),
                                EmployeeId('001'))]

        assert expected == self.repository.find_all()
