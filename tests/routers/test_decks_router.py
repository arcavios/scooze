from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from beanie import PydanticObjectId
from httpx import AsyncClient
from scooze.card import OracleCard
from scooze.deckpart import DeckPart
from scooze.models.card import CardModel, CardModelData
from scooze.models.deck import DeckModel, DeckModelData

from tests.routers.utils import dict_from_deckpart

# TODO(#273): Test Attraction and Sticker decks for deck router?


class TestDeckRouterWithPopulatedDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def populate_db(
        self,
        cards_json: list[str],
        archetype_modern_4c: str,
        main_modern_4c: DeckPart[OracleCard],
        side_modern_4c: DeckPart[OracleCard],
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
                "main": await dict_from_deckpart(main_modern_4c),
                "side": await dict_from_deckpart(side_modern_4c),
            }
        )

        deck = DeckModel.model_validate(deck_model_data.model_dump())
        await deck.create()

        yield

        await CardModel.delete_all()
        await DeckModel.delete_all()

    async def test_decks_root(self, api_client: AsyncClient):
        response = await api_client.get("/decks/")
        assert response.status_code == 200
        for deck_resp in response.json():
            assert PydanticObjectId.is_valid(deck_resp["_id"])

    async def test_decks_root_with_limit(self, api_client: AsyncClient):
        response = await api_client.get("/decks/", params={"limit": 1})
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 1
        for deck_resp in response_json:
            assert PydanticObjectId.is_valid(deck_resp["_id"])

    async def test_get_decks_by_archetype(self, api_client: AsyncClient, archetype_modern_4c: str):
        decks = await DeckModel.find({}, limit=1).to_list()
        response = await api_client.post("/decks/by?property_name=archetype", json=[archetype_modern_4c])
        assert response.status_code == 200
        response_json_archetypes = [deck_obj["archetype"] for deck_obj in response.json()]
        for deck in decks:
            assert deck.archetype in response_json_archetypes

    async def test_get_decks_by_none_found(self, api_client: AsyncClient):
        response = await api_client.post("/decks/by?property_name=archetype", json=["Grixis Death's Shadow"])
        assert response.status_code == 404
        assert response.json()["detail"] == "Decks not found."

    async def test_delete_decks(self, api_client: AsyncClient):
        num_decks = await DeckModel.count()
        response = await api_client.delete("/decks/delete/all")
        assert response.status_code == 200
        assert response.json() == f"Deleted {num_decks} deck(s)."

    @patch("scooze.routers.decks.DeckModel.delete_all")
    async def test_delete_decks_not_deleted(self, mock_delete_all: MagicMock, api_client: AsyncClient):
        mock_delete_all.return_value = None
        response = await api_client.delete("/decks/delete/all")
        assert response.status_code == 400
        assert response.json()["detail"] == "Decks weren't deleted."


class TestDecksRouterWithEmptyDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def clean_db(self):
        await DeckModel.delete_all()

    async def test_decks_root_no_decks(self, api_client: AsyncClient):
        response = await api_client.get("/decks/")
        assert response.status_code == 404
        assert response.json()["detail"] == "No decks found in the database."
