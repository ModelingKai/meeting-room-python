import datetime
from dataclasses import dataclass


@dataclass
class ResponseObject:
    year: int  # 2019
    month: int  # 5
    day: int  # 6
    start_time: datetime.time  # datetime.time(10,00)
    end_time: datetime.time  # datetime.time(12,00)
    meeting_room_name: str  # 'A'
    reserver_name: str  # 'Bob'
    number_of_participants: int  # 4

    def __str__(self) -> str:
        return f'{self.reserver_name}さん名義で、{self.fmt_datetime()} {self.meeting_room_name} を {self.number_of_participants}名で 予約しましたよ'

    def fmt_datetime(self) -> str:
        yyyy = self.year
        mm = f'{self.month:02d}'
        dd = f'{self.day:02d}'
        start_hhii = self.start_time.strftime('%H:%M')
        end_hhii = self.end_time.strftime('%H:%M')

        return f'{yyyy}年{mm}月{dd}日 {start_hhii}-{end_hhii}'
