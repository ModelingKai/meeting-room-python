from __future__ import annotations

import datetime
import uuid
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
from src.infrastructure.init_db import DB_CONFIG


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

        start_datetime_temp = datetime.datetime.strptime(from_.start_datetime, '%Y-%m-%d %H:%M:%S')
        end_datetime_temp = datetime.datetime.strptime(from_.end_datetime, '%Y-%m-%d %H:%M:%S')

        start_datetime = 使用日時(start_datetime_temp.year,
                              start_datetime_temp.month,
                              start_datetime_temp.day,
                              start_datetime_temp.hour,
                              start_datetime_temp.minute)
        end_datetime = 使用日時(end_datetime_temp.year,
                            end_datetime_temp.month,
                            end_datetime_temp.day,
                            end_datetime_temp.hour,
                            end_datetime_temp.minute)

        reservation_status = ReservationStatus.from_str(from_.reservation_status)

        return Reservation(id, TimeRangeToReserve(start_datetime, end_datetime),
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
        reservations = OratorReservation.all()

        results: List[Reservation] = []
        for reservation in reservations:
            r = OratorReservation.to_reserve_model(reservation)
            results.append(r)

        return results

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        pass

    def change_meeting_room(self, reservation: Reservation) -> None:
        pass


def main():
    reservation = Reservation(ReservationId(str(uuid.uuid4())),
                              TimeRangeToReserve(使用日時(2020, 5, 3, 13, 00), 使用日時(2020, 5, 3, 14, 00)),
                              NumberOfParticipants(4),
                              MeetingRoomId(str(uuid.uuid4())),
                              EmployeeId(str(uuid.uuid4())))

    database_manager = DatabaseManager(DB_CONFIG)

    repository = OratorReservationRepository(database_manager)

    repository.reserve_new_meeting_room(reservation)

    canceled_reservation = reservation.cancel()

    repository.cancel_meeting_room(canceled_reservation)


if __name__ == '__main__':
    main()
