from unittest.mock import MagicMock, patch

import scooze.api.card as card_api
from bson import ObjectId
from scooze.card import Card, FullCard, OracleCard
from scooze.models.card import CardModelOut


@patch("scooze.database.card.get_card_by_property")
def test_get_base_card(mock_get: MagicMock, recall_base, asyncio_runner):
    model = CardModelOut.model_validate(recall_base.__dict__)
    # model.scooze_id = recall_base.scooze_id
    mock_get.return_value: CardModelOut = model
    result = asyncio_runner.run(card_api.get_card_by(property_name="_id", value=model.scooze_id, card_class=Card))
    # recall_base._scooze_id = model.scooze_id
    assert result == recall_base


@patch("scooze.database.card.get_card_by_property")
def test_get_oracle_card(mock_get: MagicMock, recall_oracle, asyncio_runner):
    model = CardModelOut.model_validate(recall_oracle.__dict__)
    mock_get.return_value: CardModelOut = model
    result = asyncio_runner.run(card_api.get_card_by(property_name="_id", value=model.scooze_id, card_class=OracleCard))
    assert result == recall_oracle


@patch("scooze.database.card.get_card_by_property")
def test_get_full_card(mock_get: MagicMock, recall_full, asyncio_runner):
    model = CardModelOut.model_validate(recall_full.__dict__)
    mock_get.return_value: CardModelOut = model
    result = asyncio_runner.run(card_api.get_card_by(property_name="_id", value=model.scooze_id, card_class=FullCard))
    assert result == recall_full


@patch("scooze.database.card.get_card_by_property")
def test_get_card_bad(mock_get: MagicMock, asyncio_runner):
    mock_get.return_value = None
    result = asyncio_runner.run(card_api.get_card_by(property_name="_id", value=ObjectId(), card_class=Card))
    assert result is None


@patch("scooze.database.card.get_cards_by_property")
def test_get_base_cards(mock_get: MagicMock, cards_base, asyncio_runner):
    models = [CardModelOut.model_validate(card.__dict__) for card in cards_base]
    ids = [model.scooze_id for model in models]
    mock_get.return_value: list[CardModelOut] = models
    results = asyncio_runner.run(card_api.get_cards_by(property_name="_id", values=ids, card_class=Card))
    assert results == cards_base


@patch("scooze.database.card.get_cards_by_property")
def test_get_oracle_cards(mock_get: MagicMock, cards_oracle, asyncio_runner):
    models = [CardModelOut.model_validate(card.__dict__) for card in cards_oracle]
    ids = [model.scooze_id for model in models]
    mock_get.return_value: list[CardModelOut] = models
    results = asyncio_runner.run(card_api.get_cards_by(property_name="_id", values=ids, card_class=OracleCard))
    assert results == cards_oracle


@patch("scooze.database.card.get_cards_by_property")
def test_get_full_cards(mock_get: MagicMock, cards_full, asyncio_runner):
    models = [CardModelOut.model_validate(card.__dict__) for card in cards_full]
    ids = [model.scooze_id for model in models]
    mock_get.return_value: list[CardModelOut] = models
    results = asyncio_runner.run(card_api.get_cards_by(property_name="_id", values=ids, card_class=FullCard))
    assert results == cards_full


@patch("scooze.database.card.get_cards_all")
def test_get_all_cards_base(mock_get: MagicMock, cards_base, asyncio_runner):
    models = [CardModelOut.model_validate(card.__dict__) for card in cards_base]
    mock_get.return_value: list[CardModelOut] = models
    results = asyncio_runner.run(card_api.get_cards_all(card_class=Card))
    assert results == cards_base


@patch("scooze.database.card.get_cards_all")
def test_get_all_cards_oracle(mock_get: MagicMock, cards_oracle, asyncio_runner):
    models = [CardModelOut.model_validate(card.__dict__) for card in cards_oracle]
    mock_get.return_value: list[CardModelOut] = models
    results = asyncio_runner.run(card_api.get_cards_all(card_class=OracleCard))
    assert results == cards_oracle


