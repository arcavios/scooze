from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from mongomock import Collection
from scooze.models.card import CardModelIn, CardModelOut

# region Fixtures


@pytest.fixture
def request_body_card() -> CardModelIn:
    return CardModelIn.model_validate(
        {
            "id": "487116ab-b885-406b-aa54-56cb67eb3ca5",  # Scryfall ID
            "name": "Scavenging Ooze",
            "colors": ["G"],
            "cmc": 2.0,
            "power": "2",
            "toughness": "2",
            "typeLine": "Creature — Ooze",
        }
    )


@pytest.fixture
def omnath(mock_cards_collection: Collection) -> CardModelOut:
    db_omnath = mock_cards_collection.find_one({"name": "Omnath, Locus of Creation"})
    return CardModelOut(**db_omnath)


# endregion


# region Create


@pytest.mark.router_card
@patch("scooze.database.card.add_card")
def test_add_card(mock_add: MagicMock, client: TestClient, omnath: CardModelOut):
    mock_add.return_value: CardModelOut = omnath
    response = client.post("/card/add", json={"card": omnath.model_dump(mode="json", by_alias=True)})
    assert response.status_code == 200
    response_json = response.json()
    for k, v in omnath.model_dump(mode="json").items():
        assert response_json[k] == v


@pytest.mark.router_card
@patch("scooze.database.card.add_card")
def test_add_card_bad(mock_add: MagicMock, client: TestClient, omnath: CardModelOut):
    mock_add.return_value = None
    response = client.post("/card/add", json={"card": omnath.model_dump(mode="json", by_alias=True)})
    assert response.status_code == 400
    assert response.json()["message"] == "Failed to create a new card."


# endregion

# region Read


@pytest.mark.router_card
@patch("scooze.database.card.get_card_by_property")
def test_get_card_by_id(mock_get: MagicMock, client: TestClient, omnath: CardModelOut):
    mock_get.return_value: CardModelOut = omnath
    response = client.get(f"/card/id/{str(omnath.id)}")
    assert response.status_code == 200
    response_json = response.json()
    for k, v in omnath.model_dump(mode="json").items():
        assert response_json[k] == v


@pytest.mark.router_card
@patch("scooze.database.card.get_card_by_property")
def test_get_card_by_id_bad_id(mock_get: MagicMock, client: TestClient):
    mock_get.return_value = None
    response = client.get("/card/id/blarghl")
    assert response.status_code == 404
    assert response.json()["message"] == "Card with id blarghl not found."


@pytest.mark.router_card
@patch("scooze.database.card.get_card_by_property")
def test_get_card_by_name(mock_get: MagicMock, client: TestClient, omnath: CardModelOut):
    mock_get.return_value: CardModelOut = omnath
    response = client.get(f"/card/name/{omnath.name}")
    assert response.status_code == 200
    response_json = response.json()
    for k, v in omnath.model_dump(mode="json").items():
        assert response_json[k] == v


@pytest.mark.router_card
@patch("scooze.database.card.get_card_by_property")
def test_get_card_by_name_bad_name(mock_get: MagicMock, client: TestClient):
    mock_get.return_value = None
    response = client.get("/card/name/blarghl")
    assert response.status_code == 404
    assert response.json()["message"] == "Card with name blarghl not found."


# endregion

# region Update


@pytest.mark.router_card
@patch("scooze.database.card.update_card")
def test_update_card(mock_update: MagicMock, client: TestClient, omnath: CardModelOut):
    omnath_dump = omnath.model_dump(mode="json", by_alias=True)
    update_data = {"cmc": 5.0}
    omnath_dump.update(update_data)
    new_omnath = CardModelOut(**omnath_dump)
    mock_update.return_value: CardModelOut = new_omnath
    response = client.patch(f"/card/update/{omnath.id}", json={"card": update_data})
    assert response.status_code == 200
    response_json = response.json()
    for k, v in new_omnath.model_dump(mode="json").items():
        assert response_json[k] == v


@pytest.mark.router_card
@patch("scooze.database.card.update_card")
def test_update_card_bad_id(mock_update: MagicMock, client: TestClient):
    mock_update.return_value = None
    response = client.patch("/card/update/blarghl", json={"card": {}})
    assert response.status_code == 404
    assert response.json()["message"] == "Card with id blarghl not found."


# endregion
