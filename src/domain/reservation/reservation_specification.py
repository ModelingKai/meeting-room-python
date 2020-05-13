from abc import ABCMeta, abstractmethod

from src.domain.reservation.reservation import Reservation


class ReservationSpecification(metaclass=ABCMeta):
    """
    予約仕様
    """

    @abstractmethod
    def satisfying_elements_from(self, reservation: Reservation) -> bool:
        pass
