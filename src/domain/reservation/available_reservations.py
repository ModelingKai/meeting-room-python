from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from src.domain.reservation.errors import NotAvailableReservationError
from src.domain.reservation.reservation import Reservation


@dataclass(frozen=True)
class AvailableReservations:
    __values: List[Reservation] = field(default_factory=list)

    def __post_init__(self):
        for reservation in self.__values:
            if not reservation.is_available():
                raise NotAvailableReservationError('有効ではない予約が含まれています')

    def add(self, reservation: Reservation) -> AvailableReservations:
        return AvailableReservations(self.__values + [reservation])