@patch("scooze.database.card.get_cards_all")
def test_get_all_cards_full(mock_get: MagicMock, cards_full, asyncio_runner):
    models = [CardModelOut.model_validate(card.__dict__) for card in cards_full]
    mock_get.return_value: list[CardModelOut] = models
    results = asyncio_runner.run(card_api.get_cards_all(card_class=FullCard))
    assert results == cards_full


@patch("scooze.database.card.get_cards_by_property")
def test_get_cards_bad(mock_get: MagicMock, cards_base, asyncio_runner):
    mock_get.return_value = []
    results = asyncio_runner.run(
        card_api.get_cards_by(property_name="id", values=[ObjectId() for _ in cards_base], card_class=Card)
    )
    assert results == []


@patch("scooze.database.card.add_card")
def test_add_base_card(mock_add: MagicMock, recall_base, asyncio_runner):
    model = CardModelOut.model_validate(recall_base.__dict__)
    model.scooze_id = ObjectId()
    mock_add.return_value: CardModelOut = model
    result = asyncio_runner.run(card_api.add_card(card=recall_base))
    assert result == model.scooze_id


@patch("scooze.database.card.add_card")
def test_add_oracle_card(mock_add: MagicMock, recall_oracle, asyncio_runner):
    model = CardModelOut.model_validate(recall_oracle.__dict__)
    mock_add.return_value: CardModelOut = model
    result = asyncio_runner.run(card_api.add_card(card=recall_oracle))
    assert result == model.scooze_id


@patch("scooze.database.card.add_card")
def test_add_full_card(mock_add: MagicMock, recall_full, asyncio_runner):
    model = CardModelOut.model_validate(recall_full.__dict__)
    mock_add.return_value: CardModelOut = model
    result = asyncio_runner.run(card_api.add_card(card=recall_full))
    assert result == model.scooze_id


@patch("scooze.database.card.add_card")
def test_add_card_bad(mock_add: MagicMock, recall_base, asyncio_runner):
    mock_add.return_value = None
    result = asyncio_runner.run(card_api.add_card(card=recall_base))
    assert result is None


@patch("scooze.database.card.add_cards")
def test_add_base_cards(mock_add: MagicMock, cards_base, asyncio_runner):
    ids = [ObjectId() for _ in cards_base]
    mock_add.return_value: list[ObjectId] = ids
    results = asyncio_runner.run(card_api.add_cards(cards=cards_base))
    assert results == ids


@patch("scooze.database.card.add_cards")
def test_add_oracle_cards(mock_add: MagicMock, cards_oracle, asyncio_runner):
    ids = [ObjectId() for _ in cards_oracle]
    mock_add.return_value: list[ObjectId] = ids
    results = asyncio_runner.run(card_api.add_cards(cards=cards_oracle))
    assert results == ids


@patch("scooze.database.card.add_cards")
def test_add_full_cards(mock_add: MagicMock, cards_full, asyncio_runner):
    ids = [ObjectId() for _ in cards_full]
    mock_add.return_value: list[ObjectId] = ids
    results = asyncio_runner.run(card_api.add_cards(cards=cards_full))
    assert results == ids


@patch("scooze.database.card.add_cards")
def test_add_cards_bad(mock_add: MagicMock, cards_base, asyncio_runner):
    mock_add.return_value = []
    results = asyncio_runner.run(card_api.add_cards(cards=cards_base))
    assert results == []


@patch("scooze.database.card.delete_cards_all")
def test_delete_cards(mock_delete: MagicMock, asyncio_runner):
    mock_delete.return_value: int = 4
    results = asyncio_runner.run(card_api.delete_cards_all())
    assert results == 4


@patch("scooze.database.card.delete_cards_all")
def test_delete_cards_bad(mock_delete: MagicMock, asyncio_runner):
    mock_delete.return_value = None
    results = asyncio_runner.run(card_api.delete_cards_all())
    assert results is None
