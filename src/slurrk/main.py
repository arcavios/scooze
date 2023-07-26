from fastapi import FastAPI
from slurrk.routers.card import router as CardRouter

app = FastAPI()


# Router inclusion
app.include_router(CardRouter)


@app.get("/")
def read_root():
    return {"Hello": "Glurg"}
