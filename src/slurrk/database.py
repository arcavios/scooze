from typing import Any, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from pymongo.results import DeleteResult, InsertManyResult
from slurrk.models.card import CardIn, CardOut

# region Motor and Mongo Setup

MONGO_URI = "mongodb://127.0.0.1:27017"
client = AsyncIOMotorClient(MONGO_URI)
database = client.slurrk

# Collections
cards_collection = database.get_collection("cards")

# endregion

# region Card


async def add_card(card: CardIn) -> CardOut:
    # TODO: docstrings?
    insert_result = await cards_collection.insert_one(
        card.model_dump(
            mode="json",
            by_alias=True,
        )
    )
    new_card = await cards_collection.find_one({"_id": insert_result.inserted_id})
    if new_card:
        return CardOut(**new_card)


async def get_card_by_property(property_name: str, value) -> CardOut:
    # TODO: docstrings?
    if property_name == "_id":
        value = ObjectId(value)
    card = await cards_collection.find_one({property_name: value})
    if card:
        return CardOut(**card)


async def update_card(id: str, card: CardIn) -> CardOut:
    # TODO: docstrings?
    # Return false if an empty request body is sent.
    if not card.model_fields_set:
        raise ValueError  # TODO: empty body, what do?
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
        return CardOut(**updated_card)


async def delete_card(id: str) -> CardOut:
    # TODO: docstrings?
    deleted_card = await cards_collection.find_one_and_delete({"_id": ObjectId(id)})

    if deleted_card:
        return CardOut(**deleted_card)


# endregion

# region Cards


async def add_cards(cards: List[CardIn]) -> InsertManyResult:
    # TODO: docstrings?
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


## TODO: get_cards()


async def get_cards_random(limit: int) -> List[CardOut]:
    # TODO: docstring?
    pipeline = [{"$sample": {"size": limit}}]
    cards = await cards_collection.aggregate(pipeline).to_list(limit)
    if len(cards) > 0:
        return [CardOut(**card) for card in cards]


async def get_cards_by_property(
    property_name: str, items: List[Any], paginated: bool = True, page: int = 1, page_size: int = 10
) -> List[CardOut]:
    # TODO: docstrings?
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
        return [CardOut(**card) for card in cards]


async def delete_cards_all() -> DeleteResult:
    delete_many_result = await cards_collection.delete_many({})  # NOTE: This deletes the entire collection.
    if delete_many_result:
        return delete_many_result


# endregion
