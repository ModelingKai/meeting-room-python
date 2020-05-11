from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from src.domain.reservation.reservation import Reservation


@dataclass(frozen=True)
class AvailableReservations:
    values: List[Reservation] = field(default_factory=list)

    def add(self, r: Reservation) -> AvailableReservations:
        return AvailableReservations(self.values + [r])

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: int) -> Reservation:
        return self.values[index]
