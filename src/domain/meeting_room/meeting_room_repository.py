from abc import ABCMeta, abstractmethod
from typing import Optional

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId


class MeetingRoomRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_id(self, meeting_room_id: MeetingRoomId) -> Optional[MeetingRoom]:
        pass
