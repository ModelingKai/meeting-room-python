from dataclasses import dataclass

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.shared.clock import Clock


@dataclass
class ReservationDomainService:
    reservation_repository: ReservationRepository
    clock: Clock

    def can_not_reserve(self, reservation: Reservation) -> bool:
        # TODO: 性能面を考えると、クエリをカスタマイズしたほうがよさそう
        available_reservations = self.reservation_repository.find_available_reservations(self.clock)

        for not_canceled_reservation in available_reservations:
            if not_canceled_reservation.is_かぶり(reservation):
                return True

        return False
