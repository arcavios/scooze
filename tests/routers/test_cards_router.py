from unittest.mock import MagicMock, patch

import pytest
from beanie import PydanticObjectId
from fastapi.testclient import TestClient
from httpx import AsyncClient
from mongomock import Collection
from scooze.models.card import CardModel, CardModelData


class TestCardsRouterWithPopulatedDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def populate_db(self, cards_json):
        for card_json in cards_json:
            card_data = CardModelData.model_validate_json(card_json)
            card = CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True))
            await card.create()

        yield

        await CardModel.get_motor_collection().delete_many({})

    async def test_cards_root(self, api_client: AsyncClient):
        response = await api_client.get("/cards/")
        assert response.status_code == 200
        for card_resp in response.json():
            assert PydanticObjectId.is_valid(card_resp["_id"])

    async def test_cards_root_with_limit(self, api_client: AsyncClient):
        response = await api_client.get("/cards/", params={"limit": 2})
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 2
        for card_resp in response_json:
            assert PydanticObjectId.is_valid(card_resp["_id"])


class TestCardsRouterWithEmptyDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def clean_db(self):
        await CardModel.get_motor_collection().delete_many({})

    async def test_cards_root_no_cards(self, api_client: AsyncClient):
        response = await api_client.get("/cards/")
        assert response.status_code == 404
        assert response.json()["detail"] == "No cards found in the database."

    async def test_add_cards(self, api_client: AsyncClient, omnath_json: dict, recall_json: dict):
        response = await api_client.post("/cards/add", json=[omnath_json, recall_json])
        assert response.status_code == 200
        assert response.json() == "Created 2 card(s)."
        cards = await CardModel.find({}).to_list()
        assert len(cards) == 2

    @patch("scooze.routers.cards.CardModel.insert_many")
    async def test_add_cards_bad(
        self,
        mock_insert_many: MagicMock,
        api_client: AsyncClient,
        omnath_json: dict,
        recall_json: dict,
    ):
        error_msg = "Test card create route error"

        def mock_insert_many_exception(_):
            raise Exception(error_msg)

        mock_insert_many.side_effect = mock_insert_many_exception
        response = await api_client.post("/cards/add", json=[omnath_json, recall_json])
        assert response.status_code == 400
        assert response.json()["detail"] == f"Failed to create new cards. Error: {error_msg}"


# region Fixtures


# @pytest.fixture
# def omnath(mock_cards_collection: Collection) -> CardModel:
#     db_omnath = mock_cards_collection.find_one({"name": "Omnath, Locus of Creation"})
#     return CardModel.model_validate(db_omnath)


# @pytest.fixture
# def chalice(mock_cards_collection: Collection) -> CardModel:
#     db_chalice = mock_cards_collection.find_one({"name": "Chalice of the Void"})
#     return CardModel.model_validate(db_chalice)


# @pytest.fixture
# def boseiju(mock_cards_collection: Collection) -> CardModel:
#     db_boseiju = mock_cards_collection.find_one({"name": "Boseiju, Who Endures"})
#     return CardModel.model_validate(db_boseiju)


# endregion


# # region Read


# @pytest.mark.router_cards
# @patch("scooze.database.card.get_cards_by_property")
# def test_get_cards_by_cmc(mock_get: MagicMock, client: TestClient, chalice: CardModel, boseiju: CardModel):
#     zero_drops = [chalice, boseiju]
#     mock_get.return_value: list[CardModel] = zero_drops
#     response = client.post("/cards/by?property_name=cmc", json=[0.0])
#     assert response.status_code == 200
#     response_json = response.json()
#     for card in zero_drops:
#         assert card.model_dump(mode="json") in response_json


# @pytest.mark.router_cards
# @patch("scooze.database.card.get_cards_by_property")
# def test_get_cards_by_cmc_none_found(mock_get: MagicMock, client: TestClient):
#     mock_get.return_value = None
#     response = client.post("/cards/by?property_name=cmc", json=[100.0])
#     assert response.status_code == 404
#     assert response.json()["message"] == "Cards not found."


# # endregion


# # region Delete


# @pytest.mark.router_cards
# @patch("scooze.database.card.delete_cards_all")
# def test_delete_cards(mock_update: MagicMock, client: TestClient, omnath: CardModel, chalice: CardModel):
#     # Acting as though the db is set up with just Omnath and Chalice for purposes of this test
#     mock_update.return_value = 2
#     response = client.delete("/cards/delete/all")
#     assert response.status_code == 200
#     assert response.json()["message"] == "Deleted 2 card(s)."


# @pytest.mark.router_cards
# @patch("scooze.database.card.delete_cards_all")
# def test_delete_cards_bad(mock_update: MagicMock, client: TestClient):
#     mock_update.return_value = None
#     response = client.delete("/cards/delete/all")
#     assert response.status_code == 404
#     assert response.json()["message"] == "No cards deleted."


# # endregion
