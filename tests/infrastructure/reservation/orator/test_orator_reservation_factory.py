import freezegun
import pytest
from orator import DatabaseManager, Model

from src.domain.employee.employee import Employee
from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.errors import NotFoundEmployeeIdError
from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_factory import ReservationFactory
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.employee.orator.orator_employee_model import OratorEmployeeModel
from src.infrastructure.employee.orator.orator_employee_repository import OratorEmployeeRepository
from src.infrastructure.meeting_room.orator.orator_meeting_room_model import OratorMeetingRoomModel
from src.infrastructure.meeting_room.orator.orator_meeting_room_repository import OratorMeetingRoomRepository
from src.usecase.meeting_room.errors import NotFoundMeetingRoomIdError
from tests.usecase.reservation.orator.migrate_in_memory import TEST_DB_CONFIG, migrate_in_memory


class TestOratorReservationFactory:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)
        Model.set_connection_resolver(database_manager)
        migrate_in_memory(database_manager)

        employee_repository = OratorEmployeeRepository()
        employee_id = EmployeeId('001')
        employee = Employee(employee_id, 'Bob')
        OratorEmployeeModel.to_orator_model(employee).save()

        meeting_room_repository = OratorMeetingRoomRepository()
        meeting_room_id = MeetingRoomId('A')
        meeting_room = MeetingRoom(meeting_room_id, '大会議室')
        OratorMeetingRoomModel.to_orator_model(meeting_room).save()

        self.reservation_factory = ReservationFactory(meeting_room_repository, employee_repository)

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_存在しない会議室IDを持つReservationが作れてはいけない(self):
        with pytest.raises(NotFoundMeetingRoomIdError):
            self.reservation_factory.create(date='20200402',
                                            start_time='1100',
                                            end_time='1300',
                                            meeting_room_id='Z',
                                            reserver_id='001',
                                            number_of_participants='5')

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_存在しない社員IDを持つReservationが作れてはいけない(self):
        with pytest.raises(NotFoundEmployeeIdError):
            self.reservation_factory.create(date='20200402',
                                            start_time='1100',
                                            end_time='1300',
                                            meeting_room_id='A',
                                            reserver_id='999',
                                            number_of_participants='5')

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_Reservationが作れるよ(self):
        reservation_id = 'データクラス同士の比較のために、やっているよ'

        actual = self.reservation_factory.create(date='20200402',
                                                 start_time='1100',
                                                 end_time='1300',
                                                 meeting_room_id='A',
                                                 reserver_id='001',
                                                 number_of_participants='5',
                                                 reservation_id=reservation_id)

        expected = Reservation(ReservationId(reservation_id),
                               TimeRangeToReserve(使用日時(2020, 4, 2, 11, 00), 使用日時(2020, 4, 2, 13, 00)),
                               NumberOfParticipants(5),
                               MeetingRoomId('A'),
                               EmployeeId('001'))

        assert actual == expected
