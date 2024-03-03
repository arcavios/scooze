from unittest.mock import MagicMock, patch

import scooze.api.card as card_api
from beanie import PydanticObjectId
from scooze.card import Card, FullCard, OracleCard
from scooze.errors import BulkAddError
from scooze.models.card import CardModel, CardModelData


class TestCardApiWithPopulatedDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def populate_db(self, cards_json):
        for card_json in cards_json:
            card_data = CardModelData.model_validate_json(card_json)
            card = CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True))
            await card.create()

        yield

        await CardModel.delete_all()

    async def test_get_base_card(self, recall_base: Card):
        result: Card = await card_api.get_card_by(property_name="name", value=recall_base.name, card_class=Card)
        recall_base.scooze_id = result.scooze_id  # recall_base doesn't start with a Scooze ID
        assert result == recall_base

    async def test_get_oracle_card(self, recall_oracle: OracleCard):
        result: OracleCard = await card_api.get_card_by(
            property_name="name", value=recall_oracle.name, card_class=OracleCard
        )
        recall_oracle.scooze_id = result.scooze_id  # recall_oracle doesn't start with a Scooze ID
        assert result == recall_oracle

    async def test_get_full_card(self, recall_full: FullCard):
        result: FullCard = await card_api.get_card_by(property_name="name", value=recall_full.name, card_class=FullCard)
        recall_full.scooze_id = result.scooze_id  # recall_full doesn't start with a Scooze ID
        assert result == recall_full

    async def test_get_card_bad(self):
        result = await card_api.get_card_by(property_name="name", value="This is not a card name", card_class=Card)
        assert result is None

    async def test_get_base_cards(self, cards_base: list[Card]):
        data = [CardModelData.model_validate(card.__dict__) for card in cards_base]
        models = [CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True)) for card_data in data]
        names = [model.name for model in models]
        results: list[Card] = await card_api.get_cards_by(property_name="name", values=names, card_class=Card)
        assert len(cards_base) == len(results)
        for item in zip(cards_base, results):
            card, result = item
            result.scooze_id = card.scooze_id
            assert card == result

    async def test_get_oracle_cards(self, cards_oracle: list[OracleCard]):
        data = [CardModelData.model_validate(card.__dict__) for card in cards_oracle]
        models = [CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True)) for card_data in data]
        names = [model.name for model in models]
        results: list[OracleCard] = await card_api.get_cards_by(
            property_name="name", values=names, card_class=OracleCard
        )
        assert len(cards_oracle) == len(results)
        for item in zip(cards_oracle, results):
            card, result = item
            result.scooze_id = card.scooze_id
            assert card == result

    async def test_get_full_cards(self, cards_full: list[FullCard]):
        data = [CardModelData.model_validate(card.__dict__) for card in cards_full]
        models = [CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True)) for card_data in data]
        names = [model.name for model in models]
        results: list[FullCard] = await card_api.get_cards_by(property_name="name", values=names, card_class=FullCard)
        assert len(cards_full) == len(results)
        for item in zip(cards_full, results):
            card, result = item
            result.scooze_id = card.scooze_id
            assert card == result

    async def test_get_all_cards_base(self):
        total_cards = await CardModel.count()
        results = await card_api.get_cards_all(card_class=Card)
        assert len(results) == total_cards

    async def test_get_cards_bad(self):
        results = await card_api.get_cards_by(
            property_name="name", values=["Not a card name", "Also not a card name"], card_class=Card
        )
        assert results == []


class TestCardApiDeletions:
    @pytest.fixture(autouse=True)
    async def populate_db(self, cards_json):
        num_cards = 0
        for card_json in cards_json:
            if num_cards >= 10:
                break
            card_data = CardModelData.model_validate_json(card_json)
            card = CardModel.model_validate(card_data.model_dump(mode="json"))
            await card.create()
            num_cards += 1

        yield

        # Just in case
        await CardModel.delete_all()

    async def test_delete_card(self):
        card = await CardModel.find_one()
        result = await card_api.delete_card(id=card.id)
        assert result is True

    async def test_delete_card_bad_id(self):
        result = await card_api.delete_card(id=PydanticObjectId())
        assert result is False

    async def test_delete_card_malformed_id(self):
        result = await card_api.delete_card(id="not a valid id")
        assert result is False

    async def test_delete_cards(self):
        total_cards = await CardModel.count()
        result = await card_api.delete_cards_all()
        assert result == total_cards

    @patch("scooze.api.card.CardModel.delete_all")
    async def test_delete_cards_bad(self, mock_delete: MagicMock):
        mock_delete.return_value = None
        result = await card_api.delete_cards_all()
        assert result is None


class TestCardApiWithEmptyDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def clean_db(self):
        await CardModel.delete_all()

    async def test_add_base_card(self, recall_base):
        result = await card_api.add_card(card=recall_base)
        assert PydanticObjectId.is_valid(result)

    async def test_add_oracle_card(self, recall_oracle):
        result = await card_api.add_card(card=recall_oracle)
        assert PydanticObjectId.is_valid(result)

    async def test_add_full_card(self, recall_full):
        result = await card_api.add_card(card=recall_full)
        assert PydanticObjectId.is_valid(result)

    @patch("scooze.api.card.CardModel.create")
    async def test_add_card_bad(self, mock_create: MagicMock, recall_base):
        error_msg = "Test card create route error"

        def mock_create_exception():
            raise Exception(error_msg)

        mock_create.side_effect = mock_create_exception
        result = await card_api.add_card(card=recall_base)
        assert result is None

    async def test_add_base_cards(self, cards_base: list[Card]):
        results = await card_api.add_cards(cards=cards_base)
        for result in results:
            assert PydanticObjectId.is_valid(result)

    async def test_add_oracle_cards(self, cards_oracle: list[OracleCard]):
        results = await card_api.add_cards(cards=cards_oracle)
        for result in results:
            assert PydanticObjectId.is_valid(result)

    async def test_add_full_cards(self, cards_full: list[FullCard]):
        results = await card_api.add_cards(cards=cards_full)
        for result in results:
            assert PydanticObjectId.is_valid(result)

    @patch("scooze.api.card.CardModel.insert_many")
    async def test_add_cards_bad(self, mock_insert_many: MagicMock, cards_base: list[Card]):
        error_msg = "Test card create route error"

        def mock_insert_exception():
            raise Exception(error_msg)

        mock_insert_many.side_effect = mock_insert_exception
        with pytest.raises(BulkAddError):
            await card_api.add_cards(cards=cards_base)
