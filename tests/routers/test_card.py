from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from scooze.main import app
from scooze.models.card import Card, CardIn, CardOut

# region Fixtures


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def request_body_card() -> CardIn:
    return CardIn.model_validate(
        {
            "oracleId": "1",
            "name": "Snapcaster Mage",
            "colors": ["U"],
            "cmc": "2.0",
        }
    )


# endregion


@pytest.mark.router_card
@patch("scooze.database.add_card")
def test_add_card(mock_add: MagicMock, client: TestClient, request_body_card: CardIn):
    card_json = request_body_card.model_dump(mode="json", by_alias=True)
    mock_add.return_value: CardOut = CardOut(**card_json)
    response = client.post("/card/add", json={"card": card_json})
    assert response.status_code == 200
    response_json = response.json()
    for k, v in request_body_card.model_dump(mode="json").items():
        assert response_json[k] == v


@pytest.mark.router_card
@patch("scooze.database.add_card")
def test_add_card_bad(mock_add: MagicMock, client: TestClient, request_body_card: CardIn):
    card_json = request_body_card.model_dump(mode="json", by_alias=True)
    mock_add.return_value = None
    response = client.post("/card/add", json={"card": card_json})
    assert response.status_code == 400
    assert response.json()["message"] == "Failed to create a new card."
