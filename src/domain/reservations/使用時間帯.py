from dataclasses import dataclass

from src.domain.reservations import 使用日時


@dataclass(frozen=True)
class 使用時間帯:
    start: 使用日時
    end: 使用日時
