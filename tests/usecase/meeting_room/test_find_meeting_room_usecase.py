import pytest

from src.domain.meeting_room.errors import NotFoundMeetingRoomIdError
from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_id_factory import MeetingRoomIdFactory
from src.infrastructure.meeting_room.in_memory_meeting_room_repository import InMemoryMeetingRoomRepository
from src.usecase.meeting_room.find_meeting_room_commnad import FindMeetingRoomCommand
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase


class TestFindMeetingRoomUsecase:
    def setup(self):
        self.repository = InMemoryMeetingRoomRepository()

        id_factory = MeetingRoomIdFactory(self.repository)
        self.usecase = FindMeetingRoomUseCase(self.repository, id_factory)

    def test_会議室のIDを渡したら単一の会議室情報が取得できる(self):
        meeting_room_id = MeetingRoomId('A')
        meeting_room = MeetingRoom(meeting_room_id, '大会議室')

        self.repository.data[meeting_room_id] = meeting_room

        command = FindMeetingRoomCommand('A')

        assert meeting_room == self.usecase.find_meeting_room(command)

    def test_存在しない会議室IDを渡すとエラーになる(self):
        command = FindMeetingRoomCommand('NotExistMeetingRoomId')

        # UsecaseErrorではない点に注意
        with pytest.raises(NotFoundMeetingRoomIdError):
            self.usecase.find_meeting_room(command)
