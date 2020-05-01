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
from src.usecase.reservation.errors import NotFoundReservationError
from src.usecase.resevation.change_time_range_usecase import ChangeTimeRangeUsecase


@freezegun.freeze_time('2020-4-1 10:00')
class TestChangeTimeRangeUsecase:
    def setup(self):
        self.repository = InMemoryReservationRepository()
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ChangeTimeRangeUsecase(self.repository, domain_service)

    def test_既存の予約を別の時間帯に変更ができること(self):
        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                  NumberOfParticipants(4),
                                  MeetingRoomId(str(uuid.uuid4())),
                                  EmployeeId(str(uuid.uuid4())))

        new_time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 2, 15, 00), 使用日時(2020, 4, 2, 17, 00))
        expected = dataclasses.replace(reservation, time_range_to_reserve=new_time_range_to_reserve)

        self.repository.data[reservation.id] = reservation
        self.usecase.change_time_range(reservation.id, new_time_range_to_reserve)

        assert expected == self.repository.data[reservation.id]

    def test_存在しない予約に対する予約時間帯の変更依頼はダメだよ(self):
        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                  NumberOfParticipants(4),
                                  MeetingRoomId(str(uuid.uuid4())),
                                  EmployeeId(str(uuid.uuid4())))

        new_time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 2, 15, 00), 使用日時(2020, 4, 2, 17, 00))

        with pytest.raises(NotFoundReservationError):
            self.usecase.change_time_range(reservation.id, new_time_range_to_reserve)
