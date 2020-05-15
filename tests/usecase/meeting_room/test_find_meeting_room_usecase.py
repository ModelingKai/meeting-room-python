from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id_factory import MeetingRoomIdFactory
from src.infrastructure.meeting_room.in_memory_meeting_room_repository import InMemoryMeetingRoomRepository
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase


class TestFindMeetingRoomUsecase:
    def test_会議室のIDを渡したら単一の会議室情報が取得できる(self):
        repository = InMemoryMeetingRoomRepository()
        factory = MeetingRoomIdFactory(repository)
        meeting_room_id = factory.create('A')

        expected = MeetingRoom(meeting_room_id, '大会議室')

        usecase = FindMeetingRoomUseCase(repository)
        actual = usecase.find_by_id(meeting_room_id)

        assert expected == actual
