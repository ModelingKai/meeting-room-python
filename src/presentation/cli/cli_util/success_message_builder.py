import datetime

from src.domain.reservation.reservation import Reservation
from src.presentation.cli.cli_util.success_message import SuccessMessage


class SuccessMessageBuilder:
    def build(self, reservation: Reservation) -> SuccessMessage:
        meeting_room_name = '大会議室'
        reserver_name = 'Bob'
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
