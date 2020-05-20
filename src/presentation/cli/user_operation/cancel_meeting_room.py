import datetime

from orator import DatabaseManager, Model

from src.app_environment.init_dev_db import DEV_DB_CONFIG
from src.domain.reservation.available_reservation_specification import AvailableReservationSpecification
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.reservation.cancel_meeting_room_usecase import CancelMeetingRoomUsecase
from src.usecase.reservation.errors import ReservationUsecaseError


def my_format(r):
    return str(r)


def cancel():
    # 準備いろいろ
    database_manager = DatabaseManager(DEV_DB_CONFIG)
    Model.set_connection_resolver(database_manager)

    reservation_repository = OratorReservationRepository()
    cancel_meeting_room_usecase = CancelMeetingRoomUsecase(reservation_repository)

    # 現在有効な予約の一覧を表示して、そこからユーザーにキャンセルしたい予約を選んでもらう
    specification = AvailableReservationSpecification(datetime.datetime.now())
    reservations = reservation_repository.find_satisfying(specification)

    print('0: 操作をやめる')
    for idx, r in enumerate(reservations, start=1):
        formatted_reservation = my_format(r)
        print(f'{idx}: {formatted_reservation}')

    target_reservation_id_user_input = int(input('操作番号を選んでね > '))

    # ユーザ入力 → ドメインオブジェクト
    target_reservation = reservations[target_reservation_id_user_input - 1]
    print(target_reservation.id, 'をキャンセルするよ')

    try:
        # TODO: すべての予約をキャンセルしてしまうバグがある説？
        cancel_meeting_room_usecase.cancel_meeting_room(target_reservation.id)
    except ReservationUsecaseError as e:
        print(e)
        exit()

    print('TODO: サクセスメッセージをいい感じにつくって表示する')


def main():
    try:
        cancel()
    except Exception as e:
        print('Internal Server Error')
        # TODO: logging
        print(e)


if __name__ == '__main__':
    main()
