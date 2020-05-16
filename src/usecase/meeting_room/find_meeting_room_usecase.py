from dataclasses import dataclass

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_domain_service import MeetingRoomDomainService
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository
from src.usecase.meeting_room.errors import NotFoundMeetingRoomIdError
from src.usecase.meeting_room.find_meeting_room_commnad import FindMeetingRoomCommand


@dataclass
class FindMeetingRoomUseCase:
    repository: MeetingRoomRepository
    domain_service: MeetingRoomDomainService

    def find_meeting_room(self, command: FindMeetingRoomCommand) -> MeetingRoom:
        meeting_room_id = MeetingRoomId(command.meeting_room_id)

        if not self.domain_service.exists_id(meeting_room_id):
            raise NotFoundMeetingRoomIdError('そのような会議室IDはありません')

        meeting_room = self.repository.find_by_id(meeting_room_id)

        assert meeting_room

        return meeting_room
