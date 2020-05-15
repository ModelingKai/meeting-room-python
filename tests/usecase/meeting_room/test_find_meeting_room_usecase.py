import pytest

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id_factory import MeetingRoomIdFactory
from src.infrastructure.meeting_room.in_memory_meeting_room_repository import InMemoryMeetingRoomRepository
from src.usecase.meeting_room.errors import NotFoundMeetingRoomError
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase


class TestFindMeetingRoomUsecase:
    def setup(self):
        self.repository = InMemoryMeetingRoomRepository()

        self.factory = MeetingRoomIdFactory(self.repository)
        self.usecase = FindMeetingRoomUseCase(self.repository)

    def test_会議室のIDを渡したら単一の会議室情報が取得できる(self):
        meeting_room_id = self.factory.create('A')
        meeting_room = MeetingRoom(meeting_room_id, '大会議室')

        self.repository.data[meeting_room_id] = meeting_room

        assert meeting_room == self.usecase.find_by_id(meeting_room_id)

    def test_存在しない会議室IDが与えられたらエラーとなる(self):
        meeting_room_id = self.factory.create('NotExistId')

        with pytest.raises(NotFoundMeetingRoomError):
            self.usecase.find_by_id(meeting_room_id)
