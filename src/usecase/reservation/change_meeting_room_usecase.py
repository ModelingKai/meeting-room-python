from dataclasses import dataclass

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository


@dataclass
class ChangeMeetingRoomUseCase:
    reservation_repository: ReservationRepository

    def change_meeting_room(self, reservation_id: ReservationId, new_meeting_room_id: MeetingRoomId) -> None:
        reservation = self.reservation_repository.find_by_id(reservation_id)

        changed_reservation = reservation.change_meeting_room(new_meeting_room_id)

        self.reservation_repository.change_meeting_room(changed_reservation)
