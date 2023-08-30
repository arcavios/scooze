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

SCOOZE_COLLECTIONS = {
    "card": cards_collection,
    "deck": decks_collection,
}

# endregion

# region Common/Helpers


def _get_scooze_collection(doc_type: str):
    if doc_type in SCOOZE_COLLECTIONS:
        return SCOOZE_COLLECTIONS[doc_type]
    else:
        raise ValueError(f"No collection found for {doc_type.title}")


async def _insert_document(doc_type: str, document: dict[str, Any]):
    current_collection = _get_scooze_collection(doc_type)
    insert_result = await current_collection.insert_one(document)
    return await current_collection.find_one({"_id": insert_result.inserted_id})


async def _get_document_by_property(doc_type: str, property_name: str, value):
    current_collection = _get_scooze_collection(doc_type)
    if property_name == "_id":
        value = ObjectId(value)
    return await current_collection.find_one({property_name: value})


async def _update_document(doc_type: str, id: str, document: dict[str, Any]):
    if len(document) == 0:
        raise ValueError(f"No data given, skipping update for {doc_type.title} with id: {id}")
    current_collection = _get_scooze_collection(doc_type)
    return await current_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": document},
        return_document=ReturnDocument.AFTER,
    )


async def _delete_document(doc_type: str, id: str):
    current_collection = _get_scooze_collection(doc_type)
    return await current_collection.find_one_and_delete({"_id": ObjectId(id)})


# endregion


# region Card


async def add_card(card: CardModelIn) -> CardModelOut:
    # TODO(#45): router docstrings
    new_card = await _insert_document(
        "card",
        card.model_dump(
            mode="json",
            by_alias=True,
        ),
    )
    if new_card:
        return CardModelOut(**new_card)


async def get_card_by_property(property_name: str, value) -> CardModelOut:
    # TODO(#45): router docstrings
    card = await _get_document_by_property("card", property_name, value)
    if card:
        return CardModelOut(**card)


async def update_card(id: str, card: CardModelIn) -> CardModelOut:
    # TODO(#45): router docstrings
    updated_card = await _update_document(
        "card",
        id,
        card.model_dump(
            mode="json",
            by_alias=True,
            include=card.model_fields_set,
        ),
    )
    if updated_card:
        return CardModelOut(**updated_card)


async def delete_card(id: str) -> CardModelOut:
    # TODO(#45): router docstrings
    deleted_card = await _delete_document("card", id)

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
    new_deck = await _insert_document(
        "deck",
        deck.model_dump(
            mode="json",
            by_alias=True,
        ),
    )
    if new_deck:
        return DeckModelOut(**new_deck)


async def get_deck_by_property(property_name: str, value) -> DeckModelOut:
    # TODO(#45): router docstrings
    deck = await _get_document_by_property("deck", property_name, value)
    if deck:
        return DeckModelOut(**deck)


async def update_deck(id: str, deck: DeckModelIn) -> DeckModelOut:
    # TODO(#45): router docstrings
    updated_deck = await _update_document(
        "deck",
        id,
        deck.model_dump(
            mode="json",
            by_alias=True,
            include=deck.model_fields_set,
        ),
    )

    if updated_deck:
        return DeckModelOut(**updated_deck)


async def delete_deck(id: str) -> DeckModelOut:
    # TODO(#45): router docstrings
    deleted_deck = await _delete_document("deck", id)

    if deleted_deck:
        return DeckModelOut(**deleted_deck)


# endregion

# region Decks


async def add_decks(decks: list[DeckModelIn]) -> InsertManyResult:
    # TODO(#45): router docstrings
    insert_many_result = await decks_collection.insert_many(
        [
            deck.model_dump(
                mode="json",
                by_alias=True,
            )
            for deck in decks
        ]
    )
    if insert_many_result:
        return insert_many_result


async def get_decks_by_property(
    property_name: str, items: list[Any], paginated: bool = True, page: int = 1, page_size: int = 10
) -> list[DeckModelOut]:
    # TODO(#45): router docstrings
    match property_name:
        case "_id":
            values = [ObjectId(i) for i in items]  # Handle ObjectIds
        case _:
            values = [i for i in items]

    decks = (
        await decks_collection.find({"$or": [{property_name: v} for v in values]})
        .skip((page - 1) * page_size if paginated else 0)
        .to_list(page_size if paginated else None)
    )

    if len(decks) > 0:
        return [DeckModelOut(**deck) for deck in decks]


async def delete_decks_all() -> DeleteResult:
    # TODO(#45): router docstrings
    delete_many_result = await decks_collection.delete_many({})  # NOTE: This deletes the entire collection.
    if delete_many_result:
        return delete_many_result


# endregion
