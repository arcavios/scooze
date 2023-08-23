import json
from pprint import pprint

import pytest
from scooze.card import FullCard
from scooze.models.card import FullCardModel


@pytest.fixture
def temp_fixture() -> str:
    return "some stuff"


def test_temp(temp_fixture):
    assert temp_fixture == "some stuff"


# TODO(#65): WRITE TESTS FOR CARD OBJECT HERE


@pytest.fixture
def power9() -> dict:
    with open("./data/test/test_cards.json") as file:
        return json.load(file)


@pytest.fixture
def pearl(power9) -> dict:
    return power9["p9"][0]


def test_full_card_model_from_json(pearl):
    fullcardmodel = FullCardModel.model_construct(**pearl)
    pprint(fullcardmodel)
    pprint(fullcardmodel.scryfall_id)
    assert False


def test_full_card_obj_from_json(pearl):
    fullcard = FullCard(**pearl)
    pprint(fullcard.__dict__)
    assert False


def test_model_from_obj(pearl):
    fullcardobj = FullCard(**pearl)
    fullcardmodel = FullCardModel.model_construct(**fullcardobj.__dict__)
    pprint(fullcardmodel)
    pprint(fullcardmodel.scryfall_id)
    assert False


def test_obj_from_model(pearl):
    fullcardmodel = FullCardModel.model_construct(**pearl)
    fullcardobj = FullCard(**fullcardmodel.model_dump())
    pprint(fullcardobj.__dict__)
    pprint(f"PRICES: {fullcardobj.prices.__dict__}")
    pprint(f"IMAGEURIS: {fullcardobj.image_uris.__dict__}")
    assert False
