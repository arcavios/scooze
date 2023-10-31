import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

import pytest
from asgi_lifespan import LifespanManager
from beanie import init_beanie
from bson import ObjectId
from fastapi import FastAPI
from httpx import AsyncClient
from mongomock import Collection, MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from scooze.card import OracleCard
from scooze.catalogs import DbCollection
from scooze.config import CONFIG
from scooze.deck import DeckPart
from scooze.models.card import CardModel, CardModelData
from scooze.models.deck import DeckModelIn
from scooze.mongo import db

# @pytest.fixture(scope="session")
# def mock_cards_collection(db, cards_json: list[str]) -> Collection:
#     # from pprint import pprint

#     # pprint(CardModel.get_motor_collection())
#     # for card_json in cards_json:
#     #     card_data = CardModelData.model_validate_json(card_json)
#     #     card = CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True))
#     #     card.create()
#     return db.scooze_test[DbCollection.CARDS]


# @pytest.fixture()
# def mock_decks_collection(db, deck_model_modern_4c: DeckModelIn) -> Collection:
#     decks_collection = db.scooze_test[DbCollection.DECKS]
#     # decks_collection.insert_one(
#     #     deck_model_modern_4c.model_dump(
#     #         mode="json",
#     #         by_alias=True,
#     #     )
#     # )
#     return decks_collection


# @pytest.fixture
# def deck_model_modern_4c(
#     archetype_modern_4c: str,
#     main_modern_4c_dict: dict[ObjectId, int],
#     side_modern_4c_dict: dict[ObjectId, int],
#     today: datetime,
# ) -> DeckModelIn:
#     return DeckModelIn.model_validate(
#         {
#             "archetype": archetype_modern_4c,
#             "format": "modern",
#             "date_played": today,
#             "main": main_modern_4c_dict,
#             "side": side_modern_4c_dict,
#         }
#     )


# @pytest.fixture
# def main_modern_4c_dict(main_modern_4c: DeckPart[OracleCard], mock_cards_collection: Collection) -> dict[ObjectId, int]:
#     return {mock_cards_collection.find_one({"name": c.name})["_id"]: q for c, q in main_modern_4c.cards.items()}


# @pytest.fixture
# def side_modern_4c_dict(side_modern_4c: DeckPart[OracleCard], mock_cards_collection: Collection) -> dict[ObjectId, int]:
#     return {mock_cards_collection.find_one({"name": c.name})["_id"]: q for c, q in side_modern_4c.cards.items()}
