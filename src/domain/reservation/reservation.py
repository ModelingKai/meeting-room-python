from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from src.domain.employee.社員ID import 社員ID
from src.domain.meeting_room.会議室ID import 会議室ID
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.予約時間帯 import 予約時間帯
from src.domain.reservation.使用人数 import 使用人数


@dataclass
class Reservation:
    id: ReservationId = field(init=False)
    予約時間帯: 予約時間帯
    使用人数: 使用人数
    meeting_room_id: 会議室ID
    reserver_id: 社員ID
    reservation_status: [ReservationStatus] = ReservationStatus.Reserved

    def __post_init__(self):
        self.id = ReservationId(str(uuid4()))

    def is_かぶり(self, other: Reservation) -> bool:
        if self.meeting_room_id != other.meeting_room_id:
            return False

        return self.予約時間帯.is_overlap(other.予約時間帯)
