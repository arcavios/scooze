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

# TODO: test get_card

# TODO: test get_cards


@patch("scooze.database.card.add_card")
def test_add_base_card(mock_add: MagicMock, recall_base: Card):
    model = CardModelOut.model_validate(recall_base.__dict__)
    model.id = ObjectId()
    mock_add.return_value: CardModelOut = model
    result = card_api.add_card_to_db(recall_base)
    assert result == model.id


@patch("scooze.database.card.add_card")
def test_add_oracle_card(mock_add: MagicMock, recall_full: OracleCard):
    model = CardModelOut.model_validate(recall_full.__dict__)
    model.id = ObjectId()
    mock_add.return_value: CardModelOut = model
    result = card_api.add_card_to_db(recall_full)
    assert result == model.id


@patch("scooze.database.card.add_card")
def test_add_full_card(mock_add: MagicMock, recall_full: FullCard):
    model = CardModelOut.model_validate(recall_full.__dict__)
    model.id = ObjectId()
    mock_add.return_value: CardModelOut = model
    result = card_api.add_card_to_db(recall_full)
    assert result == model.id


@patch("scooze.database.card.add_card")
def test_add_card_bad(mock_add: MagicMock, recall_base: Card):
    mock_add.return_value = None
    result = card_api.add_card_to_db(recall_base)
    assert result is None


@patch("scooze.database.card.add_cards")
def test_add_base_cards(mock_add: MagicMock, cards_base: list[Card]):
    ids = [ObjectId() for _ in cards_base]
    mock_add.return_value: list[ObjectId] = ids
    results = card_api.add_cards_to_db(cards_base)
    assert results == ids


@patch("scooze.database.card.add_cards")
def test_add_oracle_cards(mock_add: MagicMock, cards_oracle: list[OracleCard]):
    ids = [ObjectId() for _ in cards_oracle]
    mock_add.return_value: list[ObjectId] = ids
    results = card_api.add_cards_to_db(cards_oracle)
    assert results == ids


@patch("scooze.database.card.add_cards")
def test_add_full_cards(mock_add: MagicMock, cards_full: list[FullCard]):
    ids = [ObjectId() for _ in cards_full]
    mock_add.return_value: list[ObjectId] = ids
    results = card_api.add_cards_to_db(cards_full)
    assert results == ids


@patch("scooze.database.card.add_cards")
def test_add_cards_bad(mock_add: MagicMock, cards_base: list[Card]):
    mock_add.return_value = None
    results = card_api.add_cards_to_db(cards_base)
    assert results is None


# TODO: test delete_all_cards
