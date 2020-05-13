import datetime
from dataclasses import dataclass

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_specification import ReservationSpecification
from src.domain.reservation.reservation_status import ReservationStatus


@dataclass
class AvailableReservationSpecification(ReservationSpecification):
    """
    有効な予約仕様
    """
    now: datetime.datetime

    def satisfying_elements_from(self, reservation: Reservation) -> bool:
        return reservation.reservation_status == ReservationStatus.Reserved \
               and reservation.time_range_to_reserve.start_datetime > self.now
