from src.presentation.cli.cli_util.user_raw_input import UserRawInput
from src.presentation.cli.cli_util.validation_result import CliValidationResult


class CliReservationCommandValidator:

    @classmethod
    def validate(cls, user_raw_input: UserRawInput) -> CliValidationResult:
        return CliValidationResult(is_ダメ=True, messages=['日付が未入力です'])
