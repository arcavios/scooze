from datetime import datetime

import pytest
from bson import ObjectId
from mongomock import Collection, MongoClient
from scooze.card import OracleCard
from scooze.enum import DbCollection
from scooze.deck import DeckPart
from scooze.models.card import CardModelData
from scooze.models.deck import DeckModelIn


@pytest.fixture(scope="session")
def mock_scooze_client():
    return MongoClient()


@pytest.fixture(scope="session")
def mock_cards_collection(mock_scooze_client: MongoClient, cards_json: list[str]) -> Collection:
    cards_collection = mock_scooze_client.scooze[DbCollection.CARDS]
    for card in cards_json:
        cards_collection.insert_one(CardModelData.model_validate_json(card).model_dump(mode="json", by_alias=True))
    return cards_collection


@pytest.fixture()
def mock_decks_collection(mock_scooze_client: MongoClient, deck_model_modern_4c: DeckModelIn) -> Collection:
    decks_collection = mock_scooze_client.scooze[DbCollection.DECKS]
    decks_collection.insert_one(deck_model_modern_4c.model_dump(mode="json", by_alias=True))
    return decks_collection


@pytest.fixture
def deck_model_modern_4c(
    archetype_modern_4c: str,
    main_modern_4c_dict: dict[ObjectId, int],
    side_modern_4c_dict: dict[ObjectId, int],
    today: datetime,
) -> DeckModelIn:
    return DeckModelIn.model_validate(
        {
            "archetype": archetype_modern_4c,
            "format": "modern",
            "date_played": today,
            "main": main_modern_4c_dict,
            "side": side_modern_4c_dict,
        }
    )


@pytest.fixture
def main_modern_4c_dict(main_modern_4c: DeckPart[OracleCard], mock_cards_collection: Collection) -> dict[ObjectId, int]:
    return {mock_cards_collection.find_one({"name": c.name})["_id"]: q for c, q in main_modern_4c.cards.items()}


@pytest.fixture
def side_modern_4c_dict(side_modern_4c: DeckPart[OracleCard], mock_cards_collection: Collection) -> dict[ObjectId, int]:
    return {mock_cards_collection.find_one({"name": c.name})["_id"]: q for c, q in side_modern_4c.cards.items()}
