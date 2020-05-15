from dataclasses import dataclass

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository


@dataclass
class FindMeetingRoomUseCase:
    repository: MeetingRoomRepository

    def find_by_id(self, meeting_room_id: MeetingRoomId) -> MeetingRoom:
        meeting_room = self.repository.find_by_id(meeting_room_id)

        return meeting_room
