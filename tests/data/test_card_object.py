import pytest


@pytest.fixture
def temp_fixture() -> str:
    return "some stuff"


def test_temp(temp_fixture):
    assert temp_fixture == "some stuff"


# TODO: WRITE TESTS FOR CARD OBJECT HERE
