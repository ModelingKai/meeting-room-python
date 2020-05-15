import pytest

from src.domain.meeting_room.errors import NotFoundMeetingRoomIdError
from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_id_factory import MeetingRoomIdFactory
from src.infrastructure.meeting_room.in_memory_meeting_room_repository import InMemoryMeetingRoomRepository


class TestMeetingRoomIdFactory:
    def setup(self):
        self.repository = InMemoryMeetingRoomRepository()
        self.factory = MeetingRoomIdFactory(self.repository)

    def test_存在しない会議室IDが与えられたらエラーとなる(self):
        with pytest.raises(NotFoundMeetingRoomIdError):
            self.factory.create('NotExistId')

    def test_正しい会議室IDを作れる(self):
        meeting_room_id = MeetingRoomId('A')
        self.repository.data[meeting_room_id] = MeetingRoom(meeting_room_id, '大会議室')

        assert meeting_room_id == self.factory.create('A')
