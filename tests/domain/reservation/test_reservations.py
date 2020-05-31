import datetime

import pytest

from src.domain.reservation.available_reservations import AvailableReservations
from src.domain.reservation.errors import NotAvailableReservationError
from src.domain.reservation.reservation import Reservation
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder


class TestReservations:
    @pytest.fixture
    def canceled_reservation(self) -> Reservation:
        return DummyReservationBuilder(datetime.datetime.now()).with_cancel().build()

    def test_初期化時に有効ではない予約を含むリストを渡すとエラーとなる(self, canceled_reservation):
        with pytest.raises(NotAvailableReservationError):
            AvailableReservations([canceled_reservation])

    def test_有効ではない予約を追加時にエラーとなる(self, canceled_reservation):
        with pytest.raises(NotAvailableReservationError):
            AvailableReservations().add(canceled_reservation)
