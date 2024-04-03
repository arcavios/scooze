from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from mongomock import Collection
from scooze.catalogs import Format
from scooze.models.deck import DeckModelOut

# region Fixtures


@pytest.fixture
def modern_4c(mock_decks_collection: Collection) -> DeckModelOut:
    db_4c = mock_decks_collection.find_one({"archetype": "Four-color Control"})
    return DeckModelOut.model_validate(db_4c)


# endregion


@pytest.mark.router_decks
@patch("scooze.database.deck.get_decks_random")
def test_decks_root(mock_get: MagicMock, client: TestClient, modern_4c: DeckModelOut):
    # random_cards = [omnath, chalice, boseiju]  # "random"
    random_decks = [modern_4c]  # "random"
    mock_get.return_value: list[DeckModelOut] = random_decks
    response = client.get("/decks/")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == len(random_decks)
    for deck in random_decks:
        assert deck.model_dump(mode="json") in response_json


@pytest.mark.router_decks
@patch("scooze.database.deck.get_decks_random")
def test_decks_root_no_decks(mock_get: MagicMock, client: TestClient):
    mock_get.return_value = None
    response = client.get("/decks/")
    assert response.status_code == 404
    assert response.json()["message"] == "No decks found in the database."


# region Create


@pytest.mark.router_decks
@patch("scooze.database.deck.add_decks")
def test_add_decks(mock_add: MagicMock, client: TestClient, modern_4c: DeckModelOut):
    decks_to_add = [modern_4c]
    mock_add.return_value: list[str] = [str(deck.id) for deck in decks_to_add]
    response = client.post("/decks/add", json=[deck.model_dump(mode="json", by_alias=True) for deck in decks_to_add])
    assert response.status_code == 200
    assert response.json()["message"] == f"Created {len(decks_to_add)} deck(s)."


@pytest.mark.router_decks
@patch("scooze.database.deck.add_decks")
def test_add_decks_bad(mock_add: MagicMock, client: TestClient):
    mock_add.return_value = None
    response = client.post("/decks/add", json=[])
    assert response.status_code == 400
    assert response.json()["message"] == "Failed to create any new decks."


# endregion

# region Read


@pytest.mark.router_decks
@patch("scooze.database.deck.get_decks_by_property")
def test_get_decks_by_format(mock_get: MagicMock, client: TestClient, modern_4c: DeckModelOut):
    modern_decks = [modern_4c]
    mock_get.return_value: list[DeckModelOut] = modern_decks
    response = client.post("/decks/by?property_name=format", json=[Format.MODERN])
    assert response.status_code == 200
    response_json = response.json()
    for card in modern_decks:
        assert card.model_dump(mode="json") in response_json


@pytest.mark.router_decks
@patch("scooze.database.deck.get_decks_by_property")
def test_get_decks_by_format_none_found(mock_get: MagicMock, client: TestClient):
    mock_get.return_value = None
    response = client.post("/decks/by?property_name=format", json=[Format.STANDARD])
    assert response.status_code == 404
    assert response.json()["message"] == "Decks not found."


# endregion


# region Delete


@pytest.mark.router_decks
@patch("scooze.database.deck.delete_decks_all")
def test_delete_decks(mock_update: MagicMock, client: TestClient, modern_4c):
    # Acting as though the db is setup with just Four-color Control for purposes of this test
    mock_update.return_value = 1
    response = client.delete("/decks/delete/all")
    assert response.status_code == 200
    assert response.json()["message"] == "Deleted 1 deck(s)."


@pytest.mark.router_decks
@patch("scooze.database.deck.delete_decks_all")
def test_delete_decks_bad(mock_update: MagicMock, client: TestClient):
    mock_update.return_value = None
    response = client.delete("/decks/delete/all")
    assert response.status_code == 404
    assert response.json()["message"] == "No decks deleted."


# endregion
