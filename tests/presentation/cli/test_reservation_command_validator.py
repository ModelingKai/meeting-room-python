from src.presentation.cli.cli_util.reservation_command_validator import CliReservationCommandValidator
from src.presentation.cli.cli_util.user_raw_input import UserRawInput
from src.presentation.cli.cli_util.validation_result import CliValidationResult


class TestCliReservationCommandValidator:
    def test_validate(self):
        # 0. ユーザからの入力を受け取る
        input_date = ''  # '20200516'  # input('日付は？')
        input_start_time = '1100'  # input('開始時刻は？')
        input_end_time = '1200'  # input('終了時刻は？')
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

        expected = CliValidationResult(is_ダメ=True, messages=['日付が未入力です'])
        # 返り値
        # 問題あるかどうか
        # どこの入力値がダメだったのかという、エラーメッセージ内容
        validation_result = CliReservationCommandValidator.validate(user_raw_input)

        assert expected == validation_result
