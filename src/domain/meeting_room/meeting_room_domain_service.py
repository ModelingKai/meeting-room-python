from dataclasses import dataclass

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository


@dataclass
class MeetingRoomDomainService:
    repository: MeetingRoomRepository

    def exists_id(self, meeting_room_id: MeetingRoomId) -> bool:
        exist_meeting_rooms = self.repository.find_all()

        for exist_meeting_room in exist_meeting_rooms:
            if exist_meeting_room.id == meeting_room_id:
                return True

        return False
