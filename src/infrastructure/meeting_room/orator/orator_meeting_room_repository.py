from typing import Optional, List

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository
from src.infrastructure.meeting_room.orator.orator_meeting_room_model import OratorMeetingRoomModel


class OratorMeetingRoomRepository(MeetingRoomRepository):

    def find_by_id(self, meeting_room_id: MeetingRoomId) -> Optional[MeetingRoom]:
        orator_meeting_room = OratorMeetingRoomModel.find(meeting_room_id.value)

        if orator_meeting_room is None:
            return None

        return OratorMeetingRoomModel.to_meeting_room(orator_meeting_room)

    def find_all(self) -> List[MeetingRoom]:
        return list(map(OratorMeetingRoomModel.to_meeting_room, OratorMeetingRoomModel.all()))
