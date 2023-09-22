from unittest.mock import MagicMock, patch

import pytest
import scooze.api.card as card_api
from bson import ObjectId
from scooze.card import Card, FullCard, OracleCard
from scooze.models.card import CardModelOut


@patch("scooze.database.card.get_card_by_property")
def test_get_base_card(mock_get: MagicMock, recall_base: Card):
    mock_get.return_value: CardModelOut = CardModelOut.model_validate(recall_base.__dict__)
    result = card_api.get_card_by("id", ObjectId(), card_class=Card)
    assert result == recall_base


@patch("scooze.database.card.get_card_by_property")
def test_get_oracle_card(mock_get: MagicMock, recall_oracle: OracleCard):
    mock_get.return_value: CardModelOut = CardModelOut.model_validate(recall_oracle.__dict__)
    result = card_api.get_card_by("id", ObjectId(), card_class=OracleCard)
    assert result == recall_oracle


@patch("scooze.database.card.get_card_by_property")
def test_get_full_card(mock_get: MagicMock, recall_full: FullCard):
    mock_get.return_value: CardModelOut = CardModelOut.model_validate(recall_full.__dict__)
    result = card_api.get_card_by("id", ObjectId(), card_class=FullCard)
    assert result == recall_full


@patch("scooze.database.card.get_card_by_property")
def test_get_card_bad(mock_get: MagicMock):
    mock_get.return_value = None
    result = card_api.get_card_by("id", ObjectId(), card_class=Card)
    assert result is None


@patch("scooze.database.card.get_cards_by_property")
def test_get_base_cards(mock_get: MagicMock, cards_base: list[Card]):
    mock_get.return_value: list[CardModelOut] = [CardModelOut.model_validate(card.__dict__) for card in cards_base]
    results = card_api.get_cards_by("id", [ObjectId() for _ in cards_base], card_class=Card)
    assert results == cards_base


@patch("scooze.database.card.get_cards_by_property")
def test_get_oracle_cards(mock_get: MagicMock, cards_oracle: list[OracleCard]):
    mock_get.return_value: list[CardModelOut] = [CardModelOut.model_validate(card.__dict__) for card in cards_oracle]
    results = card_api.get_cards_by("id", [ObjectId() for _ in cards_oracle], card_class=OracleCard)
    assert results == cards_oracle


@patch("scooze.database.card.get_cards_by_property")
def test_get_full_cards(mock_get: MagicMock, cards_full: list[FullCard]):
    mock_get.return_value: list[CardModelOut] = [CardModelOut.model_validate(card.__dict__) for card in cards_full]
    results = card_api.get_cards_by("id", [ObjectId() for _ in cards_full], card_class=FullCard)
    assert results == cards_full


@patch("scooze.database.card.get_cards_by_property")
def test_get_cards_bad(mock_get: MagicMock, cards_base: list[Card]):
    mock_get.return_value = None
    results = card_api.get_cards_by("id", [ObjectId() for _ in cards_base], card_class=Card)
    assert results is None


@patch("scooze.database.card.add_card")
def test_add_base_card(mock_add: MagicMock, recall_base: Card):
    model = CardModelOut.model_validate(recall_base.__dict__)
    model.id = ObjectId()
    mock_add.return_value: CardModelOut = model
    result = card_api.add_card(recall_base)
    assert result == model.id


@patch("scooze.database.card.add_card")
def test_add_oracle_card(mock_add: MagicMock, recall_full: OracleCard):
    model = CardModelOut.model_validate(recall_full.__dict__)
    model.id = ObjectId()
    mock_add.return_value: CardModelOut = model
    result = card_api.add_card(recall_full)
    assert result == model.id


@patch("scooze.database.card.add_card")
def test_add_full_card(mock_add: MagicMock, recall_full: FullCard):
    model = CardModelOut.model_validate(recall_full.__dict__)
    model.id = ObjectId()
    mock_add.return_value: CardModelOut = model
    result = card_api.add_card(recall_full)
    assert result == model.id


@patch("scooze.database.card.add_card")
def test_add_card_bad(mock_add: MagicMock, recall_base: Card):
    mock_add.return_value = None
    result = card_api.add_card(recall_base)
    assert result is None


@patch("scooze.database.card.add_cards")
def test_add_base_cards(mock_add: MagicMock, cards_base: list[Card]):
    ids = [ObjectId() for _ in cards_base]
    mock_add.return_value: list[ObjectId] = ids
    results = card_api.add_cards(cards_base)
    assert results == ids


@patch("scooze.database.card.add_cards")
def test_add_oracle_cards(mock_add: MagicMock, cards_oracle: list[OracleCard]):
    ids = [ObjectId() for _ in cards_oracle]
    mock_add.return_value: list[ObjectId] = ids
    results = card_api.add_cards(cards_oracle)
    assert results == ids


@patch("scooze.database.card.add_cards")
def test_add_full_cards(mock_add: MagicMock, cards_full: list[FullCard]):
    ids = [ObjectId() for _ in cards_full]
    mock_add.return_value: list[ObjectId] = ids
    results = card_api.add_cards(cards_full)
    assert results == ids


@patch("scooze.database.card.add_cards")
def test_add_cards_bad(mock_add: MagicMock, cards_base: list[Card]):
    mock_add.return_value = None
    results = card_api.add_cards(cards_base)
    assert results is None


@patch("scooze.database.card.delete_cards_all")
def test_delete_cards(mock_delete: MagicMock):
    mock_delete.return_value: int = 4
    results = card_api.delete_cards_all()
    assert results == 4


@patch("scooze.database.card.delete_cards_all")
def test_delete_cards_bad(mock_delete: MagicMock):
    mock_delete.return_value = None
    results = card_api.delete_cards_all()
    assert results is None
