from __future__ import annotations

from dataclasses import dataclass
from typing import Union, List

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.reservation.reservation_specification import ReservationSpecification
from src.infrastructure.reservation.orator.orator_reservation_model import OratorReservationModel


@dataclass
class OratorReservationRepository(ReservationRepository):
    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservationModel.to_orator_model(reservation)

        orator_reservation.save()

    def cancel_meeting_room(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservationModel.to_orator_model(reservation)

        OratorReservationModel.update(orator_reservation, reservation_status=reservation.reservation_status.value)

    def find_satisfying(self, specification: ReservationSpecification) -> List[Reservation]:
        return list(filter(specification.satisfying_elements_from, OratorReservationModel.all()))

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        orator_reservation = OratorReservationModel.find(reservation_id.value)

        if orator_reservation is None:
            return None

        return OratorReservationModel.to_reservation(orator_reservation)

    def change_meeting_room(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservationModel.to_orator_model(reservation)

        update_param_dict = dict(meeting_room_id=reservation.meeting_room_id.value)
        OratorReservationModel.update(orator_reservation, update_param_dict)

    def change_time_range(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservationModel.to_orator_model(reservation)

        update_param_dict = dict(
            start_datetime=OratorReservationModel.to_datetime(reservation.time_range_to_reserve.start_datetime),
            end_datetime=OratorReservationModel.to_datetime(reservation.time_range_to_reserve.end_datetime))

        OratorReservationModel.update(orator_reservation, update_param_dict)
