from dataclasses import dataclass

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id_factory import MeetingRoomIdFactory
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository
from src.usecase.meeting_room.find_meeting_room_commnad import FindMeetingRoomCommand


@dataclass
class FindMeetingRoomUseCase:
    repository: MeetingRoomRepository

    def find_meeting_room(self, command: FindMeetingRoomCommand) -> MeetingRoom:
        id_factory = MeetingRoomIdFactory(self.repository)
        meeting_room_id = id_factory.create(command.meeting_room_id)

        # ID生成用のファクトリを使っているので、Noneになることはないんだぞ
        return self.repository.find_by_id(meeting_room_id)
