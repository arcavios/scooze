import pytest
import json
from pprint import pprint
from scooze.models.card import FullCardModel
from scooze.card import FullCard


@pytest.fixture
def temp_fixture() -> str:
    return "some stuff"


def test_temp(temp_fixture):
    assert temp_fixture == "some stuff"


# TODO(#65): WRITE TESTS FOR CARD OBJECT HERE

@pytest.fixture
def power9() -> dict:
    with open('./data/test/test_cards.json') as file:
        return json.load(file)

@pytest.fixture
def pearl(power9) -> dict:
    return power9["p9"][0]


def test_full_card_model_from_json(pearl):
    fullcard = FullCardModel.model_construct(**pearl)
    pprint(fullcard)
    assert False

def test_full_card_obj_from_json(pearl):
    fullcard = FullCard(**pearl)
    pprint(fullcard.__dict__)
    assert False
