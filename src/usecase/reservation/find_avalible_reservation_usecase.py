import datetime
from dataclasses import dataclass
from typing import Optional, List

from src.domain.reservation.available_reservation_specification import AvailableReservationSpecification
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_repository import ReservationRepository


@dataclass
class FindAvailableReservationsUsecase:
    repository: ReservationRepository

    def find_available_reservations(self) -> Optional[List[Reservation]]:
        # 実行時のdatetimeを基準すべきだと思うので、ここでインスタンス化している
        specification = AvailableReservationSpecification(datetime.datetime.now())

        return self.repository.find_satisfying(specification)
