import pytest

from src.domain.meeting_room.errors import InvalidFormatMeetingRoomIdError
from src.domain.meeting_room.meeting_room_id import MeetingRoomId


class TestMeetingRoomId:
    @pytest.mark.parametrize('value', ['a', 'ABC'])
    def test_会議室IDは大文字のアルファベット1字でなければなりません(self, value: str):
        with pytest.raises(InvalidFormatMeetingRoomIdError):
            MeetingRoomId(value)
