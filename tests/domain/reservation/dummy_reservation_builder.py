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
    """テスト用のReservation生成を楽にするためのクラス

    テスト以外では使ってはいけない理由
        1. 不正なReservationをつくれてしまうから
            - 存在しない会議室IDや存在しない予約者IDを持つReservationの生成ができてしまう
        2. Reservation間の整合性(予約時間帯が重なっていないなど)は担保できないから
            - やろうと思えば、リポジトリやドメインサービスを適用するってことはできるが、それはやりすぎでは？

    ポイント
        1. デフォルトの予約時間帯は、「実行日の翌日の13時〜14時」である
            - `time_range_to_reserve` の指定記述が非常にだるいのでこれで十分という判断
            - 「翌日」にしているのは、不正な予約時間帯になるのを防ぐため
            - 特定の予約時間帯で作りたい場合は、 `self.with_time_range_to_reserve()` を使いましょう

    できないこと
        1. 過去の日時を持つデータはつくれない
            - 結局、使用日時クラスの now で判断しているため生成不可能。freezegunなどで日時を固定すること
        2. reservation_id と number_of_participants の指定はできない(2020年6月1日時点)
            - 現状、これらを特定の値にしたいモチベーションがないため

    その他
        1. 同一のインスタンスから生成されるReservationのId重複だけは防いでいる
    """
    execute_date: datetime.date = dataclasses.field(default=None)
    used_reservation_ids: Set[ReservationId] = dataclasses.field(default_factory=set)
    __dummy_reservation: Reservation = dataclasses.field(init=False)

    def __post_init__(self):
        # Pythonのデフォルト引数の罠を踏まないための実装
        if self.execute_date is None:
            self.execute_date = datetime.datetime.today()

        self.__dummy_reservation = Reservation(self._default_reservation_id(),
                                               self._default_time_to_range(),
                                               NumberOfParticipants(4),
                                               MeetingRoomId('A'),
                                               EmployeeId('001'))

    def _default_reservation_id(self) -> ReservationId:
        # これを採用したメリット: Reservationインスタンスのassertionが楽にできる
        # これを採用したリスク: インスタンスを複数つくれば、ReservationIdかぶりをつくれる

        return ReservationId('dummy_reservation_id')

    def _default_time_to_range(self) -> TimeRangeToReserve:
        """実行日の翌日13時〜14時 がデフォルトの予約時間帯"""
        the_next_day = self.execute_date + datetime.timedelta(days=1)
        yyyy, mm, dd, *_ = the_next_day.timetuple()

        return TimeRangeToReserve(使用日時(yyyy, mm, dd, 13, 00),
                                  使用日時(yyyy, mm, dd, 14, 00))

    def with_meeting_room_id(self, meeting_room_id: MeetingRoomId) -> DummyReservationBuilder:
        # テストデータ作成のための強引なミューテーション
        self.__dummy_reservation = dataclasses.replace(self.__dummy_reservation, meeting_room_id=meeting_room_id)

        return self

    def with_cancel(self) -> DummyReservationBuilder:
        self.__dummy_reservation = self.__dummy_reservation.cancel()

        return self

    def with_reserver_id(self, reserver_id: EmployeeId) -> DummyReservationBuilder:
        # テストデータ作成のための強引なミューテーションだから妥協して使用している
        self.__dummy_reservation = dataclasses.replace(self.__dummy_reservation, reserver_id=reserver_id)

        return self

    def with_time_range_to_reserve(self, time_range_to_reserve: TimeRangeToReserve) -> DummyReservationBuilder:
        # テストデータ作成のための強引なミューテーションだから妥協して使用している
        self.__dummy_reservation = dataclasses.replace(self.__dummy_reservation,
                                                       time_range_to_reserve=time_range_to_reserve)

        return self

    def with_random_id(self) -> DummyReservationBuilder:
        # テストデータ作成のための強引なミューテーションだから妥協して使用している
        # ReservationId の生成ルールがガードできていないので注意！
        self.__dummy_reservation = dataclasses.replace(self.__dummy_reservation, id=ReservationId(str(uuid.uuid4())))

        return self

    def build(self) -> Reservation:
        if self._has_already_build_reservation_id():
            self.with_random_id()

        self.used_reservation_ids.add(self.__dummy_reservation.id)

        return self.__dummy_reservation

    def _has_already_build_reservation_id(self) -> bool:
        return self.__dummy_reservation.id in self.used_reservation_ids
