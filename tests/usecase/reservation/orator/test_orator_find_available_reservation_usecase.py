import dataclasses
import uuid

import freezegun
import pytest
from orator import DatabaseManager, Model

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.orator.orator_reservation_model import OratorReservationModel
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.find_avalible_reservation_usecase import FindAvailableReservationsUsecase
from tests.usecase.reservation.orator.migrate_in_memory import TEST_DB_CONFIG, migrate_in_memory


class TestOratorFindAvailableReservationsUsecase:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)

        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation_0402(self) -> Reservation:
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    @pytest.fixture
    @freezegun.freeze_time('2020-3-1 10:00')
    def reservation_0301(self) -> Reservation:
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 3, 2, 13, 00), 使用日時(2020, 3, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    @freezegun.freeze_time('2020-4-1 10:00')
    def test_find_available_reservations(self, reservation_0402: Reservation, reservation_0301: Reservation):
        repository = OratorReservationRepository()
        usecase = FindAvailableReservationsUsecase(repository)

        cancelled_reservation = dataclasses.replace(reservation_0402,
                                                    id=ReservationId(str(uuid.uuid4())),
                                                    reservation_status=ReservationStatus.Canceled)

        OratorReservationModel.to_orator_model(reservation_0301).save()
        OratorReservationModel.to_orator_model(reservation_0402).save()
        OratorReservationModel.to_orator_model(cancelled_reservation).save()

        assert usecase.find_available_reservations() == [reservation_0402]
