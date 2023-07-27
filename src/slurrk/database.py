from motor.motor_asyncio import AsyncIOMotorClient
from slurrk.models.card import Card

# region Motor and Mongo Setup

MONGO_URI = "mongodb://127.0.0.1:27017"
client = AsyncIOMotorClient(MONGO_URI)
database = client.slurrk

# Collections
cards_collection = database.get_collection("cards")

# endregion

# region Cards


async def add_card(card: Card) -> Card:
    c = await cards_collection.insert_one(card.model_dump(mode="json"))
    new_card = await cards_collection.find_one({"_id": c.inserted_id})
    if new_card:
        return Card.model_validate(new_card)


async def get_card_by_property(property_name: str, value) -> Card:
    card = await cards_collection.find_one({property_name: value})
    if card:
        return Card.model_validate(card)

async def update_card(id: str, card: Card) -> bool:
    # Return false if an empty request body is sent.
    if not card:
        return False
    c = await cards_collection.find_one({"_id": id})
    if c:
        updated_card = await cards_collection.update_one({"_id": id}, {"$set": card.model_dump(mode="json")},)
        if updated_card:
            return True
    return False


# endregion
