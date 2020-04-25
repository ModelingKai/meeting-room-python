from dataclasses import dataclass


@dataclass(frozen=True)
class ReservationId:
    value: str
