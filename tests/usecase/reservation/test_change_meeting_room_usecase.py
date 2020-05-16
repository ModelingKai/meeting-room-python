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
from src.usecase.reservation.change_meeting_room_usecase import ChangeMeetingRoomUseCase
from src.usecase.reservation.errors import NotFoundReservationError
from src.usecase.reservation.errors import その会議室はその時間帯では予約ができませんよエラー


@freezegun.freeze_time('2020-4-1 10:00')
class TestChangeMeetingRoomUsecase:
    def setup(self):
        self.repository = InMemoryReservationRepository()
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ChangeMeetingRoomUseCase(self.repository, domain_service)

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation(self) -> Reservation:
        """不正でないReservationインスタンスを作成するだけのfixture"""
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    def test_既存の予約を別の会議室に変更ができること(self, reservation):
        expected = dataclasses.replace(reservation, meeting_room_id=MeetingRoomId('B'))

        self.repository.data[reservation.id] = reservation
        self.usecase.change_meeting_room(reservation.id, expected.meeting_room_id)

        assert expected == self.repository.data[reservation.id]

    def test_存在しない予約に対する会議室変更依頼はダメだよ(self, reservation):
        with pytest.raises(NotFoundReservationError):
            self.usecase.change_meeting_room(reservation.id, MeetingRoomId('A'))

    def test_会議室変更後の予約が既存の予約とぶつかっていたらダメだよ(self, reservation):
        reservation2 = dataclasses.replace(reservation,
                                           id=ReservationId(str(uuid.uuid4())),
                                           meeting_room_id=MeetingRoomId('A'))

        self.repository.data[reservation.id] = reservation
        self.repository.data[reservation2.id] = reservation2

        with pytest.raises(その会議室はその時間帯では予約ができませんよエラー):
            self.usecase.change_meeting_room(reservation2.id, reservation.meeting_room_id)
