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
from src.usecase.reservation.errors import NotFoundReservationError, その会議室はその時間帯では予約ができませんよエラー


@freezegun.freeze_time('2020-4-1 10:00')
class TestChangeMeetingRoomUsecase:
    def setup(self):
        self.repository = InMemoryReservationRepository()
        domain_service = ReservationDomainService(self.repository)
        self.usecase = ChangeMeetingRoomUseCase(self.repository, domain_service)

    def test_既存の予約を別の会議室に変更ができること(self):
        reservation_id = ReservationId(str(uuid.uuid4()))
        time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00))
        reservation_人数 = NumberOfParticipants(4)
        meeting_room_id = MeetingRoomId(str(uuid.uuid4()))
        reserver_id = EmployeeId(str(uuid.uuid4()))

        reservation = Reservation(reservation_id,
                                  time_range_to_reserve,
                                  reservation_人数,
                                  meeting_room_id,
                                  reserver_id)

        new_meeting_room_id = MeetingRoomId(str(uuid.uuid4()))
        expected = Reservation(reservation_id,
                               time_range_to_reserve,
                               reservation_人数,
                               new_meeting_room_id,
                               reserver_id)

        self.repository.data[reservation.id] = reservation
        self.usecase.change_meeting_room(reservation.id, new_meeting_room_id)

        assert expected == self.repository.data[reservation.id]

    def test_存在しない予約に対する会議室変更依頼はダメだよ(self):
        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                                  NumberOfParticipants(4),
                                  MeetingRoomId(str(uuid.uuid4())),
                                  EmployeeId(str(uuid.uuid4())))

        with pytest.raises(NotFoundReservationError):
            self.usecase.change_meeting_room(reservation.id, MeetingRoomId(str(uuid.uuid4())))

    def test_会議室変更後の予約が既存の予約とぶつかっていたらダメだよ(self):
        reservation1_meeting_id = MeetingRoomId(str(uuid.uuid4()))
        reservation2_meeting_id = MeetingRoomId(str(uuid.uuid4()))

        time_range_to_reserve = TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00))

        reservation1 = Reservation(ReservationId(str(uuid.uuid4())),
                                   time_range_to_reserve,
                                   NumberOfParticipants(4),
                                   reservation1_meeting_id,
                                   EmployeeId(str(uuid.uuid4())))

        reservation2 = Reservation(ReservationId(str(uuid.uuid4())),
                                   time_range_to_reserve,
                                   NumberOfParticipants(4),
                                   reservation2_meeting_id,
                                   EmployeeId(str(uuid.uuid4())))

        self.repository.data[reservation1.id] = reservation1
        self.repository.data[reservation2.id] = reservation2

        with pytest.raises(その会議室はその時間帯では予約ができませんよエラー):
            self.usecase.change_meeting_room(reservation2.id, reservation1_meeting_id)
