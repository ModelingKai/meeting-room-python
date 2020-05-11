import uuid

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.presentation.cli.cli_util.user_raw_input import UserRawInput


class SomeOne:
    def to_reservation(self, u: UserRawInput) -> Reservation:
        year = int(u.date[:4])
        month = int(u.date[4:6])
        day = int(u.date[6:8])

        start_hour = int(u.start_time[:2])
        start_minute = int(u.start_time[2:4])

        end_hour = int(u.end_time[:2])
        end_minute = int(u.end_time[2:4])

        start_使用日時 = 使用日時(year, month, day, start_hour, start_minute)
        end_使用日時 = 使用日時(year, month, day, end_hour, end_minute)

        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(start_使用日時, end_使用日時),
                                  NumberOfParticipants(int(u.number_of_participants)),
                                  MeetingRoomId(u.meeting_room_id),
                                  EmployeeId(u.reserver_id))

        return reservation
