from dataclasses import dataclass

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository


@dataclass
class MeetingRoomIdFactory:
    meeting_room_repository: MeetingRoomRepository

    def create(self, param):
        return MeetingRoomId(param)
