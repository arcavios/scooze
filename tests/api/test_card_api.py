import asyncio
from unittest.mock import MagicMock, patch

import pytest
import scooze.api.card as card_api
from bson import ObjectId
from scooze.card import Card, FullCard, OracleCard
from scooze.models.card import CardModelOut


# region Card fixtures
@pytest.fixture(scope="module")
def recall_base(json_ancestral_recall) -> Card:
    return Card.from_json(json_ancestral_recall)


@pytest.fixture(scope="module")
def recall_oracle(json_ancestral_recall) -> OracleCard:
    return OracleCard.from_json(json_ancestral_recall)


@pytest.fixture(scope="module")
def recall_full(json_ancestral_recall) -> FullCard:
    return FullCard.from_json(json_ancestral_recall)


@pytest.fixture(scope="module")
def mystic_snake_base(json_mystic_snake) -> Card:
    return Card.from_json(json_mystic_snake)


@pytest.fixture(scope="module")
def mystic_snake_oracle(json_mystic_snake) -> OracleCard:
    return OracleCard.from_json(json_mystic_snake)


@pytest.fixture(scope="module")
def mystic_snake_full(json_mystic_snake) -> FullCard:
    return FullCard.from_json(json_mystic_snake)


@pytest.fixture(scope="module")
def cards_base(recall_base, mystic_snake_base) -> list[Card]:
    return [recall_base, mystic_snake_base]


@pytest.fixture(scope="module")
def cards_oracle(recall_oracle, mystic_snake_oracle) -> list[OracleCard]:
    return [recall_oracle, mystic_snake_oracle]


@pytest.fixture(scope="module")
def cards_full(recall_full, mystic_snake_full) -> list[FullCard]:
    return [recall_full, mystic_snake_full]


# endregion


@patch("scooze.database.card.add_card")
def test_add_base_card(mock_add: MagicMock, recall_base: Card):
    model = CardModelOut.model_validate(recall_base.__dict__)
    model.id = ObjectId()
    mock_add.return_value: CardModelOut = model
    result = card_api.add_card_to_db(recall_base)
    assert result == model.id

@patch("scooze.database.card.add_card")
def test_add_oracle_card(mock_add: MagicMock, recall_oracle: Card):
    model = CardModelOut.model_validate(recall_oracle.__dict__)
    model.id = ObjectId()
    mock_add.return_value: CardModelOut = model
    result = card_api.add_card_to_db(recall_oracle)
    assert result == model.id


# def test_add_oracle_card(recall_oracle):
#     from scooze.database.mongo import mongo_close, mongo_connect

#     asyncio.run(mongo_connect())
#     result = card_api.add_card_to_db(recall_oracle)
#     from pprint import pprint

#     pprint(result)
#     assert result
#     asyncio.run(mongo_close())


# def test_add_full_card(recall_full):
#     from scooze.database.mongo import mongo_close, mongo_connect

#     asyncio.run(mongo_connect())
#     result = card_api.add_card_to_db(recall_full)
#     from pprint import pprint

#     pprint(result)
#     assert result
#     asyncio.run(mongo_close())


# def test_add_base_cards(cards_base):
#     from scooze.database.mongo import mongo_close, mongo_connect

#     asyncio.run(mongo_connect())
#     result = card_api.add_cards_to_db(cards_base)
#     from pprint import pprint

#     pprint(result)
#     assert result
#     asyncio.run(mongo_close())


# def test_add_oracle_cards(cards_oracle):
#     from scooze.database.mongo import mongo_close, mongo_connect

#     asyncio.run(mongo_connect())
#     result = card_api.add_cards_to_db(cards_oracle)
#     from pprint import pprint

#     pprint(result)
#     assert result
#     asyncio.run(mongo_close())


# def test_add_full_cards(cards_full):
#     from scooze.database.mongo import mongo_close, mongo_connect

#     asyncio.run(mongo_connect())
#     result = card_api.add_cards_to_db(cards_full)
#     from pprint import pprint

#     pprint(result)
#     assert result
#     asyncio.run(mongo_close())


# def test_add_mixed_cards(cards_base, cards_oracle, cards_full):
#     cards_base.extend(cards_oracle + cards_full)
#     from scooze.database.mongo import mongo_close, mongo_connect

#     asyncio.run(mongo_connect())
#     result = card_api.add_cards_to_db(cards_base)
#     from pprint import pprint

#     pprint(result)
#     assert result
#     asyncio.run(mongo_close())
