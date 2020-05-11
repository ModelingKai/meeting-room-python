import datetime

from src.domain.shared.clock import Clock


class SystemClock(Clock):
    def now(self):
        return datetime.datetime.now()
