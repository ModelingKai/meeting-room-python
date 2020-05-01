from abc import ABCMeta, abstractmethod
from typing import List, Union

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId


class ReservationRepository(metaclass=ABCMeta):
    @abstractmethod
    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def cancel_meeting_room(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def find_all(self) -> List[Reservation]:
        pass

    @abstractmethod
    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        pass
