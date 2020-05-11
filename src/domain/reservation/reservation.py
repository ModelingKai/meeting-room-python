from __future__ import annotations

import dataclasses
import datetime
from dataclasses import dataclass

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve


@dataclass(frozen=True)
class Reservation:
    id: ReservationId
    time_range_to_reserve: TimeRangeToReserve
    number_of_participants: NumberOfParticipants
    meeting_room_id: MeetingRoomId
    reserver_id: EmployeeId
    reservation_status: [ReservationStatus] = ReservationStatus.Reserved

    def is_かぶり(self, other: Reservation) -> bool:
        if self.meeting_room_id != other.meeting_room_id:
            return False

        return self.time_range_to_reserve.is_overlap(other.time_range_to_reserve)

    def cancel(self) -> Reservation:
        if self.reservation_status == ReservationStatus.Canceled:
            raise ValueError('既にキャンセル済みですよ')

        return dataclasses.replace(self, reservation_status=ReservationStatus.Canceled)

    def change_meeting_room(self, meeting_room_id: MeetingRoomId) -> Reservation:
        return dataclasses.replace(self, meeting_room_id=meeting_room_id)

    def change_time_range(self, time_range_to_reserve: TimeRangeToReserve) -> Reservation:
        return dataclasses.replace(self, time_range_to_reserve=time_range_to_reserve)

    def is_available(self, now: datetime.datetime):
        is_reserved = self.reservation_status == ReservationStatus.Reserved
        is_future = self.time_range_to_reserve.start_datetime > now
        return is_reserved and is_future
