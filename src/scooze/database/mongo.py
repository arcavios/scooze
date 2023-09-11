from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_URI = "mongodb://127.0.0.1:27017"


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def mongo_connect():
    db.client = AsyncIOMotorClient(MONGO_URI)


async def mongo_close():
    db.client.close()
