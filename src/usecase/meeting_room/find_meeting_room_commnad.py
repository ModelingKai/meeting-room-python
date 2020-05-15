from dataclasses import dataclass


@dataclass
class FindMeetingRoomCommand:
    meeting_room_id: str
