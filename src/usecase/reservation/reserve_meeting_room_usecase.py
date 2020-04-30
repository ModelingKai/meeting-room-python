from dataclasses import dataclass

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_repository import ReservationRepository
from src.usecase.reservation.errors import その会議室はその時間帯では予約ができませんよエラー


@dataclass
class ReserveMeetingRoomUsecase:
    repository: ReservationRepository
    domain_service: ReservationDomainService

    def reserve_meeting_room(self, reservation: Reservation) -> None:
        if self.domain_service.can_not_reserve(reservation):
            raise その会議室はその時間帯では予約ができませんよエラー(
                f'先約があるのでごめん！: {reservation.time_range_to_reserve}と{reservation.meeting_room_id}')

        self.repository.reserve_new_meeting_room(reservation)
