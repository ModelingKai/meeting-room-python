from abc import ABCMeta, abstractmethod
from typing import Union, List

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_specification import ReservationSpecification


class ReservationRepository(metaclass=ABCMeta):
    @abstractmethod
    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def cancel_meeting_room(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        pass

    @abstractmethod
    def change_meeting_room(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def change_time_range(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def find_satisfying(self, spec: ReservationSpecification) -> List[Reservation]:
        pass
