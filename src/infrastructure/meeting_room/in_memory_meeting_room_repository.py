from dataclasses import dataclass, field
from typing import Optional, Dict

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository


@dataclass
class InMemoryMeetingRoomRepository(MeetingRoomRepository):
    data: Dict[MeetingRoomId, MeetingRoom] = field(default_factory=dict)

    def find_by_id(self, meeting_room_id: MeetingRoomId) -> Optional[MeetingRoom]:
        return self.data.get(meeting_room_id)
