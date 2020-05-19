from typing import List, Optional

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository


class OratorMeetingRoomRepository(MeetingRoomRepository):

    def find_by_id(self, meeting_room_id: MeetingRoomId) -> Optional[MeetingRoom]:
        pass

    def find_all(self) -> List[MeetingRoom]:
        pass


class TestOratorMeetingRoomRepository:
    def test_find_by_id(self):
        repository = OratorMeetingRoomRepository()

        meeting_room_id = MeetingRoomId('A')
        actual = repository.find_by_id(meeting_room_id)

        assert MeetingRoom(meeting_room_id, '大会議室') == actual
