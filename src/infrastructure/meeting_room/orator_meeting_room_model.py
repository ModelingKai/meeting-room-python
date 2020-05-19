from orator import Model


class OratorMeetingRoomModel(Model):
    __table__ = 'meeting_rooms'

    def __repr__(self) -> str:
        # ださいけど、情報がわかりやすくなるので実装している
        tmp = ', '.join([f'{k}={v}' for k, v in self.to_dict().items()])
        repr_like_dataclass = f'{self.__class__.__name__}({tmp})'

        return repr_like_dataclass
