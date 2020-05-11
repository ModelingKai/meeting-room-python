from dataclasses import dataclass


@dataclass
class CliUserRawInput:
    date: str
    start_time: str
    end_time: str
    meeting_room_id: str
    reserver_id: str
    number_of_participants: str
