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
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reservation.errors import その会議室はその時間帯では予約ができませんよエラー
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase


class TestReserveMeetingRoomUsecase:
    def setup(self):
        self.reservation_repository = InMemoryReservationRepository()
        domain_service = ReservationDomainService(self.reservation_repository)
        self.usecase = ReserveMeetingRoomUsecase(self.reservation_repository, domain_service)

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_会議室を予約する_正常系(self):
        expected = Reservation(ReservationId(str(uuid.uuid4())),
                               TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                               NumberOfParticipants(4),
                               MeetingRoomId(str(uuid.uuid4())),
                               EmployeeId(str(uuid.uuid4())))

        self.usecase.reserve_meeting_room(expected)

        assert expected == self.reservation_repository.data[expected.id]

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_会議室を予約する_異常系_会議室と予約時間帯が完全に被っている(self):
        # テストケースとしては、完全一致しかないが、他のパターンは時間帯予約のテストケースでクリアしている
        # ので、特に不安はない
        # 予約エラーを細分化するのであれば、その分類ごとにテストを用意してもいいかもしれない。でも用意しない
        exist_reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                        TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                        NumberOfParticipants(3),
                                        MeetingRoomId(str(uuid.uuid4())),
                                        EmployeeId(str(uuid.uuid4())))

        new_reservation = dataclasses.replace(exist_reservation,
                                              id=ReservationId(str(uuid.uuid4())),
                                              number_of_participants=NumberOfParticipants(4))

        self.reservation_repository.data[exist_reservation.id] = exist_reservation

        with pytest.raises(その会議室はその時間帯では予約ができませんよエラー):
            self.usecase.reserve_meeting_room(new_reservation)

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_会議室を予約する_正常系_会議室と時間帯的には予約できないけどキャンセル済みだから予約できるんだなあ(self):
        exist_reservation_id = ReservationId(str(uuid.uuid4()))
        exist_reservation = Reservation(exist_reservation_id,
                                        TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                        NumberOfParticipants(3),
                                        MeetingRoomId(str(uuid.uuid4())),
                                        EmployeeId(str(uuid.uuid4())),
                                        ReservationStatus.Canceled)

        new_reservation = dataclasses.replace(exist_reservation,
                                              id=ReservationId(str(uuid.uuid4())),
                                              reservation_status=ReservationStatus.Reserved)

        self.reservation_repository.data[exist_reservation.id] = exist_reservation

        self.usecase.reserve_meeting_room(new_reservation)

        assert self.reservation_repository.data[new_reservation.id] == new_reservation
