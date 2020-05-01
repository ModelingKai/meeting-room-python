import dataclasses
import uuid

import freezegun
import pytest

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reservation.errors import NotFoundReservationError, その会議室はその時間帯では予約ができませんよエラー
from src.usecase.resevation.change_time_range_usecase import ChangeTimeRangeUsecase


class TestChangeTimeRangeUsecase:
    def setup(self):
        self.repository = InMemoryReservationRepository()
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ChangeTimeRangeUsecase(self.repository, domain_service)

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_既存の予約を別の時間帯に変更ができること(self):
        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                  NumberOfParticipants(4),
                                  MeetingRoomId(str(uuid.uuid4())),
                                  EmployeeId(str(uuid.uuid4())))

        new_time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 2, 15, 00), 使用日時(2020, 4, 2, 17, 00))
        expected = dataclasses.replace(reservation, time_range_to_reserve=new_time_range_to_reserve)

        self.repository.data[reservation.id] = reservation
        self.usecase.change_time_range(reservation.id, new_time_range_to_reserve)

        assert expected == self.repository.data[reservation.id]

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_存在しない予約に対する予約時間帯の変更依頼はダメだよ(self):
        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                  NumberOfParticipants(4),
                                  MeetingRoomId(str(uuid.uuid4())),
                                  EmployeeId(str(uuid.uuid4())))

        new_time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 2, 15, 00), 使用日時(2020, 4, 2, 17, 00))

        with pytest.raises(NotFoundReservationError):
            self.usecase.change_time_range(reservation.id, new_time_range_to_reserve)

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_予約時間帯変更後の予約が既存の予約とぶつかっていたらダメだよ(self):
        reservation1 = Reservation(ReservationId(str(uuid.uuid4())),
                                   TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                   NumberOfParticipants(4),
                                   MeetingRoomId(str(uuid.uuid4())),
                                   EmployeeId(str(uuid.uuid4())))

        reservation2 = dataclasses.replace(reservation1,
                                           id=ReservationId(str(uuid.uuid4())),
                                           time_range_to_reserve=TimeRangeToReserve(使用日時(2020, 4, 2, 15, 00),
                                                                                    使用日時(2020, 4, 2, 17, 00)))

        self.repository.data[reservation1.id] = reservation1
        self.repository.data[reservation2.id] = reservation2

        with pytest.raises(その会議室はその時間帯では予約ができませんよエラー):
            self.usecase.change_time_range(reservation2.id, reservation1.time_range_to_reserve)

    @freezegun.freeze_time('2020-4-10 10:00')
    def test_予約時点では未来過ぎたが変更時点ではちゃんとした予約時間帯になっているから大丈夫(self):
        @freezegun.freeze_time('2020-4-01 10:00')
        def reservation_20200402_1300_1400() -> Reservation:
            """テストのために、 '2020-4-10 10:00' 時点では本来不正である過去の予約時間帯を持つデータを作る関数"""
            return Reservation(ReservationId(str(uuid.uuid4())),
                               TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                               NumberOfParticipants(4),
                               MeetingRoomId(str(uuid.uuid4())),
                               EmployeeId(str(uuid.uuid4())))

        exist_reservation = reservation_20200402_1300_1400()
        self.repository.data[exist_reservation.id] = exist_reservation

        new_time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 24, 13, 00), 使用日時(2020, 4, 24, 14, 00))
        expected = dataclasses.replace(exist_reservation, time_range_to_reserve=new_time_range_to_reserve)

        self.usecase.change_time_range(exist_reservation.id, new_time_range_to_reserve)

        assert expected == self.repository.data[exist_reservation.id]
