import uuid
from dataclasses import dataclass

import freezegun
import pytest

from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository
from src.domain.employee.errors import NotFoundEmployeeIdError
from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.employee.in_memory_employee_repository import InMemoryEmployeeRepository
from src.infrastructure.meeting_room.in_memory_meeting_room_repository import InMemoryMeetingRoomRepository
from src.usecase.meeting_room.errors import NotFoundMeetingRoomIdError


@dataclass
class ReservationFactory(object):
    meeting_room_repository: MeetingRoomRepository
    employee_repository: EmployeeRepository

    def create(self,
               date: str,
               start_time: str,
               end_time: str,
               meeting_room_id: str,
               reserver_id: str,
               number_of_participants: str,
               ):
        meeting_room_id = MeetingRoomId(meeting_room_id)
        meeting_room = self.meeting_room_repository.find_by_id(meeting_room_id)

        if meeting_room is None:
            raise NotFoundMeetingRoomIdError('そんな会議室IDはありませんよ')

        reserver_id = EmployeeId(reserver_id)
        employee = self.employee_repository.find_by_id(reserver_id)

        if employee is None:
            raise NotFoundEmployeeIdError('そんな社員IDはありませんよ')

        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])

        start_hour = int(start_time[:2])
        start_minute = int(start_time[2:4])

        end_hour = int(end_time[:2])
        end_minute = int(end_time[2:4])

        start_使用日時 = 使用日時(year, month, day, start_hour, start_minute)
        end_使用日時 = 使用日時(year, month, day, end_hour, end_minute)

        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(start_使用日時, end_使用日時),
                                  NumberOfParticipants(int(number_of_participants)),
                                  meeting_room_id,
                                  EmployeeId(reserver_id))

        return reservation


class TestReservation:
    @freezegun.freeze_time('2020-4-1 10:00')
    def test_存在しない会議室IDを持つReservationが作れてはいけない(self):
        meeting_room_repository = InMemoryMeetingRoomRepository()
        employee_repository = InMemoryEmployeeRepository()
        reservation_factory = ReservationFactory(meeting_room_repository, employee_repository)

        with pytest.raises(NotFoundMeetingRoomIdError):
            reservation_factory.create(date='20200402',
                                       start_time='1100',
                                       end_time='1300',
                                       meeting_room_id='Z',
                                       reserver_id='001',
                                       number_of_participants='5')

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_存在しない社員IDを持つReservationが作れてはいけない(self):
        meeting_room_repository = InMemoryMeetingRoomRepository()
        employee_repository = InMemoryEmployeeRepository()

        meeting_room_id = MeetingRoomId('A')
        meeting_room = MeetingRoom(meeting_room_id, '大会議室')
        meeting_room_repository.data[meeting_room_id] = meeting_room

        reservation_factory = ReservationFactory(meeting_room_repository, employee_repository)

        with pytest.raises(NotFoundEmployeeIdError):
            reservation_factory.create(date='20200402',
                                       start_time='1100',
                                       end_time='1300',
                                       meeting_room_id='A',
                                       reserver_id='999',
                                       number_of_participants='5')
