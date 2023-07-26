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


async def get_card_by_property(property_name: str, value) -> Card:
    card = await cards_collection.find_one({property_name: value})
    if card:
        return Card.model_validate(card)


# endregion
