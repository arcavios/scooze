from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from scooze.main import app
from scooze.models.deck import DeckModelIn, DeckModelOut

# region Fixtures


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def request_body_deck(archetype_modern_4c, main_modern_4c_dict, side_modern_4c_dict) -> DeckModelIn:
    return DeckModelIn.model_validate(
        {
            "archetype": archetype_modern_4c,
            "format": "modern",
            "date_played": datetime.now().date(),
            "main": main_modern_4c_dict,
            "side": side_modern_4c_dict,
        }
    )


# endregion


@pytest.mark.router_deck
@patch("scooze.database.deck.add_deck")
def test_add_deck(mock_add: MagicMock, client: TestClient, request_body_deck: DeckModelIn):
    deck_json = request_body_deck.model_dump(mode="json", by_alias=True)
    mock_add.return_value: DeckModelOut = DeckModelOut(**deck_json)
    response = client.post("/deck/add", json={"deck": deck_json})
    assert response.status_code == 200
    response_json = response.json()
    for k, v in request_body_deck.model_dump(mode="json").items():
        assert response_json[k] == v


@pytest.mark.router_deck
@patch("scooze.database.deck.add_deck")
def test_add_deck_bad(mock_add: MagicMock, client: TestClient, request_body_deck: DeckModelIn):
    deck_json = request_body_deck.model_dump(mode="json", by_alias=True)
    mock_add.return_value = None
    response = client.post("/deck/add", json={"deck": deck_json})
    assert response.status_code == 400
    assert response.json()["message"] == "Failed to create a new deck."


# TODO(#111): Complete testing for Deck router
