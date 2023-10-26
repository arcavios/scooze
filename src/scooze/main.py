import os
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from scooze.config import CONFIG
from scooze.models.card import CardModel
from scooze.mongo import db, mongo_close, mongo_connect
from scooze.routers.card import router as CardRouter
from scooze.routers.cards import router as CardsRouter
from scooze.routers.deck import router as DeckRouter
from scooze.routers.decks import router as DecksRouter


# Startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup Mongo and Beanie
    await mongo_connect()
    await init_beanie(database=db.client[CONFIG.mongo_db], document_models=[CardModel])

    # Yield to the app
    yield

    # Mongo teardown
    await mongo_close()


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
