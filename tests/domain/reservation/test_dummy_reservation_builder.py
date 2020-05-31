import dataclasses
import datetime

import freezegun
import pytest

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder


class TestDummyReservationBuilder:
    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def default_dummy_reservation(self) -> Reservation:
        return Reservation(ReservationId('dummy_reservation_id'),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    def test_単一の正常なReservationを生成できる(self, default_dummy_reservation: Reservation):
        builder = DummyReservationBuilder(datetime.datetime.now())

        assert builder.build() == default_dummy_reservation

    def test_同一インスタンスから生成されたReservationのIDは重複しない(self):
        # 言い換えると、生成のたびにReservationIdは変化する
        builder = DummyReservationBuilder(datetime.datetime.now())

        id1 = builder.build().id
        id2 = builder.build().id
        id3 = builder.build().id

        assert len({id1, id2, id3}) == 3

    def test_別のインスタンスであれば同一IDを持つReservationがつくれてしまう(self):
        reservation_id_1 = DummyReservationBuilder(datetime.datetime.now()).build().id
        reservation_id_2 = DummyReservationBuilder(datetime.datetime.now()).build().id

        assert reservation_id_1 == reservation_id_2

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_複雑なReservationもメソッドチェーンでつくりやすいよ(self, default_dummy_reservation: Reservation):
        another_time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 15, 13, 00), 使用日時(2020, 4, 15, 14, 00))
        another_meeting_room_id = MeetingRoomId('Z')
        another_employee_id_999 = EmployeeId('999')

        expected = Reservation(ReservationId('dummy_reservation_id'),
                               another_time_range_to_reserve,
                               NumberOfParticipants(4),
                               another_meeting_room_id,
                               another_employee_id_999,
                               ReservationStatus.Canceled)

        actual = DummyReservationBuilder(datetime.datetime.now()) \
            .with_time_range_to_reserve(another_time_range_to_reserve) \
            .with_meeting_room_id(another_meeting_room_id) \
            .with_reserver_id(another_employee_id_999) \
            .with_cancel() \
            .build()

        assert actual == expected

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_キャンセル済みのReservationがつくれる(self, default_dummy_reservation: Reservation):
        builder = DummyReservationBuilder(datetime.datetime.now())

        expected = dataclasses.replace(default_dummy_reservation, reservation_status=ReservationStatus.Canceled)

        assert builder.with_cancel().build() == expected

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_会議室IDを指定できる(self, default_dummy_reservation: Reservation):
        builder = DummyReservationBuilder(datetime.datetime.now())

        another_meeting_room_id = MeetingRoomId('Z')

        expected = dataclasses.replace(default_dummy_reservation, meeting_room_id=another_meeting_room_id)

        assert builder.with_meeting_room_id(another_meeting_room_id).build() == expected

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_予約者IDを指定できる(self, default_dummy_reservation: Reservation):
        builder = DummyReservationBuilder(datetime.datetime.now())

        another_reserver_id = EmployeeId('999')

        expected = dataclasses.replace(default_dummy_reservation, reserver_id=another_reserver_id)

        assert builder.with_reserver_id(another_reserver_id).build() == expected

    @freezegun.freeze_time('2020-12-31 10:00')
    def test_予約時間帯を指定できる(self, default_dummy_reservation: Reservation):
        builder = DummyReservationBuilder(datetime.datetime(2020, 12, 31, 10, 00))

        another_time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 12, 31, 13, 00),
                                                           使用日時(2020, 12, 31, 14, 00))

        expected = dataclasses.replace(default_dummy_reservation, time_range_to_reserve=another_time_range_to_reserve)

        assert builder.with_time_range_to_reserve(another_time_range_to_reserve).build() == expected
