from __future__ import annotations

import dataclasses
from dataclasses import dataclass

from src.domain.employee.社員ID import 社員ID
from src.domain.meeting_room.会議室ID import 会議室ID
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用人数 import 使用人数


@dataclass(frozen=True)
class Reservation:
    id: ReservationId
    time_range_to_reserve: TimeRangeToReserve
    使用人数: 使用人数
    meeting_room_id: 会議室ID
    reserver_id: 社員ID
    reservation_status: [ReservationStatus] = ReservationStatus.Reserved

    def is_かぶり(self, other: Reservation) -> bool:
        if self.meeting_room_id != other.meeting_room_id:
            return False

        return self.time_range_to_reserve.is_overlap(other.time_range_to_reserve)

    def cancel(self) -> Reservation:
        if self.reservation_status == ReservationStatus.Canceled:
            raise ValueError('既にキャンセル済みですよ')

        return dataclasses.replace(self, reservation_status=ReservationStatus.Canceled)
