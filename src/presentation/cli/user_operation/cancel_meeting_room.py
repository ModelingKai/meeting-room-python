from dataclasses import dataclass

from orator import DatabaseManager, Model

from src.app_environment.init_dev_db import DEV_DB_CONFIG
from src.domain.meeting_room.meeting_room_domain_service import MeetingRoomDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.infrastructure.meeting_room.orator.orator_meeting_room_repository import OratorMeetingRoomRepository
from src.infrastructure.reservation.orator.orator_reservation_repository import OratorReservationRepository
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase
from src.usecase.reservation.cancel_meeting_room_usecase import CancelMeetingRoomUsecase
from src.usecase.reservation.errors import ReservationUsecaseError


@dataclass
class CancelMeetingCoordinator:
    user_raw_input: Taskキャンセル対象
    cancel_meeting_room_usecase: CancelMeetingRoomUsecase
    message_builder: CliSuccessToCancelMessageBuilder

    def cancel_meeting_room(self) -> None:
        # メインフローわかりやすくね？
        user_raw_input = self._read_user_raw_input()

        target_reservation_id = self._to_reservation_id(user_raw_input)

        self._exe_cancel_usecase(target_reservation_id)

        self._display_success_message(target_reservation_id)

    def _read_user_raw_input(self):
        # 1. ユーザからの入力の受け取り(有効な予約の一覧の表示と入力受け取り)
        #   - 操作対象の表示
        #   - バリデーションする
        #   - キーボード入力の受け取り
        pass

    def _to_reservation_id(self, user_raw_input: str) -> ReservationId:
        # TODO: とりあえず user_raw_input は str としている。無理にクラスに包まなくても良さそう
        # 2: ユーザからの入力をReservationIdにマッピングする
        pass

    def _exe_cancel_usecase(self, target_reservation_id: ReservationId) -> None:
        # 3. キャンセルするユースケースの実行
        try:
            self.cancel_meeting_room_usecase.cancel_meeting_room(target_reservation_id)
        except ReservationUsecaseError as e:
            print(e)
            exit()

    def _display_success_message(self, target_reservation_id: ReservationId) -> None:
        # 4. サクセスメッセージ生成と表示
        success_message = self.message_builder.build(target_reservation_id)

        print(success_message)


def main():
    # 準備
    database_manager = DatabaseManager(DEV_DB_CONFIG)
    Model.set_connection_resolver(database_manager)

    reservation_repository = OratorReservationRepository()

    find_available_reservation_usecase = FindAvalibleReservationUsecase(reservation_repository)
    task_キャンセル対象 = Taskキャンセル対象(find_available_reservation_usecase)

    cancel_meeting_room_usecase = CancelMeetingRoomUsecase(reservation_repository)

    find_reservation_usecase = FindReservatnionUsecase()
    meeting_room_repository = OratorMeetingRoomRepository()
    meeting_room_domain_service = MeetingRoomDomainService(meeting_room_repository)
    find_meeting_room_usecase = FindMeetingRoomUseCase(meeting_room_repository, meeting_room_domain_service)

    message_builder = CliSuccessToCancelMessageBuilder(find_reservation_usecase=find_reservation_usecase,
                                                       find_meeting_room_usecase=find_meeting_room_usecase)

    coordinator = CancelMeetingCoordinator(task_キャンセル対象, cancel_meeting_room_usecase, message_builder)

    # 実行
    try:
        coordinator.cancel_meeting_room()
    except Exception as e:
        print('Internal Server Error')
        # TODO: logging
        print(e)


if __name__ == '__main__':
    main()
