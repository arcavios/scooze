from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from pymongo.results import DeleteResult, InsertManyResult
from scooze.models.card import CardModelIn, CardModelOut
from scooze.models.deck import DeckModelIn, DeckModelOut

# region Motor and Mongo Setup

MONGO_URI = "mongodb://127.0.0.1:27017"
client = AsyncIOMotorClient(MONGO_URI)
database = client.scooze

# Collections
cards_collection = database.get_collection("cards")
decks_collection = database.get_collection("decks")

# endregion

# region Card


async def add_card(card: CardModelIn) -> CardModelOut:
    # TODO(#45): router docstrings
    insert_result = await cards_collection.insert_one(
        card.model_dump(
            mode="json",
            by_alias=True,
        )
    )
    new_card = await cards_collection.find_one({"_id": insert_result.inserted_id})
    if new_card:
        return CardModelOut(**new_card)


async def get_card_by_property(property_name: str, value) -> CardModelOut:
    # TODO(#45): router docstrings
    if property_name == "_id":
        value = ObjectId(value)
    card = await cards_collection.find_one({property_name: value})
    if card:
        return CardModelOut(**card)


async def update_card(id: str, card: CardModelIn) -> CardModelOut:
    # TODO(#45): router docstrings
    # Return false if an empty request body is sent.
    if not card.model_fields_set:
        raise ValueError(f"No data given, skipping update for Card with id: {id}")
    updated_card = await cards_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {
            "$set": card.model_dump(
                mode="json",
                by_alias=True,
                include=card.model_fields_set,
            )
        },
        return_document=ReturnDocument.AFTER,
    )
    if updated_card:
        return CardModelOut(**updated_card)


async def delete_card(id: str) -> CardModelOut:
    # TODO(#45): router docstrings
    deleted_card = await cards_collection.find_one_and_delete({"_id": ObjectId(id)})

    if deleted_card:
        return CardModelOut(**deleted_card)


# endregion

# region Cards


async def add_cards(cards: list[CardModelIn]) -> InsertManyResult:
    # TODO(#45): router docstrings
    insert_many_result = await cards_collection.insert_many(
        [
            card.model_dump(
                mode="json",
                by_alias=True,
            )
            for card in cards
        ]
    )
    if insert_many_result:
        return insert_many_result


async def get_cards_random(limit: int) -> list[CardModelOut]:
    # TODO(#45): router docstrings
    pipeline = [{"$sample": {"size": limit}}]
    cards = await cards_collection.aggregate(pipeline).to_list(limit)
    if len(cards) > 0:
        return [CardModelOut(**card) for card in cards]


async def get_cards_by_property(
    property_name: str, items: list[Any], paginated: bool = True, page: int = 1, page_size: int = 10
) -> list[CardModelOut]:
    # TODO(#45): router docstrings
    match property_name:
        case "_id":
            values = [ObjectId(i) for i in items]  # Handle ObjectIds
        case _:
            values = [i for i in items]

    cards = (
        await cards_collection.find({"$or": [{property_name: v} for v in values]})
        .skip((page - 1) * page_size if paginated else 0)
        .to_list(page_size if paginated else None)
    )

    if len(cards) > 0:
        return [CardModelOut(**card) for card in cards]


async def delete_cards_all() -> DeleteResult:
    # TODO(#45): router docstrings
    delete_many_result = await cards_collection.delete_many({})  # NOTE: This deletes the entire collection.
    if delete_many_result:
        return delete_many_result


# endregion

# region Deck


async def add_deck(deck: DeckModelIn) -> DeckModelOut:
    # TODO(#45): router docstrings
    insert_result = await decks_collection.insert_one(
        deck.model_dump(
            mode="json",
            by_alias=True,
        )
    )
    new_deck = await decks_collection.find_one({"_id": insert_result.inserted_id})
    if new_deck:
        return DeckModelOut(**new_deck)


async def get_deck_by_property(property_name: str, value) -> DeckModelOut:
    # TODO(#45): router docstrings
    if property_name == "_id":
        value = ObjectId(value)
    deck = await decks_collection.find_one({property_name: value})
    if deck:
        return DeckModelOut(**deck)


async def update_deck(id: str, deck: DeckModelIn) -> DeckModelOut:
    # TODO(#45): router docstrings
    # Return false if an empty request body is sent.
    if not deck.model_fields_set:
        raise ValueError(f"No data given, skipping update for Deck with id: {id}")
    updated_deck = await decks_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {
            "$set": deck.model_dump(
                mode="json",
                by_alias=True,
                include=deck.model_fields_set,
            )
        },
        return_document=ReturnDocument.AFTER,
    )
    if updated_deck:
        return DeckModelOut(**updated_deck)


async def delete_deck(id: str) -> DeckModelOut:
    # TODO(#45): router docstrings
    deleted_deck = await decks_collection.find_one_and_delete({"_id": ObjectId(id)})

    if deleted_deck:
        return DeckModelOut(**deleted_deck)


# endregion
