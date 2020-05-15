from dataclasses import dataclass

from src.domain.meeting_room.errors import NotFoundMeetingRoomIdError
from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_id_factory import MeetingRoomIdFactory
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository
from src.usecase.meeting_room.errors import NotFoundMeetingRoomError
from src.usecase.meeting_room.find_meeting_room_commnad import FindMeetingRoomCommand


@dataclass
class FindMeetingRoomUseCase:
    repository: MeetingRoomRepository

    def find_by_id(self, meeting_room_id: MeetingRoomId) -> MeetingRoom:
        meeting_room = self.repository.find_by_id(meeting_room_id)

        if meeting_room is None:
            raise NotFoundMeetingRoomError('そんな会議室はありませんぜ')

        return meeting_room

    def find_employee(self, command: FindMeetingRoomCommand) -> MeetingRoom:
        try:
            id_factory = MeetingRoomIdFactory(self.repository)
            meeting_room_id = id_factory.create(command.meeting_room_id)  # 例外処理はどこで担当？
        except NotFoundMeetingRoomIdError:
            raise NotFoundMeetingRoomError()  # ユースケースエラーを送出し直す？

        meeting_room = self.repository.find_by_id(meeting_room_id)

        if meeting_room is None:
            raise NotFoundMeetingRoomError('そんな会議室はありませんぜ')

        return meeting_room
