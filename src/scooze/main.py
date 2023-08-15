from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from scooze.routers.card import router as CardRouter
from scooze.routers.cards import router as CardsRouter

app = FastAPI(
    title="scooze",
    summary="REST API for interacting with MongoDB for Magic: the Gathering tournaments, decklists, and cards.",
)


# Router inclusion
app.include_router(CardRouter)
app.include_router(CardsRouter)

# Mount index.html
app.mount("/", StaticFiles(directory="static", html=True), name="static")
