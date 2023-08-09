from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from scooze.routers.card import router as CardRouter
from scooze.routers.cards import router as CardsRouter

app = FastAPI()


# Router inclusion
app.include_router(CardRouter)
app.include_router(CardsRouter)


@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')
