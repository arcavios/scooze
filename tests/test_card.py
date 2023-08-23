import json
from pprint import pprint

import pytest
from scooze.card import Card, FullCard, OracleCard
from scooze.models.card import FullCardModel


@pytest.fixture
def temp_fixture() -> str:
    return "some stuff"


def test_temp(temp_fixture):
    assert temp_fixture == "some stuff"


# TODO(#65): WRITE TESTS FOR CARD OBJECT HERE


import json


@pytest.fixture
def fullcards_json() -> list[str]:
    with open("./data/test/test_cards.jsonl", "r") as json_file:
        json_list = list(json_file)

    return json_list


@pytest.fixture
def fullcards(fullcards_json) -> list[FullCard]:
    cards = []
    for json_str in fullcards_json:
        card_json = json.loads(json_str)
        card = FullCard.from_json(card_json)
        cards.append(card)

    return cards


# TODO: Scope this so that it only runs once at the beginning because we don't want to check every card every time
@pytest.fixture
def pearl(fullcards) -> FullCard:
    for card in fullcards:
        if card.scryfall_id == "8ebe4be7-e12a-4596-a899-fbd5b152e879":
            return card

    return None


@pytest.fixture
def fable(fullcards) -> FullCard:
    for card in fullcards:
        if card.scryfall_id == "24c0d87b-0049-4beb-b9cb-6f813b7aa7dc":
            return card

    return None


# def test_full_card_model_from_json(pearl):
#     fullcardmodel = FullCardModel.model_construct(**pearl)
#     pprint(fullcardmodel)
#     pprint(fullcardmodel.scryfall_id)
#     assert False


# def test_pearl(pearl):
#     pprint(pearl.__dict__)
#     assert False


def test_fable(fable):
    pprint(fable.__dict__)
    assert False


# def test_oracle_card_obj_from_json(pearl):
#     oraclecard = OracleCard(**pearl)
#     pprint(oraclecard.__dict__)
#     assert False


# def test_simple_card_obj_from_json(pearl):
#     simplecard = Card(**pearl)
#     pprint(simplecard.__dict__)
#     assert False


# def test_model_from_obj(pearl):
#     fullcardobj = FullCard(**pearl)
#     fullcardmodel = FullCardModel.model_construct(**fullcardobj.__dict__)
#     pprint(fullcardmodel)
#     pprint(fullcardmodel.scryfall_id)
#     assert False


# def test_obj_from_model(pearl):
#     fullcardmodel = FullCardModel.model_construct(**pearl)
#     fullcardobj = FullCard(**fullcardmodel.model_dump())
#     pprint(fullcardobj.__dict__)
#     pprint(f"PRICES: {fullcardobj.prices.__dict__}")
#     pprint(f"IMAGEURIS: {fullcardobj.image_uris.__dict__}")
#     pprint(f"RELEASED_AT: {fullcardobj.released_at}")
#     assert False
