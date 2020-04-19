from src.domain.reservations.使用日時 import 使用日時


def test_使用日時が15分単位であること():
    jikan = 使用日時(2020, 4, 20, 10, 15)
    assert jikan.minute == 15
