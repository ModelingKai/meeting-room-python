from src.presentation.cli.cli_util.user_raw_input import UserRawInput
from src.presentation.cli.cli_util.validation_result import CliValidationResult


class CliReservationCommandValidator:

    @classmethod
    def validate(cls, user_raw_input: UserRawInput) -> CliValidationResult:
        messages = []

        if user_raw_input.date == '':
            messages.append('日付が未入力です')
        if user_raw_input.end_time == '':
            messages.append('終了時刻が未入力です')

        if messages:
            return CliValidationResult(is_ダメ=True, messages=messages)

        return CliValidationResult(is_ダメ=False, messages=[])
