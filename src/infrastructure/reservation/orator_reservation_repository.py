from typing import Union, List

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository


class OratorReservationRepository(ReservationRepository):

    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        pass

    def cancel_meeting_room(self, reservation: Reservation) -> None:
        pass

    def find_all(self) -> List[Reservation]:
        pass

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        pass

    def change_meeting_room(self, reservation: Reservation) -> None:
        pass
