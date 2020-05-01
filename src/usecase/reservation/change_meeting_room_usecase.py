from dataclasses import dataclass

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository


@dataclass
class ChangeMeetingRoomUseCase:
    reservation_repository: ReservationRepository

    def change_meeting_room(self, reservation_id: ReservationId, new_meeting_room_id: MeetingRoomId) -> None:
        pass
