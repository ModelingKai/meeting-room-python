from dataclasses import dataclass

from src.domain.reservation.errors import その会議室はその時間帯では予約ができませんよエラー
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_repository import ReservationRepository


@dataclass
class ReserveMeetingRoomUsecase():
    repository: ReservationRepository
    domain_service: ReservationDomainService

    def reserve_meeting_room(self, reservation: Reservation) -> None:
        if self.domain_service.is_かぶり(reservation):
            raise その会議室はその時間帯では予約ができませんよエラー(f'先約があるのでごめん！: {reservation.予約時間帯}と{reservation.meeting_room_id}')

        self.repository.reserve(reservation)
