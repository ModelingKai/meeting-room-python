from __future__ import annotations

from orator import Model

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId


class OratorMeetingRoomModel(Model):
    __table__ = 'meeting_rooms'

    def __repr__(self) -> str:
        # ださいけど、情報がわかりやすくなるので実装している
        tmp = ', '.join([f'{k}={v}' for k, v in self.to_dict().items()])
        repr_like_dataclass = f'{self.__class__.__name__}({tmp})'

        return repr_like_dataclass

    @classmethod
    def to_meeting_room(cls, source: OratorMeetingRoomModel) -> MeetingRoom:
        return MeetingRoom(MeetingRoomId(source.id), source.name)

    @classmethod
    def to_orator_model(cls, meeting_room: MeetingRoom) -> OratorMeetingRoomModel:
        orator_meeting_room = OratorMeetingRoomModel()
        orator_meeting_room.id = meeting_room.id.value
        orator_meeting_room.name = meeting_room.name

        return orator_meeting_room
