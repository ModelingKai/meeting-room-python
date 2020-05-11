import dataclasses
import datetime
import uuid

import freezegun

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from tests.usecase.reservation.available_reservations import AvailableReservations


class TestInMemoryFindAvailableReservations:
    @freezegun.freeze_time('2020-04-01 10:00')
    def create_base_reservation(self):
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 1, 13, 00), 使用日時(2020, 4, 1, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId(str(uuid.uuid4())),
                           EmployeeId(str(uuid.uuid4())))

    @freezegun.freeze_time('2020-04-01 10:00')
    def test_キャンセル済みはAvailableReservationではない(self):
        r_base = self.create_base_reservation()

        r1_有効 = dataclasses.replace(r_base,
                                    id=ReservationId('r1'),
                                    time_range_to_reserve=TimeRangeToReserve(使用日時(2020, 4, 1, 13, 00),
                                                                             使用日時(2020, 4, 1, 14, 00)),
                                    reservation_status=ReservationStatus.Reserved)

        r2_キャンセル済み = dataclasses.replace(r_base,
                                         id=ReservationId('r2'),
                                         time_range_to_reserve=TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00),
                                                                                  使用日時(2020, 4, 2, 14, 00)),
                                         reservation_status=ReservationStatus.Canceled)

        reservation_repository = InMemoryReservationRepository()
        reservation_repository.data[r1_有効.id] = r1_有効
        reservation_repository.data[r2_キャンセル済み.id] = r2_キャンセル済み

        available_reservations = AvailableReservations()
        available_reservations = available_reservations.add(r1_有効)

        now = datetime.datetime(2020, 4, 1, 10, 0)
        assert reservation_repository.find_available_reservations(now) == available_reservations
