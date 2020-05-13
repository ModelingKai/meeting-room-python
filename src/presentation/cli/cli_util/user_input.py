import uuid
from dataclasses import dataclass

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時


@dataclass
class CliUserInput:
    date: str
    start_time: str
    end_time: str
    meeting_room_id: str
    reserver_id: str
    number_of_participants: str

    def to_reservation(self) -> Reservation:
        # MEMO: 「ユーザ入力が正常なときだけ、正しく変換できるよ」って情報を表現できると最高なんだが？
        year = int(self.date[:4])
        month = int(self.date[4:6])
        day = int(self.date[6:8])

        start_hour = int(self.start_time[:2])
        start_minute = int(self.start_time[2:4])

        end_hour = int(self.end_time[:2])
        end_minute = int(self.end_time[2:4])

        start_使用日時 = 使用日時(year, month, day, start_hour, start_minute)
        end_使用日時 = 使用日時(year, month, day, end_hour, end_minute)

        reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  TimeRangeToReserve(start_使用日時, end_使用日時),
                                  NumberOfParticipants(int(self.number_of_participants)),
                                  MeetingRoomId(self.meeting_room_id),
                                  EmployeeId(self.reserver_id))

        return reservation
