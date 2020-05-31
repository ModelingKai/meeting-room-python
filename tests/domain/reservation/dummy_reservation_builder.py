from __future__ import annotations

import dataclasses
import datetime
import uuid
from dataclasses import dataclass
from typing import Set

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時


@dataclass
class DummyReservationBuilder:
    """
    発想: あくまで単体のReservationをつくるのを楽にするクラス

    生成するReservationIdの重複は防いでいる


    ReservationId以外の属性や、Reservation間の不正は検知はできない
        - 会議室や、予約時間帯の被っている不正なデータをつくれてしまう
        - 存在しない会議室IDや存在しない予約者IDもつくれる
        - やろうと思えば、生成したReservationをrepositoryに登録して、ドメインサービスを適用するってことはできるが、やりすぎでは？

    過去の日時を持つデータはつくれない
        - 結局、使用日時クラスのnow で判断しているため
        - with_time_range_to_reserve を使って差し込もうな
    """
    now: datetime.datetime
    used_reservation_ids: Set[Reservation] = dataclasses.field(default_factory=set)

    def __post_init__(self):
        time_range_to_reserve = self._make_tomorrow_time_to_range()

        self.dummy_reservation = Reservation(ReservationId('dummy_reservation_id'),
                                             time_range_to_reserve,
                                             NumberOfParticipants(4),
                                             MeetingRoomId('A'),
                                             EmployeeId('001'))

    def _make_tomorrow_time_to_range(self) -> TimeRangeToReserve:
        tomorrow = self.now + datetime.timedelta(days=1)

        yyyy, mm, dd, *_ = tomorrow.timetuple()

        return TimeRangeToReserve(使用日時(yyyy, mm, dd, 13, 00),
                                  使用日時(yyyy, mm, dd, 14, 00))

    def with_meeting_room_id(self, meeting_room_id: MeetingRoomId) -> DummyReservationBuilder:
        # テストデータ作成のための強引なミューテーション
        object.__setattr__(self.dummy_reservation, 'meeting_room_id', meeting_room_id)

        return self

    def with_cancel(self) -> DummyReservationBuilder:
        self.dummy_reservation = self.dummy_reservation.cancel()

        return self

    def with_reserver_id(self, reserver_id: EmployeeId) -> DummyReservationBuilder:
        # テストデータ作成のための強引なミューテーションだから妥協して使用している
        object.__setattr__(self.dummy_reservation, 'reserver_id', reserver_id)

        return self

    def with_time_range_to_reserve(self, time_range_to_reserve: TimeRangeToReserve) -> DummyReservationBuilder:
        # テストデータ作成のための強引なミューテーションだから妥協して使用している
        object.__setattr__(self.dummy_reservation, 'time_range_to_reserve', time_range_to_reserve)

        return self

    def with_random_id(self) -> DummyReservationBuilder:
        # テストデータ作成のための強引なミューテーションだから妥協して使用している
        # ReservationId の生成ルールがガードできていないので注意！
        self.dummy_reservation = dataclasses.replace(self.dummy_reservation, id=ReservationId(str(uuid.uuid4())))

        return self

    def build(self) -> Reservation:
        if self._has_already_build_reservation_id():
            self.with_random_id()

        self.used_reservation_ids.add(self.dummy_reservation.id)

        return self.dummy_reservation

    def _has_already_build_reservation_id(self) -> bool:
        return self.dummy_reservation.id in self.used_reservation_ids
