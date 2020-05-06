from src.presentation.user_raw_input import UserRawInput


class ReservationCommandValidator:

    @classmethod
    def validate(cls, user_raw_input: UserRawInput):
        # バリデーション結果
        # MEMO: True/False は わかりにくい
        # MEMO: もしかしたら、バリデーション結果オブジェクトとかもあるかもしれない
        return True  # とりあえず絶対にバリデーションが通らないようにしておく
