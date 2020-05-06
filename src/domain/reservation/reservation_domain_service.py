from dataclasses import dataclass

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.reservation.reservation_status import ReservationStatus


@dataclass
class ReservationDomainService:
    reservation_repository: ReservationRepository

    def can_not_reserve(self, reservation: Reservation) -> bool:
        # TODO: 性能面を考えると、クエリをカスタマイズしたほうがよさそう
        all_reservations = self.reservation_repository.find_available_reservations()

        # 変数名的には NotCanceled だけど、フィルタ条件的には Reservedである なのはツラい
        not_canceled_reservation = [r for r in all_reservations if r.reservation_status == ReservationStatus.Reserved]

        for not_canceled_reservation in not_canceled_reservation:
            if not_canceled_reservation.is_かぶり(reservation):
                return True

        return False
