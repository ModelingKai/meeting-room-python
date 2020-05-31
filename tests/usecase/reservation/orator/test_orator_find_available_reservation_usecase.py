import freezegun
import pytest
from orator import DatabaseManager, Model

from src.domain.reservation.reservation import Reservation
from src.infrastructure.reservation.orator.orator_reservation_model import OratorReservationModel
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.find_avalible_reservation_usecase import FindAvailableReservationsUsecase
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder
from tests.usecase.reservation.orator.migrate_in_memory import TEST_DB_CONFIG, migrate_in_memory


class TestOratorFindAvailableReservationsUsecase:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)

        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

    @pytest.fixture
    @freezegun.freeze_time('2020-3-1 10:00')
    def past_reservation(self) -> Reservation:
        return DummyReservationBuilder().with_random_id().build()

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_find_available_reservations(self, past_reservation: Reservation):
        repository = OratorReservationRepository()
        usecase = FindAvailableReservationsUsecase(repository)

        builder = DummyReservationBuilder()
        available_reservation = builder.build()
        cancelled_reservation = builder.with_cancel().build()

        OratorReservationModel.to_orator_model(past_reservation).save()
        OratorReservationModel.to_orator_model(available_reservation).save()
        OratorReservationModel.to_orator_model(cancelled_reservation).save()

        assert usecase.find_available_reservations() == [available_reservation]
