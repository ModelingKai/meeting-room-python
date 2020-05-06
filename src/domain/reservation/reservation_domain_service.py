from dataclasses import dataclass

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_repository import ReservationRepository


@dataclass
class ReservationDomainService:
    reservation_repository: ReservationRepository

    def can_not_reserve(self, reservation: Reservation) -> bool:
        # TODO: 性能面を考えると、クエリをカスタマイズしたほうがよさそう
        available_reservations = self.reservation_repository.find_available_reservations()

        for not_canceled_reservation in available_reservations:
            if not_canceled_reservation.is_かぶり(reservation):
                return True

        return False
