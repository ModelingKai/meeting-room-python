from dataclasses import dataclass

from src.domain.meeting_room.meeting_room_id import MeetingRoomId


@dataclass
class MeetingRoom:
    id: MeetingRoomId
    name: str