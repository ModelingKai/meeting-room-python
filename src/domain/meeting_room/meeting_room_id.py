import re
from dataclasses import dataclass

from src.domain.meeting_room.errors import InvalidFormatMeetingRoomIdError


@dataclass(frozen=True)
class MeetingRoomId:
    value: str

    def __post_init__(self):
        pattern = r'[A-Z]'

        if not re.fullmatch(pattern, self.value):
            raise InvalidFormatMeetingRoomIdError('会議室IDは大文字のアルファベット1字でなければなりません')
