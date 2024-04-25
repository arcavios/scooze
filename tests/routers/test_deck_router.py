from datetime import date
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest
from beanie import PydanticObjectId
from httpx import AsyncClient
from scooze.card import OracleCard
from scooze.cardlist import CardList
from scooze.models.card import CardModel, CardModelData
from scooze.models.deck import DeckModel, DeckModelData

from tests.routers.utils import dict_from_cardlist

# TODO(#273): Test Attraction and Sticker decks for deck router?


class TestDeckRouterWithPopulatedDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def populate_db(
        self,
        cards_json: list[str],
        archetype_modern_4c: str,
        main_modern_4c: CardList[OracleCard],
        side_modern_4c: CardList[OracleCard],
        today: date,
    ):
        for card_json in cards_json:
            card_data = CardModelData.model_validate_json(card_json)
            card = CardModel.model_validate(card_data.model_dump())
            await card.create()

        deck_model_data = DeckModelData.model_validate(
            {
                "archetype": archetype_modern_4c,
                "format": "modern",
                "date_played": today,
                "main": await dict_from_cardlist(main_modern_4c),
                "side": await dict_from_cardlist(side_modern_4c),
            }
        )

        deck = DeckModel.model_validate(deck_model_data.model_dump())
        await deck.create()

        yield

        await CardModel.delete_all()
        await DeckModel.delete_all()

    async def test_deck_root(self, api_client: AsyncClient):
        response = await api_client.get("/deck/")
        assert response.status_code == HTTPStatus.OK
        assert PydanticObjectId.is_valid(response.json()["_id"])

    async def test_get_deck_by_id(self, api_client: AsyncClient):
        first_deck = await DeckModel.find_one()
        response = await api_client.get(f"/deck/id/{first_deck.id}")
        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        for k, v in first_deck.model_dump(mode="json", by_alias=True).items():
            assert response_json[k] == v

    async def test_get_deck_bad_id(self, api_client: AsyncClient):
        response = await api_client.get("/deck/id/blarghl")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json()["detail"] == "Must give a valid ID."

    async def test_get_deck_fake_id(self, api_client: AsyncClient):
        fake_id = PydanticObjectId()
        response = await api_client.get(f"/deck/id/{fake_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == f"Deck with ID {fake_id} not found."

    async def test_update_deck(self, api_client: AsyncClient):
        new_archetype = "Definitely not 4c Pile"
        first_deck = await DeckModel.find_one()
        update_data = {"archetype": new_archetype}
        response = await api_client.patch(f"/deck/update/{first_deck.id}", json=update_data)
        assert response.status_code == HTTPStatus.OK
        assert response.json()["archetype"] == new_archetype
        first_deck_post_update = await DeckModel.get(first_deck.id)
        assert first_deck_post_update.archetype == new_archetype

    async def test_update_deck_bad_id(self, api_client: AsyncClient):
        response = await api_client.patch(f"/deck/update/blarghl", json={})
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json()["detail"] == "Must give a valid ID."

    async def test_update_deck_fake_id(self, api_client: AsyncClient):
        fake_id = PydanticObjectId()
        response = await api_client.patch(f"/deck/update/{fake_id}", json={})
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == f"Deck with ID {fake_id} not found."

    async def test_delete_deck(self, api_client: AsyncClient):
        response = await api_client.delete("/deck/delete/blarghl")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json()["detail"] == "Must give a valid ID."

    async def test_delete_deck_fake_id(self, api_client: AsyncClient):
        fake_id = PydanticObjectId()
        response = await api_client.delete(f"/deck/delete/{fake_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == f"Deck with ID {fake_id} not found."

    @patch("scooze.routers.deck.DeckModel.delete")
    async def test_delete_deck_not_deleted(self, mock_delete: MagicMock, api_client: AsyncClient):
        mock_delete.return_value = None
        first_card = await DeckModel.find_one()
        response = await api_client.delete(f"/deck/delete/{first_card.id}")
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["detail"] == f"Deck with ID {first_card.id} not deleted."


class TestDeckRouterWithEmptyDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def clean_db(self):
        await DeckModel.delete_all()

    async def test_deck_root_no_decks(self, api_client: AsyncClient):
        response = await api_client.get("/deck/")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == "No decks found in the database."
