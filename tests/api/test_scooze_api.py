from unittest.mock import MagicMock, patch

import pytest
from beanie import init_beanie
from scooze.api import AsyncScoozeApi, ScoozeApi
from scooze.card import Card
from scooze.catalogs import Color
from scooze.config import CONFIG
from scooze.models.card import CardModel, CardModelData
from scooze.mongo import db


@pytest.mark.context
class TestScoozeApiWithPopulatedDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def populate_db(self, cards_json, mongo_helper):
        await mongo_helper.mock_connect()
        await init_beanie(database=db.client[CONFIG.mongo_db], document_models=[CardModel])

        for card_json in cards_json:
            card_data = CardModelData.model_validate_json(card_json)
            card = CardModel.model_validate(card_data.model_dump())
            await card.create()

        yield

        await CardModel.delete_all()
        await mongo_helper.mock_close()

    @patch("scooze.api.mongo_connect")
    @patch("scooze.api.mongo_close")
    @patch("scooze.api.init_beanie")
    async def test_get_card_by_async(
        self,
        mock_beanie: MagicMock,
        mock_close: MagicMock,
        mock_connect: MagicMock,
        recall_base: Card,
    ):
        async with AsyncScoozeApi() as s:
            card = await s.get_card_by(property_name="name", value="Ancestral Recall")
            recall_base.scooze_id = card.scooze_id
            assert card == recall_base
            card = await s.get_card_by(property_name="colors", value=[Color.BLUE])
            assert card == recall_base
            card = await s.get_card_by(property_name="oracle_text", value="Target player draws three cards.")
            assert card == recall_base
            card = await s.get_card_by(property_name="oracleText", value="Target player draws three cards.")
            assert card == recall_base

        mock_connect.assert_called_once()
        mock_close.assert_called_once()
        mock_beanie.assert_called_once()

    @patch("scooze.api.mongo_connect")
    @patch("scooze.api.mongo_close")
    @patch("scooze.api.init_beanie")
    def test_get_card_by_sync(
        self,
        mock_beanie: MagicMock,
        mock_close: MagicMock,
        mock_connect: MagicMock,
        recall_base: Card,
    ):
        with ScoozeApi() as s:
            card: Card = s.get_card_by(property_name="name", value="Ancestral Recall")
            recall_base.scooze_id = card.scooze_id
            assert card == recall_base
            card = s.get_card_by(property_name="colors", value=[Color.BLUE])
            assert card == recall_base
            card = s.get_card_by(property_name="oracle_text", value="Target player draws three cards.")
            assert card == recall_base
            card = s.get_card_by(property_name="oracleText", value="Target player draws three cards.")
            assert card == recall_base

        mock_connect.assert_called_once()
        mock_close.assert_called_once()
        mock_beanie.assert_called_once()
