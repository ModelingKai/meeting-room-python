import datetime

from orator import DatabaseManager

from src.app_environment.init_dev_db import DEV_DB_CONFIG, init_dev_db
from src.domain.employee.employee_domain_service import EmployeeDomainService
from src.domain.meeting_room.meeting_room_domain_service import MeetingRoomDomainService
from src.domain.reservation.errors import ReservationDomainObjectError
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.infrastructure.employee.in_memory_employee_repository import InMemoryEmployeeRepository
from src.infrastructure.meeting_room.in_memory_meeting_room_repository import InMemoryMeetingRoomRepository
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.presentation.cli.cli_util.success_message_builder import SuccessMessageBuilder
from src.presentation.cli.cli_util.user_input import CliUserInput
from src.usecase.employee.find_employee_usecase import FindEmployeeUseCase
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase
from src.usecase.reservation.errors import ReservationUsecaseError
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase


class Task使用人数:
    """
    クラス名どうしよう？
    メソッド名どうしよう？
    """

    def exe(self) -> str:
        while True:
            input_number_of_participants = input('使用人数は？ > ')

            if input_number_of_participants == '':
                print('空文字はだめだぞ？')
            elif not input_number_of_participants.isdigit():
                print('数字を入力してね')
            else:
                return input_number_of_participants


class Task使用日:
    def exe(self) -> str:
        while True:
            input_use_date = input('使用日は？(yyyymmdd) > ')

            if input_use_date == '':
                print('空文字はだめだぞ？')
            elif self.is_yyyymmdd_じゃないぞ(input_use_date):
                print('使用日は yyyymmdd のフォーマットで入力してくださいね')
            else:
                return input_use_date

    def is_yyyymmdd_じゃないぞ(self, input_use_date: str) -> bool:
        try:
            datetime.datetime.strptime(input_use_date, '%Y%m%d')
            return False
        except ValueError:
            return True


class Task開始時刻:
    def exe(self) -> str:
        while True:
            input_use_date = input('開始時刻は？(hhii) > ')

            if input_use_date == '':
                print('空文字はだめだぞ？')
            elif self.is_hhii_じゃないぞ(input_use_date):
                print('使用日は hhii のフォーマットで入力してくださいね')
            else:
                return input_use_date

    def is_hhii_じゃないぞ(self, input_use_start_time: str) -> bool:
        try:
            datetime.datetime.strptime(input_use_start_time, '%H%M')
            return False
        except ValueError:
            return True


class Task終了時刻:
    def exe(self) -> str:
        while True:
            input_use_date = input('終了時刻は？(hhii) > ')

            if input_use_date == '':
                print('空文字はだめだぞ？')
            elif self.is_hhii_じゃないぞ(input_use_date):
                print('使用日は hhii のフォーマットで入力してくださいね')
            else:
                return input_use_date

    def is_hhii_じゃないぞ(self, input_use_start_time: str) -> bool:
        try:
            datetime.datetime.strptime(input_use_start_time, '%H%M')
            return False
        except ValueError:
            return True


class Task会議室ID:
    def exe(self) -> str:
        while True:
            input_meeting_room_id = input('会議室IDは？(RoomA or RoomB or RoomC) > ')

            # 存在する会議室IDの中から選ばせるようにUIで制約を設けるなら、CLIアプリにおいてのみ、
            # 後半のバリデーションはしなくても、「一応」成立する。
            if input_meeting_room_id == '':
                print('空文字はだめだぞ？')
            else:
                return input_meeting_room_id


class Task社員ID:
    def exe(self) -> str:
        while True:
            input_employee_id = input('社員IDは？ > ')

            if input_employee_id == '':
                print('空文字はだめだぞ？')
            else:
                return input_employee_id


def 新規予約():
    database_manager = DatabaseManager(DEV_DB_CONFIG)

    # TODO: ここのDIの仕方も、違うところでやるんだろう( Python Injectorとか？）
    reservation_repository = OratorReservationRepository(database_manager)
    domain_service = ReservationDomainService(reservation_repository)
    usecase = ReserveMeetingRoomUsecase(reservation_repository, domain_service)

    init_dev_db()  # 検証しやすくするために毎回DBを初期化する
    # input_使用日 = Task使用日().exe()
    # input_開始時刻 = Task開始時刻().exe()
    # input_終了時刻 = Task終了時刻().exe()
    # input_会議室ID = Task会議室ID().exe()
    # input_社員ID = Task社員ID().exe()
    # input_使用人数 = Task使用人数().exe()

    # user_input = CliUserInput(input_使用日,
    #                           input_開始時刻,
    #                           input_終了時刻,
    #                           input_会議室ID,
    #                           input_社員ID,
    #                           input_使用人数)

    user_input = CliUserInput('20200520',
                              '1100',
                              '1300',
                              'A',
                              '001',
                              '5')

    try:
        reservation = user_input.to_reservation()
    except ReservationDomainObjectError as e:
        print(e)
        exit()

    try:
        usecase.reserve_meeting_room(reservation)
    except ReservationUsecaseError as e:
        print(e)
        exit()

    # MeetingRoom に関する準備
    meeting_room_repository = InMemoryMeetingRoomRepository()
    meeting_room_domain_service = MeetingRoomDomainService(meeting_room_repository)
    find_meeting_room_usecase = FindMeetingRoomUseCase(meeting_room_repository, meeting_room_domain_service)

    # Employee に関する準備
    employee_repository = InMemoryEmployeeRepository()
    employee_domain_service = EmployeeDomainService(employee_repository)
    find_employee_usecase = FindEmployeeUseCase(employee_repository, employee_domain_service)

    success_message_builder = SuccessMessageBuilder(find_meeting_room_usecase, find_employee_usecase)

    success_message = success_message_builder.build(reservation)

    print(success_message)


def main():
    try:
        新規予約()
    except KeyboardInterrupt:
        print('Bye!')
    except Exception as e:
        print(e)
        print('500 Internal Server Error')


if __name__ == '__main__':
    main()
