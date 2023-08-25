import json

import pytest
from scooze.card import Card, FullCard, OracleCard
from scooze.enums import Color, Format, Legality
from scooze.models.card import CardModel, FullCardModel

# TODO(#65): WRITE TESTS FOR CARD OBJECT HERE

# TODO: remove NOTE s and TODO s from this file.
# Write tests for Card conversion. Write tests for normal Card behavior
# Write tests for CardModel conversion. Write tests for normal CardModel behavior

# NOTE: these tests can be run with pytest -s so you can see the print statements
# NOTE: helpful little jq that can get you a card from one of the bulk files. You can get scryfall_id from
# image address on scryfall.com
# ╰─❯ cat data/bulk/oracle_cards.json | jq '.[] | select(.id == "371ceb58-f498-4616-a7f0-eb118fe2e4ff")' > ./data/bulk/card.json

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




@pytest.fixture
def cards_json() -> list[str]:
    with open("./data/test/test_cards.jsonl", "r") as json_file:
        json_list = list(json_file)

    return json_list


# NOTE: helper to get particular card_json
def get_card_json(cards_json: list[str], id: str) -> dict:
    for json_str in cards_json:
        card_json = json.loads(json_str)
        if card_json["id"] == id:
            return card_json


# region Card JSON


@pytest.fixture
def json_ancestral_recall(cards_json) -> dict:
    return get_card_json(cards_json, "2398892d-28e9-4009-81ec-0d544af79d2b")


@pytest.fixture
def json_mystic_snake(cards_json) -> dict:
    return get_card_json(cards_json, "2d4bacd1-b602-4bcc-9aea-1229949a7d20")


@pytest.fixture
def json_ancestral_visions(cards_json) -> dict:
    return get_card_json(cards_json, "9079c93e-3da8-442a-89d2-609a3eac83b0")


# Digital
@pytest.fixture
def json_urzas_construction_drone(cards_json) -> dict:
    return get_card_json(cards_json, "bfa6bfa2-0aee-4623-a17e-a77898deb16d")


# Transform (Saga)
@pytest.fixture
def json_tales_of_master_seshiro(cards_json) -> dict:
    return get_card_json(cards_json, "512bc867-3a86-4da2-93f0-dd76d6a6f30d")


# Transform (Planeswalker)
@pytest.fixture
def json_arlinn_the_packs_hope(cards_json) -> dict:
    return get_card_json(cards_json, "50d4b0df-a1d8-494f-a019-70ce34161320")


# Split (Aftermath)
@pytest.fixture
def json_driven_despair(cards_json) -> dict:
    return get_card_json(cards_json, "7713ba59-dd4c-4b49-93a7-292728df86b8")


# MDFC
@pytest.fixture
def json_turntimber_symbiosis(cards_json) -> dict:
    return get_card_json(cards_json, "61bd69ea-1e9e-46b0-b1a1-ed7fdbe3deb6")


# Flip
@pytest.fixture
def json_orochi_eggwatcher(cards_json) -> dict:
    return get_card_json(cards_json, "a4f4aa3b-c64a-4430-b1a2-a7fca87d0a22")


# endregion

# region json -> Card Object


def test_card_from_json_instant(json_ancestral_recall):
    card = Card.from_json(json_ancestral_recall)
    assert card.cmc == 1.0
    assert card.color_identity == {Color.BLUE}
    assert card.colors == {Color.BLUE}
    assert card.legalities == {
        Format.ALCHEMY: Legality.NOT_LEGAL,
        Format.BRAWL: Legality.NOT_LEGAL,
        Format.COMMANDER: Legality.BANNED,
        Format.DUEL: Legality.BANNED,
        Format.EXPLORER: Legality.NOT_LEGAL,
        Format.FUTURE: Legality.NOT_LEGAL,
        Format.GLADIATOR: Legality.NOT_LEGAL,
        Format.HISTORIC: Legality.NOT_LEGAL,
        Format.HISTORICBRAWL: Legality.NOT_LEGAL,
        Format.LEGACY: Legality.BANNED,
        Format.MODERN: Legality.NOT_LEGAL,
        Format.OATHBREAKER: Legality.BANNED,
        Format.OLDSCHOOL: Legality.NOT_LEGAL,
        Format.PAUPER: Legality.NOT_LEGAL,
        Format.PAUPERCOMMANDER: Legality.NOT_LEGAL,
        Format.PENNY: Legality.NOT_LEGAL,
        Format.PIONEER: Legality.NOT_LEGAL,
        Format.PREDH: Legality.BANNED,
        Format.PREMODERN: Legality.NOT_LEGAL,
        Format.STANDARD: Legality.NOT_LEGAL,
        Format.VINTAGE: Legality.RESTRICTED,
    }
    assert card.mana_cost == "{U}"
    assert card.name == "Ancestral Recall"
    assert card.power is None
    assert card.toughness is None
    assert card.type_line == "Instant"


def test_card_from_json_creature(json_mystic_snake):
    card = Card.from_json(json_mystic_snake)
    assert card.color_identity == {Color.GREEN, Color.BLUE}
    assert card.colors == {Color.GREEN, Color.BLUE}
    assert card.power == "2"
    assert card.toughness == "2"
    assert card.type_line == "Creature — Snake"


# def test_full_card_obj_from_json(json_mystic_snake):
#     full_card = FullCard.from_json(json_mystic_snake)
#     print("test_full_card_obj_from_json")
#     pprint(get_members(full_card))
#     assert True


# endregion


# region json -> CardModel


# def test_card_model_from_json(json_mystic_snake):
#     card_model = CardModel.model_validate(json_mystic_snake)
#     print("test_card_model_from_json")
#     pprint(dict(card_model))
#     assert True


# def test_full_card_from_json(json_mystic_snake):
#     full_card_model = FullCardModel.model_validate(json_mystic_snake)
#     print("test_full_card_model_from_json")
#     pprint(dict(full_card_model))
#     assert True


# endregion


# region CardModel -> Card Object


# def test_card_object_from_card_model(json_mystic_snake):
#     card_model = CardModel.model_validate(json_mystic_snake)
#     card = Card.from_model(card_model)
#     print("test_card_object_from_card_model")
#     pprint(get_members(card))
#     assert True


# def test_oracle_card_object_from_full_card_model(json_mystic_snake):
#     full_card_model = FullCardModel.model_validate(json_mystic_snake)
#     full_card = OracleCard.from_model(full_card_model)
#     print("test_oracle_card_object_from_full_card_model")
#     pprint(get_members(full_card))
#     assert True


# def test_full_card_object_from_full_card_model(json_mystic_snake):
#     full_card_model = FullCardModel.model_validate(json_mystic_snake)
#     full_card = FullCard.from_model(full_card_model)
#     print("test_full_card_object_from_full_card_model")
#     pprint(get_members(full_card))
#     assert True


# endregion
