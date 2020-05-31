import freezegun
import pytest

from src.domain.reservation.reservation import Reservation
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reservation.find_avalible_reservation_usecase import FindAvailableReservationsUsecase
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder


class TestInMemoryFindAvailableReservationsUsecase:
    @pytest.fixture
    @freezegun.freeze_time('2020-3-1 10:00')
    def past_reservation(self) -> Reservation:
        return DummyReservationBuilder().with_random_id().build()

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_find_available_reservations(self, past_reservation: Reservation):
        repository = InMemoryReservationRepository()
        usecase = FindAvailableReservationsUsecase(repository)

        builder = DummyReservationBuilder()
        available_reservation = builder.build()
        cancelled_reservation = builder.with_cancel().build()

        repository.data[available_reservation.id] = available_reservation
        repository.data[cancelled_reservation.id] = cancelled_reservation
        repository.data[past_reservation.id] = past_reservation

        assert usecase.find_available_reservations() == [available_reservation]
