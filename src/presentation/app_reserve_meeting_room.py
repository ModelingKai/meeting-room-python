import datetime
import uuid
from collections import Callable
from dataclasses import dataclass

from orator import Schema, DatabaseManager
from orator.schema import Blueprint

from src.domain.employee.employee_id import EmployeeId
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.time_range_to_reserve import TimeRangeToReserve
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.errors import その会議室はその時間帯では予約ができませんよエラー
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase

DEV_DB_CONFIG = {
    'dev': {
        'driver': 'sqlite',
        'database': 'dev_db.sqlite3',
    }
}


def init_dev_db():
    schema = Schema(DatabaseManager(DEV_DB_CONFIG))

    table_name = 'reservations'
    schema.drop_if_exists(table_name)

    with schema.create(table_name) as table:
        table: Blueprint

        table.string('id').unique()
        table.string('meeting_room_id')
        table.string('reserver_id')
        table.enum('reservation_status', ['予約中', 'キャンセル済み'])
        table.integer('number_of_participants')
        table.datetime('start_datetime')
        table.datetime('end_datetime')

        table.datetime('created_at')
        table.datetime('updated_at')


@dataclass
class UserRawInput:
    date: str
    start_time: str
    end_time: str
    meeting_room_id: str
    reserver_id: str
    number_of_participants: str


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


@dataclass
class Dareka:
    reservation: Reservation
    find_employee_usecase: Callable
    find_mtg_room_usecase: Callable

    def to_response_object(self, reservation: Reservation) -> ResponseObject:
        time_to_range = reservation.time_range_to_reserve
        start_datetime = time_to_range.start_datetime
        end_datetime = time_to_range.end_datetime

        year, month, day = start_datetime.year, start_datetime.month, start_datetime.day
        start_time, end_time = start_datetime.time(), end_datetime.time()

        reserver_name = self.find_employee_usecase(reservation.reserver_id).name
        meeting_room_name = self.find_mtg_room_usecase(reservation.meeting_room_id).name

        number_of_participants = reservation.number_of_participants.value

        return ResponseObject(year,
                              month,
                              day,
                              start_time,
                              end_time,
                              meeting_room_name,
                              reserver_name,
                              number_of_participants)


def main():
    # DB用意
    init_dev_db()

    # usecaseの準備
    database_manager = DatabaseManager(DEV_DB_CONFIG)

    reservation_repository = OratorReservationRepository(database_manager)
    domain_service = ReservationDomainService(reservation_repository)
    usecase = ReserveMeetingRoomUsecase(reservation_repository, domain_service)

    # 0. ユーザからの入力を受け取する
    input_date = '20200505'
    input_start_time = '1100'
    input_end_time = '1200'
    input_meeting_room_id = 'A'
    input_reserver_id = 'Bob'
    input_number_of_participants = '4'

    # 1. バックエンドに行く前のバリデーション
    # ここは一旦考えない

    # 2. ユースケースクラスに渡せるような形に変換する
    user_raw_input = UserRawInput(input_date,
                                  input_start_time,
                                  input_end_time,
                                  input_meeting_room_id,
                                  input_reserver_id,
                                  input_number_of_participants)

    # ユーザからの文字列入力を、 Reservation に変換をする
    # to_reservation の責務は正しいドメインオブジェクトに変換をする
    reservation: Reservation = SomeOne().to_reservation(user_raw_input)

    # 3. ユースケースに依頼する ← ユースケース層の世界で、あとはユースケースに任せる
    try:
        usecase.reserve_meeting_room(reservation)
    except その会議室はその時間帯では予約ができませんよエラー as e:
        # エラーページみたいなもの
        print(e)
        exit()
    except Exception as e:
        # 500番 エラー
        print('なんか落ちた。ごめんね。')
        exit()

    @dataclass
    class Employee:
        id: EmployeeId
        name: str

    @dataclass
    class MeetingRoom:
        id: MeetingRoomId
        name: str

    MockFindEmployeeUseCase_find_by_id = lambda x: Employee(EmployeeId('1'), name='Bob')
    MockFindMeetingRoomUseCase_find_by_id = lambda x: MeetingRoom(MeetingRoomId('1'), name='会議室A')

    dareka = Dareka(reservation,
                    MockFindEmployeeUseCase_find_by_id,
                    MockFindMeetingRoomUseCase_find_by_id)

    response_object = dareka.to_response_object(reservation)

    # 4. ユースケースでの処理結果に応じて、なんかする。
    # ResponseObjectは __str__()を持っているようにする
    print(response_object)


if __name__ == '__main__':
    main()
