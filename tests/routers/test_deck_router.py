from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from mongomock import Collection, Database
from scooze.models.deck import DeckModelIn, DeckModelOut

# region Fixtures


# endregion


@pytest.mark.router_deck
@patch("scooze.database.deck.get_decks_random")
def test_deck_root(
    mock_get_random: MagicMock, client: TestClient, mock_decks_collection: Collection, deck_model_modern_4c: DeckModelIn
):
    mock_get_random.return_value = [DeckModelOut(**mock_decks_collection.find_one({"archetype": "Four-color Control"}))]
    response = client.get("/deck/")
    assert response.status_code == 200
    response_json = response.json()
    for k, v in deck_model_modern_4c.model_dump(mode="json").items():
        assert response_json[k] == v


# region Create


@pytest.mark.router_deck
@patch("scooze.database.deck.add_deck")
def test_add_deck(mock_add: MagicMock, client: TestClient, deck_model_modern_4c: DeckModelIn):
    deck_json = deck_model_modern_4c.model_dump(mode="json", by_alias=True)
    mock_add.return_value: DeckModelOut = DeckModelOut(**deck_json)
    response = client.post("/deck/add", json={"deck": deck_json})
    assert response.status_code == 200
    response_json = response.json()
    for k, v in deck_model_modern_4c.model_dump(mode="json").items():
        assert response_json[k] == v


@pytest.mark.router_deck
@patch("scooze.database.deck.add_deck")
def test_add_deck_bad(mock_add: MagicMock, client: TestClient, deck_model_modern_4c: DeckModelIn):
    deck_json = deck_model_modern_4c.model_dump(mode="json", by_alias=True)
    mock_add.return_value = None
    response = client.post("/deck/add", json={"deck": deck_json})
    assert response.status_code == 400
    assert response.json()["message"] == "Failed to create a new deck."


# endregion

# TODO(#111): Complete testing for Deck router
