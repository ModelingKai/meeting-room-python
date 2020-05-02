from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass
from typing import Union, List

import freezegun
from orator import DatabaseManager, Model

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_repository import ReservationRepository
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.init_db import DB_CONFIG


class OratorReservation(Model):
    __table__ = 'reservations'

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
        pass

    def find_all(self) -> List[Reservation]:
        pass

    def find_by_id(self, reservation_id: ReservationId) -> Union[Reservation, None]:
        pass

    def change_meeting_room(self, reservation: Reservation) -> None:
        pass


@freezegun.freeze_time('2020-4-1 10:00')
def main():
    reservation = Reservation(ReservationId(str(uuid.uuid4())),
                              TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                              NumberOfParticipants(4),
                              MeetingRoomId(str(uuid.uuid4())),
                              EmployeeId(str(uuid.uuid4())))

    database_manager = DatabaseManager(DB_CONFIG)

    repository = OratorReservationRepository(database_manager)

    repository.reserve_new_meeting_room(reservation)


if __name__ == '__main__':
    main()
