import json
from pprint import pprint

import pytest
from scooze.card import Card, FullCard, OracleCard
from scooze.models.card import FullCardModel, CardModel
import inspect

@pytest.fixture
def temp_fixture() -> str:
    return "some stuff"


def test_temp(temp_fixture):
    assert temp_fixture == "some stuff"


# TODO(#65): WRITE TESTS FOR CARD OBJECT HERE

# TODO: remove NOTE s and TODO s from this file.
# Write tests for Card conversion. Write tests for normal Card behavior
# Write tests for CardModel conversion. Write tests for normal CardModel behavior

# NOTE: these tests can be run with pytest -s so you can see the print statements

# STUFF TO WORK THROUGH:
# 1. it seems like methods with underscores in the name aren't able to go from json -> Model -> Card object. Investigate.
# 2. we need to write code to get from Card -> json -> Card Model. This might be as easy as model_validate(**card.__dict__)
# 3. The tests need to actually check the values to see if they're what we expect. Use a few different cards to really touch on every field you can
# 4. The same tests should be done for Card and CardModel
# 5. Rename the card classes. This shit sucks.
#       Card and CardModel should be the ones you use the most and should just be called as such, idk.
#       The simpler ones should have the more annoying names imo
# 6. Fix the cards in the conftest and test_deckpart and test_deck to use regular Card instead of OracleCard (I think?)
# 7. Do we want to have CardFaces on the regular cards? probably not? idk
# 8. Figure out if Card.from_model() should use model_dump() or dict(). Investigate the key differences.


import json


@pytest.fixture
def fullcards_json() -> list[str]:
    with open("./data/test/test_cards.jsonl", "r") as json_file:
        json_list = list(json_file)

    return json_list


@pytest.fixture
def fable_json(fullcards_json) -> dict:
    for json_str in fullcards_json:
        card_json = json.loads(json_str)
        if card_json["id"] == "24c0d87b-0049-4beb-b9cb-6f813b7aa7dc":
            return card_json

@pytest.fixture
def recall_json(fullcards_json) -> dict:
    for json_str in fullcards_json:
        card_json = json.loads(json_str)
        if card_json["id"] == "70e7ddf2-5604-41e7-bb9d-ddd03d3e9d0b":
            return card_json


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


# def test_pearl(pearl):
#     pprint(pearl.__dict__)
#     assert False


# def test_fable(fable):
#     pprint(fable.__dict__)
#     assert False

# NOTE: helper to filter dunders out of getmembers
def get_members(obj):
    return list(filter(lambda t: not t[0].endswith("__"), inspect.getmembers(obj)))

# NOTE: json -> Card Object

def test_card_obj_from_json(recall_json):
    card = Card.from_json(recall_json)
    print("test_card_obj_from_json")
    pprint(get_members(card))
    assert True

def test_oracle_card_obj_from_json(recall_json):
    oracle_card = OracleCard.from_json(recall_json)
    print("test_oracle_card_obj_from_json")
    pprint(get_members(oracle_card))
    assert True

def test_full_card_obj_from_json(recall_json):
    full_card = FullCard.from_json(recall_json)
    print("test_full_card_obj_from_json")
    pprint(get_members(full_card))
    assert True

#########

# NOTE: json -> CardModel

def test_card_model_from_json(recall_json):
    card_model = CardModel.model_validate(recall_json)
    print("test_card_model_from_json")
    pprint(dict(card_model))
    assert True

def test_full_card_from_json(recall_json):
    full_card_model = FullCardModel.model_validate(recall_json)
    print("test_full_card_model_from_json")
    pprint(dict(full_card_model))
    assert True

#########

# NOTE CardModel -> Card Object

def test_card_object_from_card_model(recall_json):
    card_model = CardModel.model_validate(recall_json)
    card = Card.from_model(card_model)
    print("test_card_object_from_card_model")
    pprint(get_members(card))
    assert True

def test_oracle_card_object_from_full_card_model(recall_json):
    full_card_model = FullCardModel.model_validate(recall_json)
    full_card = OracleCard.from_model(full_card_model)
    print("test_oracle_card_object_from_full_card_model")
    pprint(get_members(full_card))
    assert True

def test_full_card_object_from_full_card_model(recall_json):
    full_card_model = FullCardModel.model_validate(recall_json)
    full_card = FullCard.from_model(full_card_model)
    print("test_full_card_object_from_full_card_model")
    pprint(get_members(full_card))
    assert True

# def test_model_from_obj(pearl):
#     fullcardobj = FullCard(**pearl)
#     fullcardmodel = FullCardModel.model_construct(**fullcardobj.__dict__)
#     pprint(fullcardmodel)
#     pprint(fullcardmodel.scryfall_id)
#     assert False


# def test_obj_from_model(fable, fable_json):
    # pprint(fable_json)
    # fullcardmodel = FullCardModel.model_validate(fable_json)
    # pprint(fullcardmodel)
    # pprint(dict(fullcardmodel))
    # fullcardobj = FullCard.from_model(fullcardmodel)
    # pprint(fullcardobj.__dict__)
    # print("ALL PARTS:")
    # for part in fullcardobj.all_parts:
    #     pprint(part.__dict__)
    # print("CARD FACES:")
    # for face in fullcardobj.card_faces:
    #     pprint(face.__dict__)
    # print("CMC")
    # pprint(fullcardobj.cmc)
    # print("PREVIEW")
    # pprint(fullcardobj.preview.__dict__)
    # print("PRICES")
    # pprint(fullcardobj.prices.__dict__)
    # print("RELEASED AT")
    # pprint(fullcardobj.released_at)
    # assert False
