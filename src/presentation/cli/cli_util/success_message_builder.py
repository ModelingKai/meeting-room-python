import datetime

from src.domain.reservation.reservation import Reservation
from src.presentation.cli.cli_util.success_message import SuccessMessage


class SuccessMessageBuilder:
    def build(self, reservation: Reservation) -> SuccessMessage:
        return SuccessMessage(
            2020,
            4,
            2,
            datetime.time(13, 00),
            datetime.time(14, 00),
            '大会議室',
            'Bob',
            4
        )
