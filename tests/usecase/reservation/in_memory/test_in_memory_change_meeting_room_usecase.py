import dataclasses
import uuid

import pytest

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reservation.change_meeting_room_usecase import ChangeMeetingRoomUseCase
from src.usecase.reservation.errors import NotFoundReservationError
from src.usecase.reservation.errors import その会議室はその時間帯では予約ができませんよエラー
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder


class TestInMemoryChangeMeetingRoomUsecase:
    def setup(self):
        self.repository = InMemoryReservationRepository()
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ChangeMeetingRoomUseCase(self.repository, domain_service)

    @pytest.fixture
    def reservation(self) -> Reservation:
        return DummyReservationBuilder().build()

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
