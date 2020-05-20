from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Union, List

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.reservation.reservation_specification import ReservationSpecification
from src.domain.reservation.reservation_status import ReservationStatus
from src.infrastructure.reservation.orator.orator_reservation_model import OratorReservationModel


@dataclass
class OratorReservationRepository(ReservationRepository):
    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservationModel.to_orator_model(reservation)

        orator_reservation.save()

    def cancel_meeting_room(self, reservation: Reservation) -> None:
        OratorReservationModel \
            .where('id', '=', reservation.id.value) \
            .update(reservation_status=reservation.reservation_status.value)

        # これでもOKだよ 参考: https://orator-orm.com/docs/0.9/orm.html#updating-a-retrieved-model
        # orator_reservation = OratorReservationModel.find(reservation.id.value)
        # orator_reservation.reservation_status = ReservationStatus.Canceled.value
        # orator_reservation.save()

    def find_satisfying(self, specification: ReservationSpecification) -> List[Reservation]:
        # フィルタリング → 再構成 は OK! だが 再構成 → フィルタリング は、再構成時点で過去予約はダメよエラーになるぞ！
        satisfied_orator_reservation_models = []

        for orator_model in OratorReservationModel.all():
            is_reserved = orator_model.reservation_status == ReservationStatus.Reserved.value

            start_datetime = datetime.datetime.strptime(orator_model.start_datetime, '%Y-%m-%d %H:%M:%S')
            is_future = start_datetime > datetime.datetime.now()

            if is_reserved and is_future:
                satisfied_orator_reservation_models.append(orator_model)

        return [OratorReservationModel.to_reservation(o) for o in satisfied_orator_reservation_models]

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        orator_reservation = OratorReservationModel.find(reservation_id.value)

        if orator_reservation is None:
            return None

        return OratorReservationModel.to_reservation(orator_reservation)

    def change_meeting_room(self, reservation: Reservation) -> None:
        OratorReservationModel \
            .where('id', '=', reservation.id.value) \
            .update(meeting_room_id=reservation.meeting_room_id.value)

    def change_time_range(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservationModel.to_orator_model(reservation)

        update_param_dict = dict(
            start_datetime=OratorReservationModel.to_datetime(reservation.time_range_to_reserve.start_datetime),
            end_datetime=OratorReservationModel.to_datetime(reservation.time_range_to_reserve.end_datetime))

        OratorReservationModel.update(orator_reservation, update_param_dict)
