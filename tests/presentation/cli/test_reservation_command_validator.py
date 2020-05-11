import dataclasses

import pytest

from src.presentation.cli.cli_util.reservation_command_validator import CliReservationCommandValidator
from src.presentation.cli.cli_util.user_raw_input import UserRawInput
from src.presentation.cli.cli_util.validation_result import CliValidationResult


class TestCliReservationCommandValidator:
    @pytest.fixture
    def valid_user_raw_input(self) -> UserRawInput:
        return UserRawInput(date='20200516',
                            start_time='1100',
                            end_time='1200',
                            meeting_room_id='A',
                            reserver_id='Bob',
                            number_of_participants='4')

    def test_未入力は許さない_日付(self, valid_user_raw_input: UserRawInput):
        user_raw_input = dataclasses.replace(valid_user_raw_input, date='')

        expected = CliValidationResult(is_ダメ=True, messages=['日付が未入力です'])

        assert expected == CliReservationCommandValidator.validate(user_raw_input)
