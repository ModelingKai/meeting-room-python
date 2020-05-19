from orator import DatabaseManager, Model

from src.domain.meeting_room.meeting_room import MeetingRoom
from src.domain.meeting_room.meeting_room_id import MeetingRoomId
from src.infrastructure.meeting_room.orator.orator_meeting_room_model import OratorMeetingRoomModel
from src.infrastructure.meeting_room.orator.orator_meeting_room_repository import OratorMeetingRoomRepository
from tests.usecase.reservation.orator.migrate_in_memory import migrate_in_memory, TEST_DB_CONFIG


class TestOratorMeetingRoomRepository:
    def setup(self):
        database_manager = DatabaseManager(TEST_DB_CONFIG)
        Model.set_connection_resolver(database_manager)

        migrate_in_memory(database_manager)

        self.repository = OratorMeetingRoomRepository()

    def test_find_by_id(self):
        meeting_room = MeetingRoom(MeetingRoomId('A'), '大会議室')

        OratorMeetingRoomModel.to_orator_model(meeting_room).save()

        assert self.repository.find_by_id(meeting_room.id) == meeting_room

    def test_find_by_id_return_None_when_not_exist_id(self):
        assert self.repository.find_by_id(MeetingRoomId('Z')) is None

    def test_find_all(self):
        meeting_room_a = MeetingRoom(MeetingRoomId('A'), '大会議室')
        meeting_room_b = MeetingRoom(MeetingRoomId('B'), '中会議室')
        meeting_room_c = MeetingRoom(MeetingRoomId('C'), '小会議室')

        OratorMeetingRoomModel.to_orator_model(meeting_room_a).save()
        OratorMeetingRoomModel.to_orator_model(meeting_room_b).save()
        OratorMeetingRoomModel.to_orator_model(meeting_room_c).save()

        assert self.repository.find_all() == [meeting_room_a, meeting_room_b, meeting_room_c]
