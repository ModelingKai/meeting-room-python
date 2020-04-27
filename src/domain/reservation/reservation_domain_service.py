from dataclasses import dataclass
from typing import List

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_repository import ReservationRepository


@dataclass
class ReservationDomainService:
    reservation_repository: ReservationRepository

    def can_not_reserve(self, reservation: Reservation) -> bool:
        # TODO: いずれは性能面を考えると、日付で検索した方がよさそう
        reservations: List[Reservation] = self.reservation_repository.find_all()

        for exist_reservation in reservations:
            if exist_reservation.is_かぶり(reservation):
                return True

        return False
