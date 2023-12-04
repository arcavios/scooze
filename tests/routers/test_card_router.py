from unittest.mock import MagicMock, patch

import pytest
from beanie import PydanticObjectId
from httpx import AsyncClient
from scooze.models.card import CardModel, CardModelData


class TestCardRouterWithPopulatedDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def populate_db(self, cards_json):
        for card_json in cards_json:
            card_data = CardModelData.model_validate_json(card_json)
            card = CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True))
            await card.create()

        yield

        await CardModel.delete_all()

    async def test_card_root(self, api_client: AsyncClient):
        response = await api_client.get("/card/")
        assert response.status_code == 200
        response_json = response.json()
        card_id = response_json["_id"]
        assert PydanticObjectId.is_valid(card_id)

    async def test_get_card_by_id(self, api_client: AsyncClient):
        first_card = await CardModel.find_one({})
        response = await api_client.get(f"/card/id/{first_card.id}")
        assert response.status_code == 200
        response_json = response.json()
        for k, v in first_card.model_dump(mode="json", by_alias=True).items():
            assert response_json[k] == v

    async def test_get_card_bad_id(self, api_client: AsyncClient):
        response = await api_client.get("/card/id/blarghl")
        assert response.status_code == 422
        assert response.json()["detail"] == "Must give a valid ID."

    async def test_get_card_fake_id(self, api_client: AsyncClient):
        fake_id = PydanticObjectId()
        response = await api_client.get(f"/card/id/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == f"Card with ID {fake_id} not found."

    async def test_get_card_by_name(self, api_client: AsyncClient):
        first_card = await CardModel.find_one({})
        response = await api_client.get(f"/card/name/{first_card.name}")
        assert response.status_code == 200
        response_json = response.json()
        for k, v in first_card.model_dump(mode="json", by_alias=True).items():
            assert response_json[k] == v

    async def test_get_card_bad_name(self, api_client: AsyncClient):
        response = await api_client.get("/card/name/not a valid magic card name")
        assert response.status_code == 404
        assert response.json()["detail"] == "Card with name 'not a valid magic card name' not found."

    async def test_update_card(self, api_client: AsyncClient):
        first_card = await CardModel.find_one({})
        update_data = {"cmc": 5.0}
        response = await api_client.patch(f"/card/update/{first_card.id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["cmc"] == 5.0
        first_card_post_update = await CardModel.get(first_card.id)
        assert first_card_post_update.cmc == 5.0

    async def test_update_card_bad_id(self, api_client: AsyncClient):
        response = await api_client.patch(f"/card/update/blarghl", json={})
        assert response.status_code == 422
        assert response.json()["detail"] == "Must give a valid ID."

    async def test_update_card_fake_id(self, api_client: AsyncClient):
        fake_id = PydanticObjectId()
        response = await api_client.patch(f"/card/update/{fake_id}", json={})
        assert response.status_code == 404
        assert response.json()["detail"] == f"Card with ID {fake_id} not found."

    async def test_delete_card(self, api_client: AsyncClient):
        first_card = await CardModel.find_one({})
        response = await api_client.delete(f"/card/delete/{first_card.id}")
        assert response.status_code == 200
        assert response.json() == f"Card with ID {first_card.id} deleted."

    async def test_delete_card_bad_id(self, api_client: AsyncClient):
        response = await api_client.delete("/card/delete/blarghl")
        assert response.status_code == 422
        assert response.json()["detail"] == "Must give a valid ID."

    async def test_delete_card_fake_id(self, api_client: AsyncClient):
        fake_id = PydanticObjectId()
        response = await api_client.delete(f"/card/delete/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == f"Card with ID {fake_id} not found."

    @patch("scooze.routers.card.CardModel.delete")
    async def test_delete_card_not_deleted(self, mock_delete: MagicMock, api_client: AsyncClient):
        mock_delete.return_value = None
        first_card = await CardModel.find_one({})
        response = await api_client.delete(f"/card/delete/{first_card.id}")
        assert response.status_code == 400
        assert response.json()["detail"] == f"Card with ID {first_card.id} not deleted."


class TestCardRouterWithEmptyDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def clean_db(self):
        await CardModel.delete_all()

    async def test_card_root_no_cards(self, api_client: AsyncClient):
        response = await api_client.get("/card/")
        assert response.status_code == 404
        assert response.json()["detail"] == "No cards found in the database."

    async def test_add_card(
        self, api_client: AsyncClient, json_omnath_locus_of_creation: dict, cardmodel_omnath: CardModel
    ):
        response = await api_client.post("/card/add", json=json_omnath_locus_of_creation)
        assert response.status_code == 200
        card = await CardModel.get(response.json()["_id"])
        assert card.model_dump(mode="json", exclude=["id"]) == cardmodel_omnath.model_dump(mode="json", exclude=["id"])

    @patch("scooze.routers.card.CardModel.create")
    async def test_add_card_bad(
        self, mock_create: MagicMock, api_client: AsyncClient, json_omnath_locus_of_creation: dict
    ):
        error_msg = "Test card create route error"

        def mock_create_exception():
            raise Exception(error_msg)

        mock_create.side_effect = mock_create_exception
        response = await api_client.post("/card/add", json=json_omnath_locus_of_creation)
        assert response.status_code == 400
        assert response.json()["detail"] == f"Failed to create a new card. Error: {error_msg}"
