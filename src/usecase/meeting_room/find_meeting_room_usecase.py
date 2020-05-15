from dataclasses import dataclass

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository


@dataclass
class FindMeetingRoomUseCase:
    meeting_room_repository: MeetingRoomRepository

    def find_by_id(self, meeting_room_id: MeetingRoomId) -> MeetingRoom:
        pass
