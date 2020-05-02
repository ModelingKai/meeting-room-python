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
from src.usecase.reservation.errors import NotFoundReservationError


class OratorReservation(Model):
    __table__ = 'reservations'

    def __repr__(self) -> str:
        # ださいけど、情報がわかりやすくなるので実装している
        tmp = ', '.join([f'{k}={v}' for k, v in self.to_dict().items()])
        repr_like_dataclass = f'{self.__class__.__name__}({tmp})'

        return repr_like_dataclass

    @classmethod
    def to_reserve_model(cls, from_: OratorReservation) -> Reservation:
        id = ReservationId(from_.id)
        meeting_room_id = MeetingRoomId(from_.meeting_room_id)
        reserver_id = EmployeeId(from_.reserver_id)

        number_of_participants = NumberOfParticipants(from_.number_of_participants)

        start_yyyy_mm_dd_HH_MM = datetime.datetime.strptime(from_.start_datetime, '%Y-%m-%d %H:%M:%S').timetuple()[:5]
        start_datetime = 使用日時(*start_yyyy_mm_dd_HH_MM)

        end_yyyy_mm_dd_HH_MM = datetime.datetime.strptime(from_.end_datetime, '%Y-%m-%d %H:%M:%S').timetuple()[:5]
        end_datetime = 使用日時(*end_yyyy_mm_dd_HH_MM)

        reservation_status = ReservationStatus.from_str(from_.reservation_status)

        return Reservation(id,
                           TimeRangeToReserve(start_datetime, end_datetime),
                           number_of_participants,
                           meeting_room_id,
                           reserver_id,
                           reservation_status)

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

        orator_reservation.update

    def find_all(self) -> List[Reservation]:
        return [OratorReservation.to_reserve_model(r) for r in OratorReservation.all()]

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        orator_reservation = OratorReservation.find(reservation_id.value)

        if orator_reservation is None:
            raise NotFoundReservationError('そんな予約ないよ')

        return OratorReservation.to_reserve_model(orator_reservation)

    def change_meeting_room(self, reservation: Reservation) -> None:
        pass
