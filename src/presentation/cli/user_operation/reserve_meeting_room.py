from orator import DatabaseManager

from src.app_environment.init_dev_db import DEV_DB_CONFIG
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.presentation.cli.cli_util.reservation_command_validator import CliReservationCommandValidator
from src.presentation.cli.cli_util.response_object_factory import ResponseObjectFactory
from src.presentation.cli.cli_util.some_one import SomeOne
from src.presentation.cli.cli_util.user_raw_input import UserRawInput
from src.usecase.employee.mock_find_employee_usecase import MockFindEmployeeUseCase
from src.usecase.meeting_room.mock_find_meeting_room_usecase import MockFindMeetingRoomUseCase
from src.usecase.reservation.errors import その会議室はその時間帯では予約ができませんよエラー
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase


def main():
    # usecaseの準備
    database_manager = DatabaseManager(DEV_DB_CONFIG)

    # TODO: ここのDIの仕方も、違うところでやるんだろう( Python Injectorとか？）
    reservation_repository = OratorReservationRepository(database_manager)
    domain_service = ReservationDomainService(reservation_repository)
    usecase = ReserveMeetingRoomUsecase(reservation_repository, domain_service)

    # TODO: input()でユーザからデータ入力する
    # 0. ユーザからの入力を受け取る
    input_date = ''  # '20200516'  # input('日付は？')
    input_start_time = '1100'  # input('開始時刻は？')
    input_end_time = ''  # input('終了時刻は？')
    input_meeting_room_id = 'A'  # input('会議室は？')
    input_reserver_id = 'Bob'  # input('あなたはだれ？')
    input_number_of_participants = '4'  # input('何人くらいで利用する？')

    # 1. バックエンドに行く前のバリデーション
    user_raw_input = UserRawInput(input_date,
                                  input_start_time,
                                  input_end_time,
                                  input_meeting_room_id,
                                  input_reserver_id,
                                  input_number_of_participants)

    validation_result = CliReservationCommandValidator.validate(user_raw_input)

    if validation_result.is_ダメ():
        validation_result.display_messages()
        exit()

    # 2. ユースケースクラスに渡せるような形に変換する

    # ユーザからの文字列入力を、 Reservation に変換をする
    # to_reservation の責務は正しいドメインオブジェクトに変換をする
    # TODO: SomeOneの名前の変更はしたい
    reservation: Reservation = SomeOne().to_reservation(user_raw_input)

    # 3. ユースケースに依頼する ← ユースケース層の世界で、あとはユースケースに任せる
    try:
        usecase.reserve_meeting_room(reservation)
    except その会議室はその時間帯では予約ができませんよエラー as e:
        # エラーページみたいなもの
        print(e)
        exit()
    except Exception as e:
        # Webでいう 500番 エラー
        # TODO: これも独自例外にするかも
        print('なんか落ちた。ごめんね。', e)
        exit()

    # MEMO: モックやぞ！
    # TODO: Mockのユースケースを本物に差し替える
    factory = ResponseObjectFactory(MockFindEmployeeUseCase(), MockFindMeetingRoomUseCase())
    response_object = factory.create(reservation)

    # 4. ユースケースでの処理結果に応じて、なんかする。
    # ResponseObjectは __str__()を持っているようにする
    print(response_object)


if __name__ == '__main__':
    main()
