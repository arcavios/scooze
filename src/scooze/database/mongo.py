from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# TODO(#119): database docstrings

MONGO_URI = "mongodb://127.0.0.1:27017"


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def mongo_connect():
    db.client = AsyncIOMotorClient(MONGO_URI)


async def mongo_close():
    db.client.close()
