from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://127.0.0.1:27017"


class Database:
    """
    A simple database object to house the Motor client.

    Attributes:
        client: An AsyncIOMotorClient for managing Scooze's MongoDB connection.
    """

    client: AsyncIOMotorClient = None


db = Database()


async def mongo_connect():
    """
    Connect to the database client to MongoDB.
    """

    db.client = AsyncIOMotorClient(MONGO_URI)


async def mongo_close():
    """
    Close the database client's MongoDB connection.
    """

    db.client.close()
