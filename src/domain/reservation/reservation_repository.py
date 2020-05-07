from abc import ABCMeta, abstractmethod
from typing import Union

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.shared.clock import Clock
from tests.usecase.reservation.available_reservations import AvailableReservations


class ReservationRepository(metaclass=ABCMeta):
    @abstractmethod
    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def cancel_meeting_room(self, reservation: Reservation) -> None:
        pass

    @abstractmethod
    def find_available_reservations(self, clock: Clock) -> AvailableReservations:
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
