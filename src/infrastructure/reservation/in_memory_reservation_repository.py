from typing import Dict, Union

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from tests.usecase.reservation.available_reservations import AvailableReservations


class InMemoryReservationRepository(ReservationRepository):
    def __init__(self):
        self.data: Dict[ReservationId, Reservation] = {}

    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def find_available_reservations(self) -> AvailableReservations:
        available_reservations = AvailableReservations()

        for r in self.data.values():
            available_reservations = available_reservations.add(r)

        return available_reservations
        # 下記の実装は、とりあえず、残しておく
        # now = datetime.datetime.now()
        #
        # is_available_reservation = lambda x: x.reservation_status == ReservationStatus.Reserved \
        #                                      and x.time_range_to_reserve.start_datetime > now
        #
        # available_reservations = list(filter(is_available_reservation, self.data.values()))
        #
        # return available_reservations

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        return self.data.get(reservation_id)

    def change_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def cancel_meeting_room(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation

    def change_time_range(self, reservation: Reservation) -> None:
        self.data[reservation.id] = reservation
