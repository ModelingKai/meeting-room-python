from dataclasses import dataclass, field
from typing import Dict, List, Optional

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.reservation.reservation_specification import ReservationSpecification


@dataclass
class InMemoryReservationRepository(ReservationRepository):
    data: Dict[ReservationId, Reservation] = field(default_factory=dict)

    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def find_satisfying(self, specification: ReservationSpecification) -> List[Reservation]:
        available_reservations = list(filter(specification.satisfying_elements_from, self.data.values()))

        return available_reservations

    def find_by_id(self, reservation_id: ReservationId) -> Optional[Reservation]:
        return self.data.get(reservation_id)

    def change_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def cancel_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def change_time_range(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation
