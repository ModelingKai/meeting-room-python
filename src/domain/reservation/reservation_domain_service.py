import datetime
from dataclasses import dataclass

from src.domain.reservation.available_reservation_specification import AvailableReservationSpecification
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.shared.clock import Clock


@dataclass
class ReservationDomainService:
    reservation_repository: ReservationRepository
    clock: Clock

    def can_not_reserve(self, reservation: Reservation) -> bool:
        # Memo:　外から差し込むかと迷ったが、can_not_reserve は有効な予約を取得するということを明示したいので、
        # あえてこの中で生成する
        available_spec = AvailableReservationSpecification(datetime.datetime.now())
        # TODO: 性能面を考えると、クエリをカスタマイズしたほうがよさそう
        available_reservations = self.reservation_repository.find_satisfying(available_spec)

        for not_canceled_reservation in available_reservations:
            if not_canceled_reservation.is_かぶり(reservation):
                return True

        return False
