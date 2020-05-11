import dataclasses

import pytest

from src.presentation.cli.cli_util.reservation_command_validator import CliReservationCommandValidator
from src.presentation.cli.cli_util.user_raw_input import UserRawInput
from src.presentation.cli.cli_util.validation_result import CliValidationResult


class TestCliReservationCommandValidator:
    """
    - バリデーションする項目
        - [ ] 空文字チェック

        - [ ] 日付や時刻に関するフォーマットチェック
            - [ ] 日付+開始時刻 が 正しいdatetime型にできるかどうか
            - [ ] 日付+終了時刻 が 正しいdatetime型にできるかどうか

        - [ ] 参加人数
            - [ ] 1以上の整数？

    - バリデーションしない項目
        - [x] 開始時刻と終了時刻の関係性のチェックはしない

    - 謎の項目
        - [ ] 全角を許容するか？
        - [ ] 文字数の最大値(たとえば、文字数が10万文字入力されると困る)
        - [ ] 他にもたぶんあるけど、まあいいよ。
    """

    @pytest.fixture
    def valid_user_raw_input(self) -> UserRawInput:
        return UserRawInput(date='20200516',
                            start_time='1100',
                            end_time='1200',
                            meeting_room_id='A',
                            reserver_id='Bob',
                            number_of_participants='4')

    def test_入力に不備がない場合はこうなる(self, valid_user_raw_input: UserRawInput):
        expected = CliValidationResult(messages=[])

        assert expected == CliReservationCommandValidator.validate(valid_user_raw_input)

    def test_未入力は許さない_日付(self, valid_user_raw_input: UserRawInput):
        user_raw_input = dataclasses.replace(valid_user_raw_input, date='')

        expected = CliValidationResult(messages=['日付が未入力です'])

        assert expected == CliReservationCommandValidator.validate(user_raw_input)

    def test_未入力は許さない_2つ未入力があるとき_日付と終了時刻(self, valid_user_raw_input: UserRawInput):
        user_raw_input = dataclasses.replace(valid_user_raw_input, date='', end_time='')

        expected = CliValidationResult(messages=['日付が未入力です', '終了時刻が未入力です'])

        assert expected == CliReservationCommandValidator.validate(user_raw_input)
