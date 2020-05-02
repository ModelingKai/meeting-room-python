import dataclasses

from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.usecase.reservation.errors import NotFoundReservationError, その会議室はその時間帯では予約ができませんよエラー


@dataclasses.dataclass
class ChangeTimeRangeUsecase:
    reservation_repository: ReservationRepository
    reservation_domain_service: ReservationDomainService

    def change_time_range(self, reservation_id: ReservationId, time_range_to_reserve: TimeRangeToReserve) -> None:
        reservation = self.reservation_repository.find_by_id(reservation_id)

        if reservation is None:
            raise NotFoundReservationError('そんな予約はないんやで？')

        changed_reservation = reservation.change_time_range(time_range_to_reserve)

        if self.reservation_domain_service.can_not_reserve(changed_reservation):
            raise その会議室はその時間帯では予約ができませんよエラー('ダメだよ')

        self.reservation_repository.change_time_range(changed_reservation)
