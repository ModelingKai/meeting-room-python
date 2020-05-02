from typing import Dict, List, Union

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository


class InMemoryReservationRepository(ReservationRepository):
    data: Dict[ReservationId, Reservation] = {}

    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def find_all(self) -> List[Reservation]:
        return list(self.data.values())

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        return self.data.get(reservation_id)

    def change_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def cancel_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def change_time_range(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation
