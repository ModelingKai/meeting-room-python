from dataclasses import dataclass

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_repository import ReservationRepository


@dataclass
class ReserveMeetingRoomUsecase():
    repository: ReservationRepository

    def reserve_meeting_room(self, reservation: Reservation) -> None:
        self.repository.reserve(reservation)
