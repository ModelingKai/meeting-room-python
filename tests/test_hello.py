from src.hello import Hello


def test_car_brake():
    hello = Hello()
    result = hello.say()
    assert result == 'hello'
