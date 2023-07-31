from fastapi import FastAPI
from slurrk.routers.card import router as CardRouter
from slurrk.routers.cards import router as CardsRouter

app = FastAPI()


# Router inclusion
app.include_router(CardRouter)
app.include_router(CardsRouter)


@app.get("/")
def read_root():
    return {"Hello": "Go to ./docs for the SwaggerAPI"}
