import uuid

import freezegun
import pytest

from src.domain.employee.社員ID import 社員ID
from src.domain.meeting_room.会議室ID import 会議室ID
from src.domain.reservation.errors import その会議室はその時間帯では予約ができませんよエラー
from src.domain.reservation.reservation import Reservation
from src.domain.reservation.reservation_domain_service import ReservationDomainService
from src.domain.reservation.reservation_id import ReservationId
from src.domain.reservation.予約時間帯 import 予約時間帯
from src.domain.reservation.使用人数 import 使用人数
from src.domain.reservation.使用日時 import 使用日時
from src.infrastructure.reservation.in_memory_reservation_repository import InMemoryReservationRepository
from src.usecase.reserve_meeting_room_usecase import ReserveMeetingRoomUsecase


@freezegun.freeze_time('2020-4-1 10:00')
def test_会議室を予約する_正常系():
    expected = Reservation(ReservationId(str(uuid.uuid4())),
                           予約時間帯(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00)),
                           使用人数(4),
                           会議室ID(str(uuid.uuid4())),
                           社員ID(str(uuid.uuid4())))

    reservation_repository = InMemoryReservationRepository()
    domain_service = ReservationDomainService(reservation_repository)
    usecase = ReserveMeetingRoomUsecase(reservation_repository, domain_service)

    usecase.reserve_meeting_room(expected)

    assert expected == reservation_repository.data[expected.id]


@freezegun.freeze_time('2020-4-1 10:00')
def test_会議室を予約する_異常系_会議室と予約時間帯が完全に被っている():
    # テストケースとしては、完全一致しかないが、他のパターンは時間帯予約のテストケースでクリアしている
    # ので、特に不安はない
    # 予約エラーを細分化するのであれば、その分類ごとにテストを用意してもいいかもしれない。でも用意しない
    meeting_room_id = 会議室ID(str(uuid.uuid4()))
    reservation_予約時間帯 = 予約時間帯(使用日時(2020, 4, 2, 13, 00), 使用日時(2020, 4, 2, 14, 00))

    exist_reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                    reservation_予約時間帯,
                                    使用人数(3),
                                    meeting_room_id,
                                    社員ID(str(uuid.uuid4())))

    new_reservation = Reservation(ReservationId(str(uuid.uuid4())),
                                  reservation_予約時間帯,
                                  使用人数(4),
                                  meeting_room_id,
                                  社員ID(str(uuid.uuid4())))

    reservation_repository = InMemoryReservationRepository()
    reservation_repository.data[exist_reservation.id] = exist_reservation

    domain_service = ReservationDomainService(reservation_repository)
    usecase = ReserveMeetingRoomUsecase(reservation_repository, domain_service)

    with pytest.raises(その会議室はその時間帯では予約ができませんよエラー):
        usecase.reserve_meeting_room(new_reservation)
