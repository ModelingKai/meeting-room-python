from abc import ABCMeta, abstractmethod
from typing import List

from src.domain.reservation.reservation import Reservation


class ReservationRepository(metaclass=ABCMeta):
    @abstractmethod
    def reserve(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def find_all(self) -> List[Reservation]:
        pass
