from abc import ABCMeta, abstractmethod

from src.domain.reservation.reservation import Reservation


class ReservationRepository(metaclass=ABCMeta):
    @abstractmethod
    def reserve(self, reservation: Reservation) -> None:
        pass
