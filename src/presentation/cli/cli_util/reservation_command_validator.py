from src.presentation.cli.cli_util.user_raw_input import CliUserRawInput
from src.presentation.cli.cli_util.validation_result import CliValidationResult


class CliReservationCommandValidator:

    @classmethod
    def validate(cls, user_raw_input: CliUserRawInput) -> CliValidationResult:
        messages = []

        if user_raw_input.date == '':
            messages.append('日付が未入力です')

        if user_raw_input.end_time == '':
            messages.append('終了時刻が未入力です')

        return CliValidationResult(messages)
