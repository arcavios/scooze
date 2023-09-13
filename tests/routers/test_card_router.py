from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from scooze.models.card import CardModelIn, CardModelOut

# region Fixtures


@pytest.fixture
def request_body_card() -> CardModelIn:
    return CardModelIn.model_validate(
        {
            "id": "487116ab-b885-406b-aa54-56cb67eb3ca5", # Scryfall ID
            "name": "Scavenging Ooze",
            "colors": ["G"],
            "cmc": 2.0,
            "power": "2",
            "toughness": "2",
            "typeLine": "Creature — Ooze",
        }
    )


# endregion


@pytest.mark.router_card
@patch("scooze.database.card.add_card")
def test_add_card(mock_add: MagicMock, client: TestClient, request_body_card: CardModelIn):
    card_json = request_body_card.model_dump(mode="json", by_alias=True)
    mock_add.return_value: CardModelOut = CardModelOut(**card_json)
    response = client.post("/card/add", json={"card": card_json})
    assert response.status_code == 200
    response_json = response.json()
    for k, v in request_body_card.model_dump(mode="json").items():
        assert response_json[k] == v


@pytest.mark.router_card
@patch("scooze.database.card.add_card")
def test_add_card_bad(mock_add: MagicMock, client: TestClient, request_body_card: CardModelIn):
    card_json = request_body_card.model_dump(mode="json", by_alias=True)
    mock_add.return_value = None
    response = client.post("/card/add", json={"card": card_json})
    assert response.status_code == 400
    assert response.json()["message"] == "Failed to create a new card."


# TODO(#13): Complete testing for Card router
