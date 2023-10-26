from unittest.mock import MagicMock, patch

import pytest
from beanie import PydanticObjectId
from fastapi.testclient import TestClient
from httpx import AsyncClient
from mongomock import Collection
from scooze.models.card import CardModel, CardModelData

# region Fixtures


# @pytest.fixture
# def omnath(mock_cards_collection: Collection) -> CardModel:
#     # db_omnath = mock_cards_collection.find_one({"name": "Omnath, Locus of Creation"})
#     # from pprint import pprint

#     # pprint(db_omnath)
#     # return CardModel.model_validate(db_omnath)
#     return None


@pytest.fixture(autouse=True)
async def set_up_modern_4c(cards_json):
    for card_json in cards_json:
        card_data = CardModelData.model_validate_json(card_json)
        card = CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True))
        await card.create()


@pytest.fixture()
async def clean_cards_db():
    async def inner():
        await CardModel.get_motor_collection().delete_many({})

    return inner


# endregion


@pytest.mark.asyncio
async def test_card_root(api_client: AsyncClient):
    response = await api_client.get("/card/")
    assert response.status_code == 200
    response_json = response.json()
    card_id = response_json["_id"]
    assert PydanticObjectId.is_valid(card_id)


async def test_card_root_no_cards(clean_cards_db, api_client: AsyncClient):
    await clean_cards_db()
    response = await api_client.get("/card/")
    assert response.status_code == 404
    assert response.json()["detail"] == "No cards found in the database."


# # region Create


# @pytest.mark.router_card
# @patch("scooze.database.card.add_card")
# def test_add_card(mock_add: MagicMock, client: TestClient, omnath: CardModel):
#     mock_add.return_value: CardModel = omnath
#     response = client.post("/card/add", json={"card": omnath.model_dump(mode="json", by_alias=True)})
#     assert response.status_code == 200
#     response_json = response.json()
#     for k, v in omnath.model_dump(mode="json").items():
#         assert response_json[k] == v


# @pytest.mark.router_card
# @patch("scooze.database.card.add_card")
# def test_add_card_bad(mock_add: MagicMock, client: TestClient, omnath: CardModel):
#     mock_add.return_value = None
#     response = client.post("/card/add", json={"card": omnath.model_dump(mode="json", by_alias=True)})
#     assert response.status_code == 400
#     assert response.json()["message"] == "Failed to create a new card."


# # endregion

# # region Read


# @pytest.mark.router_card
# @patch("scooze.database.card.get_card_by_property")
# def test_get_card_by_id(mock_get: MagicMock, client: TestClient, omnath: CardModel):
#     mock_get.return_value: CardModel = omnath
#     response = client.get(f"/card/id/{str(omnath.scooze_id)}")
#     assert response.status_code == 200
#     response_json = response.json()
#     for k, v in omnath.model_dump(mode="json").items():
#         assert response_json[k] == v


# @pytest.mark.router_card
# @patch("scooze.database.card.get_card_by_property")
# def test_get_card_by_id_bad_id(mock_get: MagicMock, client: TestClient):
#     mock_get.return_value = None
#     response = client.get("/card/id/blarghl")
#     assert response.status_code == 404
#     assert response.json()["message"] == "Card with id blarghl not found."


# @pytest.mark.router_card
# @patch("scooze.database.card.get_card_by_property")
# def test_get_card_by_name(mock_get: MagicMock, client: TestClient, omnath: CardModel):
#     mock_get.return_value: CardModel = omnath
#     response = client.get(f"/card/name/{omnath.name}")
#     assert response.status_code == 200
#     response_json = response.json()
#     for k, v in omnath.model_dump(mode="json").items():
#         assert response_json[k] == v


# @pytest.mark.router_card
# @patch("scooze.database.card.get_card_by_property")
# def test_get_card_by_name_bad_name(mock_get: MagicMock, client: TestClient):
#     mock_get.return_value = None
#     response = client.get("/card/name/blarghl")
#     assert response.status_code == 404
#     assert response.json()["message"] == "Card with name blarghl not found."


# # endregion

# # region Update


# @pytest.mark.router_card
# @patch("scooze.database.card.update_card")
# def test_update_card(mock_update: MagicMock, client: TestClient, omnath: CardModel):
#     omnath_dump = omnath.model_dump(mode="json", by_alias=True)
#     update_data = {"cmc": 5.0}
#     omnath_dump.update(update_data)
#     new_omnath = CardModel.model_validate(omnath_dump)
#     mock_update.return_value: CardModel = new_omnath
#     response = client.patch(f"/card/update/{omnath.scooze_id}", json={"card": update_data})
#     assert response.status_code == 200
#     response_json = response.json()
#     for k, v in new_omnath.model_dump(mode="json").items():
#         assert response_json[k] == v


# @pytest.mark.router_card
# @patch("scooze.database.card.update_card")
# def test_update_card_bad_id(mock_update: MagicMock, client: TestClient):
#     mock_update.return_value = None
#     response = client.patch("/card/update/blarghl", json={"card": {}})
#     assert response.status_code == 404
#     assert response.json()["message"] == "Card with id blarghl not found."


# # endregion


# # region Delete


# @pytest.mark.router_card
# @patch("scooze.database.card.delete_card")
# def test_delete_card(mock_update: MagicMock, client: TestClient, omnath: CardModel):
#     mock_update.return_value: CardModel = omnath
#     response = client.delete(f"/card/delete/{omnath.scooze_id}")
#     assert response.status_code == 200
#     assert response.json()["message"] == f"Card with id {omnath.scooze_id} deleted."


# @pytest.mark.router_card
# @patch("scooze.database.card.delete_card")
# def test_delete_card_bad_id(mock_update: MagicMock, client: TestClient):
#     mock_update.return_value = None
#     response = client.delete("/card/delete/blarghl")
#     assert response.status_code == 404
#     assert response.json()["message"] == "Card with id blarghl not deleted."


# # endregion
