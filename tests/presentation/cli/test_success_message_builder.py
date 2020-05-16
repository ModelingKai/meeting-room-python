import uuid

import freezegun
import pytest

from src.domain.employee.employee import Employee
from src.domain.employee.employee_domain_service import EmployeeDomainService
from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_domain_service import MeetingRoomDomainService
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.employee.in_memory_employee_repository import InMemoryEmployeeRepository
from src.infrastructure.meeting_room.in_memory_meeting_room_repository import InMemoryMeetingRoomRepository
from src.presentation.cli.cli_util.cli_new_reservation_success_message_builder import \
    CliNewReservationSuccessMessageBuilder
from src.usecase.employee.find_employee_usecase import FindEmployeeUseCase
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase


class TestCliNewReservationSuccessMessageBuilder:
    @pytest.fixture
    @freezegun.freeze_time('2020-4-1 10:00')
    def reservation(self) -> Reservation:
        """不正でないReservationインスタンスを作成するだけのfixture"""
        return Reservation(ReservationId(str(uuid.uuid4())),
                           TimeRangeToReserve(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           NumberOfParticipants(4),
                           MeetingRoomId('A'),
                           EmployeeId('001'))

    def test_1(self, reservation: Reservation):
        # MeetingRoom に関する準備
        meeting_room_repository = InMemoryMeetingRoomRepository()
        meeting_room_domain_service = MeetingRoomDomainService(meeting_room_repository)
        find_meeting_room_usecase = FindMeetingRoomUseCase(meeting_room_repository, meeting_room_domain_service)
        meeting_room_id = MeetingRoomId('A')
        meeting_room = MeetingRoom(meeting_room_id, '大会議室')

        meeting_room_repository.data[meeting_room_id] = meeting_room

        # Employee に関する準備
        employee_repository = InMemoryEmployeeRepository()
        employee_domain_service = EmployeeDomainService(employee_repository)
        find_employee_usecase = FindEmployeeUseCase(employee_repository, employee_domain_service)

        employee_id = EmployeeId('001')
        employee = Employee(employee_id, 'Bob')
        employee_repository.data[employee_id] = employee

        # こっから本編
        success_message_builder = CliNewReservationSuccessMessageBuilder(find_meeting_room_usecase,
                                                                         find_employee_usecase)

        success_message = success_message_builder.build(reservation)

        expected = 'Bobさん名義で、2020年04月02日 13:00-14:00 大会議室 を 4名で 予約しましたよ'
        assert expected == str(success_message)
