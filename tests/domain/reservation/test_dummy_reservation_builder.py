import freezegun

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
    @freezegun.freeze_time('2020-4-1 10:00')
    def test_単一の正常なReservationを生成できる_予約時間帯は翌日13時から14時がデフォルトとなる(self):
        expected = Reservation(ReservationId('1'),
                               TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                               NumberOfParticipants(4),
                               MeetingRoomId('A'),
                               EmployeeId('001'))

        assert DummyReservationBuilder().build() == expected

    def test_同一インスタンスから生成されたReservationのIDは1から順にインクリメントされる(self):
        # 言い換えると、生成のたびにReservationIdは変化する
        builder = DummyReservationBuilder()

        id1 = builder.build().id
        id2 = builder.build().id
        id3 = builder.build().id

        assert [id1, id2, id3] == [ReservationId('1'), ReservationId('2'), ReservationId('3')]

    def test_ランダムなIdを割り振ることができる(self):
        # 1つのテストで複数のBuilderインスタンスを利用するときのId衝突を防ぐときに役立つ機能
        builder = DummyReservationBuilder()

        random_id = builder.with_random_id().build().id

        assert random_id != ReservationId('1')

    def test_別のインスタンスであれば同一IDを持つReservationがつくれてしまう(self):
        reservation_id_1 = DummyReservationBuilder().build().id
        reservation_id_2 = DummyReservationBuilder().build().id

        assert reservation_id_1 == reservation_id_2

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_複雑なReservationもメソッドチェーンでつくりやすいよ(self):
        another_time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 15, 13, 00), 使用日時(2020, 4, 15, 14, 00))
        another_meeting_room_id = MeetingRoomId('Z')
        another_employee_id_999 = EmployeeId('999')

        expected = Reservation(ReservationId('1'),
                               another_time_range_to_reserve,
                               NumberOfParticipants(4),
                               another_meeting_room_id,
                               another_employee_id_999,
                               ReservationStatus.Canceled)

        actual = DummyReservationBuilder() \
            .with_time_range_to_reserve(another_time_range_to_reserve) \
            .with_meeting_room_id(another_meeting_room_id) \
            .with_reserver_id(another_employee_id_999) \
            .with_cancel() \
            .build()

        assert actual == expected
