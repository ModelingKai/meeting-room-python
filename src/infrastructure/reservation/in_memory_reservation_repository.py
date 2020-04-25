from typing import Dict

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository


class InMemoryReservationRepository(ReservationRepository):
    data: Dict[ReservationId, Reservation] = {}

    def reserve(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation
