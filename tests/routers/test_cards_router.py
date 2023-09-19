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


@pytest.mark.router_card
@patch("scooze.database.card.get_cards_random")
def test_cards_root(
    mock_get: MagicMock, client: TestClient, omnath: CardModelOut, chalice: CardModelOut, boseiju: CardModelOut
):
    mock_get.return_value: list[CardModelOut] = [omnath, chalice, boseiju]
    response = client.get("/cards/")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 3
    assert omnath.model_dump(mode="json") in response_json
    assert chalice.model_dump(mode="json") in response_json
    assert boseiju.model_dump(mode="json") in response_json


@pytest.mark.router_card
@patch("scooze.database.card.get_cards_random")
def test_cards_root(mock_get: MagicMock, client: TestClient):
    mock_get.return_value = None
    response = client.get("/cards/")
    assert response.status_code == 404
    assert response.json()["message"] == "No cards found in the database."


# region Create


@pytest.mark.router_card
@patch("scooze.database.card.add_cards")
def test_add_card(
    mock_add: MagicMock, client: TestClient, omnath: CardModelOut, chalice: CardModelOut, boseiju: CardModelOut
):
    mock_add.return_value: list[str] = [str(card.id) for card in [omnath, chalice, boseiju]]
    response = client.post(
        "/cards/add",
        json={
            "cards": [
                omnath.model_dump(mode="json", by_alias=True),
                # chalice.model_dump(mode="json"),
                # boseiju.model_dump(mode="json"),
            ]
        },
    )
    # print(response.request.content)
    assert response.status_code == 200
    assert response.json()["message"] == "Created 3 cards."


# @pytest.mark.router_card
# @patch("scooze.database.card.add_cards")
# def test_add_card_bad(mock_add: MagicMock, client: TestClient, omnath: CardModelOut):
#     mock_add.return_value = None
#     response = client.post("/card/add", json={"card": omnath.model_dump(mode="json", by_alias=True)})
#     assert response.status_code == 400
#     assert response.json()["message"] == "Failed to create a new card."


# endregion

# region Read


# @pytest.mark.router_card
# @patch("scooze.database.card.get_cards_by_property")
# def test_get_card_by_id(mock_get: MagicMock, client: TestClient, omnath: CardModelOut):
#     mock_get.return_value: CardModelOut = omnath
#     response = client.get(f"/card/id/{str(omnath.id)}")
#     assert response.status_code == 200
#     response_json = response.json()
#     for k, v in omnath.model_dump(mode="json").items():
#         assert response_json[k] == v


# @pytest.mark.router_card
# @patch("scooze.database.card.get_cards_by_property")
# def test_get_card_by_id_bad_id(mock_get: MagicMock, client: TestClient):
#     mock_get.return_value = None
#     response = client.get("/card/id/blarghl")
#     assert response.status_code == 404
#     assert response.json()["message"] == "Card with id blarghl not found."


# @pytest.mark.router_card
# @patch("scooze.database.card.get_cards_by_property")
# def test_get_card_by_name(mock_get: MagicMock, client: TestClient, omnath: CardModelOut):
#     mock_get.return_value: CardModelOut = omnath
#     response = client.get(f"/card/name/{omnath.name}")
#     assert response.status_code == 200
#     response_json = response.json()
#     for k, v in omnath.model_dump(mode="json").items():
#         assert response_json[k] == v


# @pytest.mark.router_card
# @patch("scooze.database.card.get_cards_by_property")
# def test_get_card_by_name_bad_name(mock_get: MagicMock, client: TestClient):
#     mock_get.return_value = None
#     response = client.get("/card/name/blarghl")
#     assert response.status_code == 404
#     assert response.json()["message"] == "Card with name blarghl not found."


# endregion


# region Delete


# @pytest.mark.router_card
# @patch("scooze.database.card.delete_cards_all")
# def test_delete_card(mock_update: MagicMock, client: TestClient, omnath: CardModelOut):
#     mock_update.return_value: CardModelOut = omnath
#     response = client.delete(f"/card/delete/{omnath.id}")
#     assert response.status_code == 200
#     assert response.json()["message"] == f"Card with id {omnath.id} deleted."


# @pytest.mark.router_card
# @patch("scooze.database.card.delete_card_all")
# def test_delete_card_bad_id(mock_update: MagicMock, client: TestClient):
#     mock_update.return_value = None
#     response = client.delete("/card/delete/blarghl")
#     assert response.status_code == 404
#     assert response.json()["message"] == "Card with id blarghl not deleted."


# endregion
