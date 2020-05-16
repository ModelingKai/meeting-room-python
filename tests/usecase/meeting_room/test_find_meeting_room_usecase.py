from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_domain_service import MeetingRoomDomainService
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.infrastructure.meeting_room.in_memory_meeting_room_repository import InMemoryMeetingRoomRepository
from src.usecase.meeting_room.find_meeting_room_commnad import FindMeetingRoomCommand
from src.usecase.meeting_room.find_meeting_room_usecase import FindMeetingRoomUseCase


class TestFindMeetingRoomUsecase:
    def setup(self):
        self.repository = InMemoryMeetingRoomRepository()
        domain_service = MeetingRoomDomainService(self.repository)
        self.usecase = FindMeetingRoomUseCase(self.repository, domain_service)

    def test_会議室のIDを渡したら単一の会議室情報が取得できる(self):
        meeting_room_id = MeetingRoomId('001')
        meeting_room = MeetingRoom(meeting_room_id, '大会議室')
        command = FindMeetingRoomCommand('001')

        self.repository.data[meeting_room_id] = meeting_room

        assert meeting_room == self.usecase.find_meeting_room(command)

    #
    # def test_存在しない会議室IDを渡すとエラーになる(self):
    #     command = FindMeetingRoomCommand('NotExistMeetingRoomId')
    #
    #     # UsecaseErrorではない点に注意
    #     with pytest.raises(NotFoundMeetingRoomIdError):
    #         self.usecase.find_meeting_room(command)
