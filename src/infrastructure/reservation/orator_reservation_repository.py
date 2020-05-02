from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Union, List

from orator import DatabaseManager, Model

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時


class OratorReservation(Model):
    __table__ = 'reservations'

    def __repr__(self) -> str:
        # ださいけど、情報がわかりやすくなるので実装している
        tmp = ', '.join([f'{k}={v}' for k, v in self.to_dict().items()])
        repr_like_dataclass = f'{self.__class__.__name__}({tmp})'

        return repr_like_dataclass

    @classmethod
    def to_reservation(cls, source: OratorReservation) -> Reservation:
        start_yyyy_mm_dd_HH_MM = datetime.datetime.strptime(source.start_datetime, '%Y-%m-%d %H:%M:%S').timetuple()[:5]
        end_yyyy_mm_dd_HH_MM = datetime.datetime.strptime(source.end_datetime, '%Y-%m-%d %H:%M:%S').timetuple()[:5]
        time_range_to_reserve = TimeRangeToReserve(使用日時(*start_yyyy_mm_dd_HH_MM), 使用日時(*end_yyyy_mm_dd_HH_MM))

        return Reservation(ReservationId(source.id),
                           time_range_to_reserve,
                           NumberOfParticipants(source.number_of_participants),
                           MeetingRoomId(source.meeting_room_id),
                           EmployeeId(source.reserver_id),
                           ReservationStatus.from_str(source.reservation_status))

    @classmethod
    def to_datetime(cls, from_: 使用日時) -> datetime.datetime:
        return datetime.datetime(from_.year, from_.month, from_.day, from_.hour, from_.minute)

    @classmethod
    def to_orator_model(cls, reservation: Reservation) -> OratorReservation:
        orator_reservation = OratorReservation()
        orator_reservation.id = reservation.id.value
        orator_reservation.meeting_room_id = reservation.meeting_room_id.value
        orator_reservation.reserver_id = reservation.reserver_id.value

        orator_reservation.reservation_status = reservation.reservation_status.value

        orator_reservation.number_of_participants = reservation.number_of_participants.value

        orator_reservation.start_datetime = OratorReservation.to_datetime(reservation.time_range_to_reserve.start)
        orator_reservation.end_datetime = OratorReservation.to_datetime(reservation.time_range_to_reserve.end)

        return orator_reservation


@dataclass
class OratorReservationRepository(ReservationRepository):
    database_manager: DatabaseManager

    def __post_init__(self):
        Model.set_connection_resolver(self.database_manager)

    def reserve_new_meeting_room(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservation.to_orator_model(reservation)

        orator_reservation.save()

    def cancel_meeting_room(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservation.to_orator_model(reservation)

        OratorReservation.update(orator_reservation, reservation_status=reservation.reservation_status.value)

    def find_all(self) -> List[Reservation]:
        return [OratorReservation.to_reservation(r) for r in OratorReservation.all()]

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        orator_reservation = OratorReservation.find(reservation_id.value)

        if orator_reservation is None:
            return None

        return OratorReservation.to_reservation(orator_reservation)

    def change_meeting_room(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservation.to_orator_model(reservation)

        OratorReservation.update(orator_reservation, meeting_room_id=reservation.meeting_room_id.value)

    def change_time_range(self, reservation: Reservation) -> None:
        orator_reservation = OratorReservation.to_orator_model(reservation)

        OratorReservation.update(orator_reservation, time_range_to_reserve=reservation.time_range_to_reserve)
