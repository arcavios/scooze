from unittest.mock import MagicMock, patch

import pytest
from beanie import PydanticObjectId
from httpx import AsyncClient
from scooze.models.card import CardModel, CardModelData


class TestCardsRouterWithPopulatedDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def populate_db(self, cards_json: list[str]):
        for card_json in cards_json:
            print(CardModel.get_bson_encoders())
            card_data = CardModelData.model_validate_json(card_json)
            card = CardModel.model_validate(card_data.model_dump())
            await card.create()
            raise Exception

        yield

        await CardModel.delete_all()

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

    async def test_get_cards_by_ids(self, api_client: AsyncClient):
        cards = await CardModel.find({}, limit=2).to_list()
        response = await api_client.post("/cards/by?property_name=id", json=[str(card.id) for card in cards])
        assert response.status_code == 200
        response_json_ids = [card_obj["_id"] for card_obj in response.json()]
        for card in cards:
            assert str(card.id) in response_json_ids

    async def test_get_cards_by_names(self, api_client: AsyncClient):
        cards = await CardModel.find({}, limit=2).to_list()
        response = await api_client.post("/cards/by?property_name=name", json=[card.name for card in cards])
        assert response.status_code == 200
        response_json_names = [card_obj["name"] for card_obj in response.json()]
        for card in cards:
            assert card.name in response_json_names

    async def test_get_cards_by_none_found(self, api_client: AsyncClient):
        response = await api_client.post("/cards/by?property_name=id", json=[str(PydanticObjectId())])
        assert response.status_code == 404
        assert response.json()["detail"] == "Cards not found."

    async def test_delete_cards(self, api_client: AsyncClient):
        num_cards = await CardModel.find({}).count()
        response = await api_client.delete("/cards/delete/all")
        assert response.status_code == 200
        assert response.json() == f"Deleted {num_cards} card(s)."

    @patch("scooze.routers.cards.CardModel.delete_all")
    async def test_delete_cards_not_deleted(self, mock_delete_all: MagicMock, api_client: AsyncClient):
        mock_delete_all.return_value = None
        response = await api_client.delete(f"/cards/delete/all")
        assert response.status_code == 400
        assert response.json()["detail"] == "Cards weren't deleted."


class TestCardsRouterWithEmptyDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def clean_db(self):
        await CardModel.get_motor_collection().delete_many({})

    async def test_cards_root_no_cards(self, api_client: AsyncClient):
        response = await api_client.get("/cards/")
        assert response.status_code == 404
        assert response.json()["detail"] == "No cards found in the database."

    async def test_add_cards(
        self, api_client: AsyncClient, json_omnath_locus_of_creation: dict, json_ancestral_recall: dict
    ):
        response = await api_client.post("/cards/add", json=[json_omnath_locus_of_creation, json_ancestral_recall])
        assert response.status_code == 200
        assert response.json() == "Created 2 card(s)."
        cards = await CardModel.find({}).to_list()
        assert len(cards) == 2

    @patch("scooze.routers.cards.CardModel.insert_many")
    async def test_add_cards_bad(
        self,
        mock_insert_many: MagicMock,
        api_client: AsyncClient,
        json_omnath_locus_of_creation: dict,
        json_ancestral_recall: dict,
    ):
        error_msg = "Test card create route error"

        def mock_insert_many_exception(_):
            raise Exception(error_msg)

        mock_insert_many.side_effect = mock_insert_many_exception
        response = await api_client.post("/cards/add", json=[json_omnath_locus_of_creation, json_ancestral_recall])
        assert response.status_code == 400
        assert response.json()["detail"] == f"Failed to create new cards. Error: {error_msg}"
