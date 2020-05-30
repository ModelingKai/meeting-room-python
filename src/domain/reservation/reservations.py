from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_status import ReservationStatus


@dataclass(frozen=True)
class Reservations:
    __values: List[Reservation] = field(default_factory=list)

    def add(self, reservation: Reservation) -> Reservations:
        return Reservations(self.__values + [reservation])

    def availables(self) -> Reservations:
        return Reservations([r for r in self.__values if r.reservation_status == ReservationStatus.Available])
