from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from mongomock import Collection
from scooze.models.deck import DeckModelIn, DeckModelOut

# region Fixtures


# endregion


@patch("scooze.database.deck.get_decks_random")
def test_deck_root(
    mock_get_random: MagicMock, client: TestClient, mock_decks_collection: Collection, deck_model_modern_4c: DeckModelIn
):
    mock_get_random.return_value = [
        DeckModelOut.model_validate(mock_decks_collection.find_one({"archetype": "Four-color Control"}))
    ]
    response = client.get("/deck/")
    assert response.status_code == 200
    response_json = response.json()
    for k, v in deck_model_modern_4c.model_dump(mode="json").items():
        assert response_json[k] == v


# region Create


@patch("scooze.database.deck.add_deck")
def test_add_deck(mock_add: MagicMock, client: TestClient, deck_model_modern_4c: DeckModelIn):
    deck_json = deck_model_modern_4c.model_dump(mode="json", by_alias=True)
    mock_add.return_value: DeckModelOut = DeckModelOut.model_validate(deck_json)
    response = client.post("/deck/add", json={"deck": deck_json})
    assert response.status_code == 200
    response_json = response.json()
    for k, v in deck_model_modern_4c.model_dump(mode="json").items():
        assert response_json[k] == v


@patch("scooze.database.deck.add_deck")
def test_add_deck_bad(mock_add: MagicMock, client: TestClient, deck_model_modern_4c: DeckModelIn):
    deck_json = deck_model_modern_4c.model_dump(mode="json", by_alias=True)
    mock_add.return_value = None
    response = client.post("/deck/add", json={"deck": deck_json})
    assert response.status_code == 400
    assert response.json()["message"] == "Failed to create a new deck."


# endregion

# region Read


@patch("scooze.database.deck.get_deck_by_property")
def test_get_deck_by_id(
    mock_get: MagicMock, client: TestClient, deck_model_modern_4c: DeckModelIn, mock_decks_collection: Collection
):
    db_4c_id = mock_decks_collection.find_one({"archetype": "Four-color Control"})["_id"]
    deck_json = deck_model_modern_4c.model_dump(mode="json", by_alias=True)
    deck_json["_id"] = db_4c_id
    mock_get.return_value: DeckModelOut = DeckModelOut.model_validate(deck_json)
    response = client.get(f"/deck/id/{str(db_4c_id)}")
    assert response.status_code == 200
    response_json = response.json()
    for k, v in deck_model_modern_4c.model_dump(mode="json").items():
        assert response_json[k] == v


@patch("scooze.database.deck.get_deck_by_property")
def test_get_deck_by_id_bad_id(mock_get: MagicMock, client: TestClient):
    mock_get.return_value = None
    response = client.get("/deck/id/blarghl")
    assert response.status_code == 404
    assert response.json()["message"] == "Deck with id blarghl not found."


# endregion


# region Update


@patch("scooze.database.deck.update_deck")
def test_update_deck(
    mock_update: MagicMock, client: TestClient, deck_model_modern_4c: DeckModelIn, mock_decks_collection: Collection
):
    db_4c_id = mock_decks_collection.find_one({"archetype": "Four-color Control"})["_id"]
    deck_json = deck_model_modern_4c.model_dump(mode="json", by_alias=True)
    updated_deck_json = deck_json.copy()
    updated_deck_json.update({"side": {}})
    mock_update.return_value: DeckModelOut = DeckModelOut.model_validate(updated_deck_json)
    response = client.patch(f"/deck/update/{str(db_4c_id)}", json={"deck": {"side": {}}})
    assert response.status_code == 200
    response_json = response.json()
    updated_deck_json["date_played"] = updated_deck_json.pop("datePlayed")
    for k, v in updated_deck_json.items():
        assert response_json[k] == v


@patch("scooze.database.deck.update_deck")
def test_update_deck_bad_id(mock_update: MagicMock, client: TestClient):
    mock_update.return_value = None
    response = client.patch("/deck/update/blarghl", json={"deck": {}})
    assert response.status_code == 404
    assert response.json()["message"] == "Deck with id blarghl not found."


# endregion


# region Delete


@patch("scooze.database.deck.delete_deck")
def test_delete_deck(
    mock_delete: MagicMock, client: TestClient, deck_model_modern_4c: DeckModelIn, mock_decks_collection: Collection
):
    db_4c_id = mock_decks_collection.find_one({"archetype": "Four-color Control"})["_id"]
    deck_json = deck_model_modern_4c.model_dump(mode="json", by_alias=True)
    deck_json["_id"] = db_4c_id
    mock_delete.return_value: DeckModelOut = DeckModelOut.model_validate(deck_json)
    response = client.delete(f"/deck/delete/{str(db_4c_id)}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Deck with id {db_4c_id} deleted."


@patch("scooze.database.deck.delete_deck")
def test_delete_deck_bad_id(mock_delete: MagicMock, client: TestClient):
    mock_delete.return_value = None
    response = client.delete("/deck/delete/blarghl")
    assert response.status_code == 400
    assert response.json()["message"] == "Deck with id blarghl not deleted."


# endregion
