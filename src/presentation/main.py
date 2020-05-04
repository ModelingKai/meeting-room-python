from dataclasses import dataclass

from orator import Schema, DatabaseManager
from orator.schema import Blueprint

from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
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
class UserInput:
    input_date: str
    input_start_time: str
    input_end_time: str
    input_meeting_room_id: str
    input_reserver_id: str
    input_number_of_participant: str


class SomeOne:
    def to_reservation(self, user_input: UserInput) -> Reservation:
        pass


class ResponseObject:
    def __str__(self) -> str:
        return 'なんかいい感じのメッセージ'


class Darekaga:
    def nankasuru(self, reservation: Reservation) -> ResponseObject:
        pass


def main():
    # DB用意
    # init_dev_db()

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
    user_input = UserInput(input_date,
                           input_start_time,
                           input_end_time,
                           input_meeting_room_id,
                           input_reserver_id,
                           input_number_of_participants)

    # ユーザからの文字列入力を、 Reservation に変換をする
    # to_reservation の責務は正しいドメインオブジェクトに変換をする
    reservation: Reservation = SomeOne().to_reservation(user_input)

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

    # もし、社員名が欲しい場合には、社員名を取得するような
    # reserver_name = FindEmployeeUseCase().find_by_id(reservation.reserver_id)

    # 4. ユースケースでの処理結果に応じて、なんかする。
    response_object: ResponseObject = Darekaga().nankasuru(reservation)
    # ResponseObjectは __str__()を持っているようにする
    print(response_object)


if __name__ == '__main__':
    main()
