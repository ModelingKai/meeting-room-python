import dataclasses
import datetime

import pytest

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_status import ReservationStatus
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reservation.cancel_meeting_room_usecase import CancelMeetingRoomUsecase
from src.usecase.reservation.errors import NotFoundReservationError
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder


class TestInMemoryCancelMeetingRoomUsecase:
    def setup(self):
        self.reservation_repository = InMemoryReservationRepository()
        self.usecase = CancelMeetingRoomUsecase(self.reservation_repository)

    @pytest.fixture
    def reservation(self) -> Reservation:
        return DummyReservationBuilder(datetime.datetime.now()).build()

    def test_予約をキャンセルができること(self, reservation: Reservation):
        expected = dataclasses.replace(reservation, reservation_status=ReservationStatus.Canceled)

        self.reservation_repository.data[reservation.id] = reservation

        self.usecase.cancel_meeting_room(reservation.id)

        assert expected == self.reservation_repository.data[reservation.id]

    def test_存在しない予約に対してキャンセルするのはダメだよ(self, reservation: Reservation):
        with pytest.raises(NotFoundReservationError):
            self.usecase.cancel_meeting_room(reservation.id)

    def test_キャンセル済みに対してキャンセルするのもダメだよ(self, reservation: Reservation):
        canceled_reservation = dataclasses.replace(reservation, reservation_status=ReservationStatus.Canceled)

        self.reservation_repository.data[canceled_reservation.id] = canceled_reservation

        with pytest.raises(ValueError):
            self.usecase.cancel_meeting_room(canceled_reservation.id)
