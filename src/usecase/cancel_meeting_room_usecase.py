from dataclasses import dataclass

from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository


@dataclass
class CancelMeetingRoomUsecase:
    reservation_repository: ReservationRepository

    def cancel_meeting_room(self, reservation_id: ReservationId) -> None:
        reservation = self.reservation_repository.find_by_id(reservation_id)

        # いきなりリポジトリでCancelを呼んでもいいのではないか
        # なんでダメなのか
        canceled_reservation = reservation.cancel()

        self.reservation_repository.reserve(canceled_reservation)
