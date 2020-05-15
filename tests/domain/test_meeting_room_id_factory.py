import pytest

from src.domain.meeting_room.errors import NotFoundMeetingRoomIdError
from src.domain.meeting_room.meeting_room_id_factory import MeetingRoomIdFactory
from src.infrastructure.meeting_room.in_memory_meeting_room_repository import InMemoryMeetingRoomRepository


class TestMeetingRoomIdFactory:
    def test_存在しない会議室IDが与えられたらエラーとなる(self):
        self.repository = InMemoryMeetingRoomRepository()
        self.factory = MeetingRoomIdFactory(self.repository)

        with pytest.raises(NotFoundMeetingRoomIdError):
            self.factory.create_あとでなおす('NotExistId')
