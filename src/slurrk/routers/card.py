import slurrk.database as db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from slurrk.models.card import Card

router = APIRouter(
    prefix="/card",
    tags=["card"],
    responses={404: {"description": "Card Not Found"}},
)


@router.get("/")
def card_root():
    # TODO: return a random card
    return {"Documentation": f"{router.docs_url}"}


# Create


@router.post("/add")
async def add_card(card: Card):
    new_card = await db.add_card(card=card)
    if new_card:
        return JSONResponse({"card": new_card.model_dump(mode="json")})
    else:
        return JSONResponse({"card": f"Failed to create a new card."})


# Read


@router.get("/id/{id}")
async def get_card_by_id(id: str):
    card = await db.get_card_by_property(property_name="id", value=id)
    if card:
        return JSONResponse({"card": card.model_dump(mode="json")})
    else:
        return JSONResponse({"card": f"Card with id {id} not found."})


@router.get("/oracle_id/{oracle_id}")
async def get_card_by_oracle_id(oracle_id: str):
    card = await db.get_card_by_property(property_name="oracle_id", value=oracle_id)
    if card:
        return JSONResponse({"card": card.model_dump(mode="json")})
    else:
        return JSONResponse({"card": f"Card with oracle_id {oracle_id} not found."})


@router.get("/name/{card_name}")
async def get_card_by_name(card_name: str):
    card = await db.get_card_by_property(property_name="name", value=card_name)
    if card:
        return JSONResponse({"card": card.model_dump(mode="json")})
    else:
        return JSONResponse({"card": f"Card with name {card_name} not found."})


# Update


@router.patch("/update/{card_id}")
def update_card(card_id: str, card: Card):
    updated = db.update_card_by_id
    return {
        "card.name": card.name,
        "card.color": card.color,
    }


# Delete


@router.delete("/{card_id}")
def delete_card_by_id(card_id):
    # TODO: delete card
    return {"Deleted card id": card_id}
