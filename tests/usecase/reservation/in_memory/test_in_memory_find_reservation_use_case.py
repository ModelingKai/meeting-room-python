import dataclasses
from dataclasses import dataclass

import pytest

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reservation.errors import NotFoundReservationError
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder


@dataclass
class FindReservationsUsecase:
    repository: InMemoryReservationRepository

    def find_reservation(self, reservation_id: ReservationId) -> Reservation:
        reservation = self.repository.find_by_id(reservation_id)

        if reservation is None:
            raise NotFoundReservationError('そんな予約ないよ')

        return reservation


class TestInMemoryFindReservationsUsecase:
    def setup(self):
        self.repository = InMemoryReservationRepository()
        self.usecase = FindReservationsUsecase(self.repository)

    @pytest.fixture
    def reservation(self) -> Reservation:
        return DummyReservationBuilder().build()

    def test_指定IDのReservationが1件だけ取得できる(self, reservation: Reservation):
        self.repository.data[reservation.id] = reservation
        self.repository.data[ReservationId('B')] = dataclasses.replace(reservation, meeting_room_id=MeetingRoomId('B'))
        self.repository.data[ReservationId('C')] = dataclasses.replace(reservation, meeting_room_id=MeetingRoomId('C'))

        assert self.usecase.find_reservation(reservation.id) == reservation

    def test_存在しないIDを指定された場合は例外だよ(self):
        with pytest.raises(NotFoundReservationError):
            self.usecase.find_reservation(ReservationId('Not Exist ID'))
