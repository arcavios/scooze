from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from slurrk.models.card import CardIn, CardOut

# region Motor and Mongo Setup

MONGO_URI = "mongodb://127.0.0.1:27017"
client = AsyncIOMotorClient(MONGO_URI)
database = client.slurrk

# Collections
cards_collection = database.get_collection("cards")

# endregion

# region Cards


async def add_card(card: CardIn) -> CardOut:
    # TODO: docstrings?
    insert_result = await cards_collection.insert_one(
        card.model_dump(
            mode="json",
            by_alias=True,
            exclude={"id"},
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
        {"$set": card.model_dump(mode="json", include=card.model_fields_set)},
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
