from dataclasses import dataclass

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository
from src.usecase.meeting_room.errors import NotFoundMeetingRoomIdError


@dataclass
class MeetingRoomIdFactory:
    meeting_room_repository: MeetingRoomRepository

    def create(self, meeting_room_id_str: str) -> MeetingRoomId:
        meeting_rooms = self.meeting_room_repository.find_all()

        for meeting_room in meeting_rooms:
            if meeting_room.id.value == meeting_room_id_str:
                return meeting_room.id

        raise NotFoundMeetingRoomIdError('そのような会議室IDはありません')
