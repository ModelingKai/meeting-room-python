import dataclasses

from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve


@dataclasses.dataclass
class ChangeTimeRangeUsecase:
    reservation_repository: ReservationRepository
    reservation_domain_service: ReservationDomainService

    def change_time_range(self, reservation_id: ReservationId, time_range_to_reserve: TimeRangeToReserve) -> None:
        reservation = self.reservation_repository.find_by_id(reservation_id)

        changed_reservation = reservation.change_time_range(time_range_to_reserve)

        self.reservation_repository.change_meeting_room(changed_reservation)
