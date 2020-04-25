from dataclasses import dataclass

from src.domain.reservation.errors import 既に予約されているものがあるよエラー
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_repository import ReservationRepository


@dataclass
class ReserveMeetingRoomUsecase():
    repository: ReservationRepository

    def reserve_meeting_room(self, reservation: Reservation) -> None:
        # かぶりがあったら、こらーという

        # リポジトリからデータを見に行く必要がある
        service = ReservationDomainService(self.repository)
        if service.is_かぶり(reservation):
            raise 既に予約されているものがあるよエラー(f'先約があるのでごめん！: {reservation.予約時間帯}と{reservation.meeting_room_id}')

        self.repository.reserve(reservation)
