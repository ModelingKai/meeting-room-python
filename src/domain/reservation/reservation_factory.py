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
class ReservationFactory:
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

        reservation_id = self._create_reservation_id(reservation_id)
        time_range_to_reserve = self._create_time_range_to_reserve(date, end_time, start_time)
        number_of_participants = self._create_number_of_participants(number_of_participants)
        meeting_room_id = self._create_meeting_room_id(meeting_room_id)
        employee_id = self._create_employee_id(reserver_id)

        return Reservation(reservation_id,
                           time_range_to_reserve,
                           number_of_participants,
                           meeting_room_id,
                           employee_id)

    def _create_reservation_id(self, reservation_id: str) -> ReservationId:
        return ReservationId(reservation_id)

    def _create_number_of_participants(self, number_of_participants: str) -> NumberOfParticipants:
        return NumberOfParticipants(int(number_of_participants))

    def _create_meeting_room_id(self, meeting_room_id: str) -> MeetingRoomId:
        meeting_room = self.meeting_room_repository.find_by_id(MeetingRoomId(meeting_room_id))

        if meeting_room is None:
            raise NotFoundMeetingRoomIdError('そんな会議室IDはありませんよ')

        return meeting_room.id

    def _create_employee_id(self, reserver_id: str) -> EmployeeId:
        employee = self.employee_repository.find_by_id(EmployeeId(reserver_id))

        if employee is None:
            raise NotFoundEmployeeIdError('そんな社員IDはありませんよ')

        return employee.id

    def _create_time_range_to_reserve(self, date: str, end_time: str, start_time: str) -> TimeRangeToReserve:
        year, month, day = int(date[:4]), int(date[4:6]), int(date[6:8])
        start_hour, start_minute = int(start_time[:2]), int(start_time[2:4])
        end_hour, end_minute = int(end_time[:2]), int(end_time[2:4])

        start_使用日時 = 使用日時(year, month, day, start_hour, start_minute)
        end_使用日時 = 使用日時(year, month, day, end_hour, end_minute)

        return TimeRangeToReserve(start_使用日時, end_使用日時)
