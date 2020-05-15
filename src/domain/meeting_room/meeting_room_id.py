from dataclasses import dataclass


@dataclass(frozen=True)
class MeetingRoomId:
    value: str
