from dataclasses import dataclass

from src.domain.reservation.reservation import Reservation
from src.presentation.response_object import ResponseObject
from src.usecase.employee.find_employee_usecase import FindEmployeeUseCase
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase


@dataclass
class ResponseObjectFactory:
    find_employee_usecase: FindEmployeeUseCase
    find_mtg_room_usecase: FindMeetingRoomUseCase

    def create(self, reservation: Reservation) -> ResponseObject:
        time_to_range = reservation.time_range_to_reserve
        start_datetime = time_to_range.start_datetime
        end_datetime = time_to_range.end_datetime

        year, month, day = start_datetime.year, start_datetime.month, start_datetime.day
        start_time, end_time = start_datetime.time(), end_datetime.time()

        reserver_name = self.find_employee_usecase.find_by_id(reservation.reserver_id).name
        meeting_room_name = self.find_mtg_room_usecase.find_by_id(reservation.meeting_room_id).name

        number_of_participants = reservation.number_of_participants.value

        return ResponseObject(year,
                              month,
                              day,
                              start_time,
                              end_time,
                              meeting_room_name,
                              reserver_name,
                              number_of_participants)
