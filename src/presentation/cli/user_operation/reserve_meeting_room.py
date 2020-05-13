from orator import DatabaseManager

from src.app_environment.init_dev_db import DEV_DB_CONFIG
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.presentation.cli.cli_util.reservation_command_validator import CliReservationCommandValidator
from src.presentation.cli.cli_util.response_object_factory import ResponseObjectFactory
from src.presentation.cli.cli_util.user_input import CliUserInput
from src.usecase.employee.mock_find_employee_usecase import MockFindEmployeeUseCase
from src.usecase.meeting_room.mock_find_meeting_room_usecase import MockFindMeetingRoomUseCase
from src.usecase.reservation.errors import その会議室はその時間帯では予約ができませんよエラー
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase


def main():
    database_manager = DatabaseManager(DEV_DB_CONFIG)

    # TODO: ここのDIの仕方も、違うところでやるんだろう( Python Injectorとか？）
    reservation_repository = OratorReservationRepository(database_manager)
    domain_service = ReservationDomainService(reservation_repository)
    usecase = ReserveMeetingRoomUsecase(reservation_repository, domain_service)

    # TODO: input()でユーザからデータ入力する
    input_date = '20200517'
    input_start_time = '1100'
    input_end_time = '1300'
    input_meeting_room_id = 'A'
    input_reserver_id = 'Bob'
    input_number_of_participants = '4'

    user_input = CliUserInput(input_date,
                              input_start_time,
                              input_end_time,
                              input_meeting_room_id,
                              input_reserver_id,
                              input_number_of_participants)

    validation_result = CliReservationCommandValidator.validate(user_input)

    if validation_result.is_not_satisfied():
        validation_result.display_messages()
        exit()

    reservation = user_input.to_reservation()

    try:
        usecase.reserve_meeting_room(reservation)
    except その会議室はその時間帯では予約ができませんよエラー as e:
        print(e)
        exit()
    except Exception as e:
        # TODO: これも独自例外にするかも
        print('なんか落ちた。ごめんね。', e)
        exit()

    # TODO: Mockのユースケースを本物に差し替える
    factory = ResponseObjectFactory(MockFindEmployeeUseCase(), MockFindMeetingRoomUseCase())
    response_object = factory.create(reservation)

    print(response_object)


if __name__ == '__main__':
    main()
