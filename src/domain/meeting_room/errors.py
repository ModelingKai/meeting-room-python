class MeetingRoomDomainObjectError(Exception):
    pass


class NotFoundMeetingRoomIdError(MeetingRoomDomainObjectError):
    pass


class InvalidFormatMeetingRoomIdError(MeetingRoomDomainObjectError):
    pass
