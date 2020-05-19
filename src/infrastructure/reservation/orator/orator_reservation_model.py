from __future__ import annotations

import datetime

from orator import Model

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時


class OratorReservationModel(Model):
    __table__ = 'reservations'

    def __repr__(self) -> str:
        # ださいけど、情報がわかりやすくなるので実装している
        tmp = ', '.join([f'{k}={v}' for k, v in self.to_dict().items()])
        repr_like_dataclass = f'{self.__class__.__name__}({tmp})'

        return repr_like_dataclass

    @classmethod
    def to_reservation(cls, source: OratorReservationModel) -> Reservation:
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
    def to_orator_model(cls, reservation: Reservation) -> OratorReservationModel:
        orator_reservation = OratorReservationModel()
        orator_reservation.id = reservation.id.value
        orator_reservation.meeting_room_id = reservation.meeting_room_id.value
        orator_reservation.reserver_id = reservation.reserver_id.value

        orator_reservation.reservation_status = reservation.reservation_status.value

        orator_reservation.number_of_participants = reservation.number_of_participants.value

        orator_reservation.start_datetime = OratorReservationModel.to_datetime(
            reservation.time_range_to_reserve.start_datetime)
        orator_reservation.end_datetime = OratorReservationModel.to_datetime(
            reservation.time_range_to_reserve.end_datetime)

        return orator_reservation
