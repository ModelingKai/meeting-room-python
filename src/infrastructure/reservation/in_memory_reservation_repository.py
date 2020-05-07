from typing import Dict, Union

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.shared.clock import Clock
from tests.usecase.reservation.available_reservations import AvailableReservations


class InMemoryReservationRepository(ReservationRepository):
    def __init__(self):
        self.data: Dict[ReservationId, Reservation] = {}

    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def find_available_reservations(self, clock: Clock) -> AvailableReservations:
        available_reservations = [r for r in self.data.values() if r.is_available(clock.now())]

        return AvailableReservations(available_reservations)

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        return self.data.get(reservation_id)

    def change_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def cancel_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def change_time_range(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation
