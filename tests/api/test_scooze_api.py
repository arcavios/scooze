from unittest.mock import MagicMock, patch

import pytest
import scooze.api.card as card_api
from scooze.api import AsyncScoozeApi, ScoozeApi
from scooze.card import Card
from scooze.catalogs import Color
from scooze.models.card import CardModel, CardModelData


@pytest.mark.context
class TestScoozeApiWithPopulatedDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def populate_db(self, cards_json):
        for card_json in cards_json:
            card_data = CardModelData.model_validate_json(card_json)
            card = CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True))
            await card.create()

        yield

        await CardModel.delete_all()

    # async def test_get_card_by_async(self, recall_base: Card):
    #     async with AsyncScoozeApi(card_class=Card) as s:
    #         card = await s.get_card_by(property_name="name", value="Ancestral Recall")
    #         assert card == recall_base
    #         card = await s.get_card_by(property_name="colors", value=[Color.BLUE])
    #         assert card == recall_base
    #         card = await s.get_card_by(property_name="produced_mana", value=[])
    #         assert card == recall_base
    #         card = await s.get_card_by(property_name="producedMana", value=[])
    #         assert card == recall_base

    def test_get_card_by_sync(self, recall_base: Card):
        with ScoozeApi(card_class=Card) as s:
            card: Card = s.get_card_by(property_name="name", value="Ancestral Recall")
            recall_base.scooze_id = card.scooze_id
            assert card == recall_base
            card = s.get_card_by(property_name="colors", value=[Color.BLUE])
            assert card == recall_base
            card = s.get_card_by(property_name="produced_mana", value=[])
            print(card is None)
            assert card == recall_base
            card = s.get_card_by(property_name="producedMana", value=[])
            assert card == recall_base
