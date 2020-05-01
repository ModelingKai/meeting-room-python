from dataclasses import dataclass

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from src.usecase.reservation.errors import NotFoundReservationError, その会議室はその時間帯では予約ができませんよエラー


@dataclass
class ChangeMeetingRoomUseCase:
    reservation_repository: ReservationRepository
    reservation_domain_service: ReservationDomainService

    def change_meeting_room(self, reservation_id: ReservationId, new_meeting_room_id: MeetingRoomId) -> None:
        reservation = self.reservation_repository.find_by_id(reservation_id)

        if reservation is None:
            raise NotFoundReservationError('そんな予約はないんやで？')

        changed_reservation = reservation.change_meeting_room(new_meeting_room_id)

        if self.reservation_domain_service.can_not_reserve(changed_reservation):
            raise その会議室はその時間帯では予約ができませんよエラー('ダメだよ')

        self.reservation_repository.change_meeting_room(changed_reservation)
