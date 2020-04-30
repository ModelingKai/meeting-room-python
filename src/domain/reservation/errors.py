class Not15分単位Error(Exception):
    pass


class 使用時間帯の範囲がおかしいよError(Exception):
    pass


class 未来過ぎて予約できないよError(Exception):
    pass


class 使用日時は過去であってはいけないんだよError(Exception):
    pass


class 予約時間が長すぎError(Exception):
    pass
