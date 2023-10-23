import os
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from scooze.models.card import CardModel
from scooze.routers.card import router as CardRouter
from scooze.routers.cards import router as CardsRouter
from scooze.routers.deck import router as DeckRouter
from scooze.routers.decks import router as DecksRouter

MONGO_URI = "mongodb://127.0.0.1:27017"


# Startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup Mongo and Beanie
    scooze_client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(database=scooze_client.scooze, document_models=[CardModel])

    # Yield to the app
    yield

    # Mongo teardown
    scooze_client.close()


app = FastAPI(
    title="scooze",
    summary="REST API for interacting with MongoDB for Magic: the Gathering tournaments, decklists, and cards.",
    lifespan=lifespan,
)


# Router inclusion
app.include_router(CardRouter)
app.include_router(CardsRouter)
app.include_router(DeckRouter)
app.include_router(DecksRouter)

# Mount index.html
app_dir = os.path.dirname(__file__)
static_dir = os.path.join(app_dir, "static/")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
