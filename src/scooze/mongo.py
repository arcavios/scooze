from motor.motor_asyncio import AsyncIOMotorClient
from scooze.config import CONFIG


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

    db.client = AsyncIOMotorClient(CONFIG.mongo_dsn)


async def mongo_close():
    """
    Close the database client's MongoDB connection.
    """

    db.client.close()
