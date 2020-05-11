import datetime
from abc import ABCMeta, abstractmethod


class Clock(metaclass=ABCMeta):
    @abstractmethod
    def now(self) -> datetime.datetime:
        pass
