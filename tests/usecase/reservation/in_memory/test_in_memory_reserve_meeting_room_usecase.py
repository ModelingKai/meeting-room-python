import dataclasses
import datetime
import uuid

import pytest

from src.domain.reservation.number_of_participants import NumberOfParticipants
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.reservation_status import ReservationStatus
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reservation.errors import その会議室はその時間帯では予約ができませんよエラー
from src.usecase.reservation.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase
from tests.domain.reservation.dummy_reservation_builder import DummyReservationBuilder


class TestInMemoryReserveMeetingRoomUsecase:
    def setup(self):
        self.reservation_repository = InMemoryReservationRepository()
        domain_service = ReservationDomainService(self.reservation_repository)
        self.usecase = ReserveMeetingRoomUsecase(self.reservation_repository, domain_service)

    @pytest.fixture
    def reservation(self) -> Reservation:
        return DummyReservationBuilder(datetime.datetime.now()).build()

    def test_会議室を予約する_正常系(self, reservation):
        self.usecase.reserve_meeting_room(reservation)

        assert reservation == self.reservation_repository.data[reservation.id]

    def test_会議室を予約する_異常系_会議室と予約時間帯が完全に被っている(self, reservation):
        # このテストクラスでは、予約時間帯が完全一致のテストケースしか要していないが、
        # 他のパターンは予約時間帯のテストケースでクリアしているので、特に不安はない
        # 予約エラーを細分化するのであれば、その分類ごとにテストを用意してもいいかもしれない。でも用意しない
        new_reservation = dataclasses.replace(reservation,
                                              id=ReservationId(str(uuid.uuid4())),
                                              number_of_participants=NumberOfParticipants(4))

        self.reservation_repository.data[reservation.id] = reservation

        with pytest.raises(その会議室はその時間帯では予約ができませんよエラー):
            self.usecase.reserve_meeting_room(new_reservation)

    def test_会議室を予約する_正常系_会議室と時間帯的には予約できないけどキャンセル済みだから予約できるんだなあ(self, reservation):
        exist_canceled_reservation = dataclasses.replace(reservation, reservation_status=ReservationStatus.Canceled)

        new_reservation = dataclasses.replace(exist_canceled_reservation,
                                              id=ReservationId(str(uuid.uuid4())),
                                              reservation_status=ReservationStatus.Available)

        self.reservation_repository.data[exist_canceled_reservation.id] = exist_canceled_reservation

        self.usecase.reserve_meeting_room(new_reservation)

        assert self.reservation_repository.data[new_reservation.id] == new_reservation
