from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase


class MockFindMeetingRoomUseCase(FindMeetingRoomUseCase):
    # TODO: 命名は InMemory かもしれない

    def find_by_id(self, meeting_room_id: MeetingRoomId) -> MeetingRoom:
        return MeetingRoom(meeting_room_id, name='会議室A')
