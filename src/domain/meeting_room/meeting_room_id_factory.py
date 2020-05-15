from dataclasses import dataclass

from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.domain.meeting_room.meeting_room_repository import MeetingRoomRepository


@dataclass
class MeetingRoomIdFactory:
    meeting_room_repository: MeetingRoomRepository

    def create(self, meeting_room_id_str: str) -> MeetingRoomId:
        return MeetingRoomId(meeting_room_id_str)

    def create_あとでなおす(self, meeting_room_id_str: str) -> MeetingRoomId:
        pass
        # meeting_room_id_str='A'
        # repository.find_id_by_idを経由して、正しいMeetingRoomの問い合わせをする
        #
        # repository に
        # 存在するMeetingRoomIdが守れればいい

        # meeting_room = repository.find_by_id(meeting_room_id_str)
        #
        # if 存在したら:
        # return MeetingRoomId(meeting_room_id_str)
