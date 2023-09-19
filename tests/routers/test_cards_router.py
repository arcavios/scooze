from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from mongomock import Collection
from scooze.models.card import CardModelOut

# region Fixtures


@pytest.fixture
def omnath(mock_cards_collection: Collection) -> CardModelOut:
    db_omnath = mock_cards_collection.find_one({"name": "Omnath, Locus of Creation"})
    return CardModelOut(**db_omnath)


@pytest.fixture
def chalice(mock_cards_collection: Collection) -> CardModelOut:
    db_chalice = mock_cards_collection.find_one({"name": "Chalice of the Void"})
    return CardModelOut(**db_chalice)


@pytest.fixture
def boseiju(mock_cards_collection: Collection) -> CardModelOut:
    db_boseiju = mock_cards_collection.find_one({"name": "Boseiju, Who Endures"})
    return CardModelOut(**db_boseiju)


# endregion


@pytest.mark.router_cards
@patch("scooze.database.card.get_cards_random")
def test_cards_root(
    mock_get: MagicMock, client: TestClient, omnath: CardModelOut, chalice: CardModelOut, boseiju: CardModelOut
):
    random_cards = [omnath, chalice, boseiju]  # "random"
    mock_get.return_value: list[CardModelOut] = random_cards
    response = client.get("/cards/")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 3
    for card in random_cards:
        assert card.model_dump(mode="json") in response_json


@pytest.mark.router_cards
@patch("scooze.database.card.get_cards_random")
def test_cards_root(mock_get: MagicMock, client: TestClient):
    mock_get.return_value = None
    response = client.get("/cards/")
    assert response.status_code == 404
    assert response.json()["message"] == "No cards found in the database."


# region Create


@pytest.mark.router_cards
@patch("scooze.database.card.add_cards")
def test_add_cards(
    mock_add: MagicMock, client: TestClient, omnath: CardModelOut, chalice: CardModelOut, boseiju: CardModelOut
):
    cards_to_add = [omnath, chalice, boseiju]
    mock_add.return_value: list[str] = [str(card.id) for card in cards_to_add]
    response = client.post("/cards/add", json=[card.model_dump(mode="json", by_alias=True) for card in cards_to_add])
    assert response.status_code == 200
    assert response.json()["message"] == f"Created {len(cards_to_add)} cards."


@pytest.mark.router_cards
@patch("scooze.database.card.add_cards")
def test_add_cards_bad(mock_add: MagicMock, client: TestClient):
    mock_add.return_value = None
    response = client.post("/cards/add", json=[])
    assert response.status_code == 400
    assert response.json()["message"] == "Failed to create any new cards."


# endregion

# region Read


@pytest.mark.router_cards
@patch("scooze.database.card.get_cards_by_property")
def test_get_cards_by_cmc(mock_get: MagicMock, client: TestClient, chalice: CardModelOut, boseiju: CardModelOut):
    zero_drops = [chalice, boseiju]
    mock_get.return_value: list[CardModelOut] = zero_drops
    response = client.post("/cards/by?property_name=cmc", json=[0.0])
    assert response.status_code == 200
    response_json = response.json()
    for card in zero_drops:
        assert card.model_dump(mode="json") in response_json


@pytest.mark.router_cards
@patch("scooze.database.card.get_cards_by_property")
def test_get_carsd_by_cmc_none_found(mock_get: MagicMock, client: TestClient):
    mock_get.return_value = None
    response = client.post("/cards/by?property_name=cmc", json=[100.0])
    assert response.status_code == 404
    assert response.json()["message"] == "Cards not found."


# endregion


# region Delete


@pytest.mark.router_cards
@patch("scooze.database.card.delete_cards_all")
def test_delete_cards(mock_update: MagicMock, client: TestClient, omnath: CardModelOut, chalice: CardModelOut):
    # Acting as though the db is set up with just Omnath and Chalice for purposes of this test
    mock_update.return_value = 2
    response = client.delete("/cards/delete/all")
    assert response.status_code == 200
    assert response.json()["message"] == "Deleted 2 cards."


@pytest.mark.router_cards
@patch("scooze.database.card.delete_cards_all")
def test_delete_all_cards(mock_update: MagicMock, client: TestClient):
    mock_update.return_value = None
    response = client.delete("/cards/delete/all")
    assert response.status_code == 404
    assert response.json()["message"] == "No cards deleted."


# endregion
