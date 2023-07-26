from fastapi import FastAPI

from .routers import card

app = FastAPI()


# Router inclusion
app.include_router(card.router)


@app.get("/")
def read_root():
    return {"Hello": "Glurg"}
