import uuid
from dataclasses import dataclass

from src.domain.employee.employee_id import EmployeeId
from src.domain.employee.employee_repository import EmployeeRepository
from src.domain.employee.errors import NotFoundEmployeeIdError
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
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
               reservation_id: str = str(uuid.uuid4())
               ) -> Reservation:

        employee = self.employee_repository.find_by_id(EmployeeId(reserver_id))

        if employee is None:
            raise NotFoundEmployeeIdError('そんな社員IDはありませんよ')

        meeting_room = self.meeting_room_repository.find_by_id(MeetingRoomId(meeting_room_id))

        if meeting_room is None:
            raise NotFoundMeetingRoomIdError('そんな会議室IDはありませんよ')

        year, month, day = int(date[:4]), int(date[4:6]), int(date[6:8])

        start_hour = int(start_time[:2])
        start_minute = int(start_time[2:4])

        end_hour = int(end_time[:2])
        end_minute = int(end_time[2:4])

        start_使用日時 = 使用日時(year, month, day, start_hour, start_minute)
        end_使用日時 = 使用日時(year, month, day, end_hour, end_minute)

        return Reservation(ReservationId(reservation_id),
                           TimeRangeToReserve(start_使用日時, end_使用日時),
                           NumberOfParticipants(int(number_of_participants)),
                           meeting_room.id,
                           employee.id)
