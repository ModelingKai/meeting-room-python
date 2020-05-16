import datetime
from dataclasses import dataclass

from src.domain.reservation.reservation import Reservation
from src.presentation.cli.cli_util.success_message import SuccessMessage
from src.usecase.employee.find_employee_command import FindEmployeeCommand
from src.usecase.employee.find_employee_usecase import FindEmployeeUseCase
from src.usecase.meeting_room.find_meeting_room_commnad import FindMeetingRoomCommand
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase


@dataclass
class SuccessMessageBuilder:
    find_meeting_room_usecase: FindMeetingRoomUseCase
    find_employee_usecase: FindEmployeeUseCase

    def build(self, reservation: Reservation) -> SuccessMessage:
        meeting_room_name = self.find_meeting_room_name(reservation)
        reserver_name = self.find_reserver_name(reservation)
        number_of_participants = reservation.number_of_participants.value

        year = 2020
        month = 4
        day = 2
        start_time = datetime.time(13, 00)
        end_time = datetime.time(14, 00)

        return SuccessMessage(
            year,
            month,
            day,
            start_time,
            end_time,
            meeting_room_name,
            reserver_name,
            number_of_participants
        )

    def find_reserver_name(self, reservation: Reservation) -> str:
        find_employee_command = FindEmployeeCommand(employee_id=reservation.reserver_id.value)
        reserver = self.find_employee_usecase.find_employee(find_employee_command)

        return reserver.name

    def find_meeting_room_name(self, reservation: Reservation) -> str:
        find_meeting_room_command = FindMeetingRoomCommand(meeting_room_id=reservation.meeting_room_id.value)
        meeting_room = self.find_meeting_room_usecase.find_meeting_room(find_meeting_room_command)

        return meeting_room.name
