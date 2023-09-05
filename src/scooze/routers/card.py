import scooze.database.card as db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from scooze.models.card import CardModelIn

router = APIRouter(
    prefix="/card",
    tags=["card"],
    responses={404: {"description": "Card Not Found"}},
)


@router.get("/")
async def card_root():
    cards = await db.get_cards_random(limit=1)
    if cards:
        card = cards[0]
        return JSONResponse(card.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": "No cards found in the database."}, status_code=404)


# Create


@router.post("/add")
async def add_card(card: CardModelIn):
    new_card = await db.add_card(card=card)
    if new_card:
        return JSONResponse(new_card.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Failed to create a new card."}, status_code=400)


# Read


@router.get("/id/{id}")
async def get_card_by_id(card_id: str):
    card = await db.get_card_by_property(property_name="_id", value=card_id)
    if card:
        return JSONResponse(card.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Card with id {card_id} not found."}, status_code=404)


@router.get("/name/{card_name}")
async def get_card_by_name(card_name: str):
    card = await db.get_card_by_property(property_name="name", value=card_name)
    if card:
        return JSONResponse(card.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Card with name {card_name} not found."}, status_code=404)


# Update


@router.patch("/update/{card_id}")
async def update_card(card_id: str, card: CardModelIn):
    updated_card = await db.update_card(id=card_id, card=card)

    if updated_card:
        return JSONResponse(updated_card.model_dump(mode="json"), status_code=200)
    else:
        # NOTE: in this setup, there isn't a way to distinguish between actually
        # changing a value and finding something but not changing.
        return JSONResponse({"message": f"Card with id {card_id} not updated."}, status_code=400)


# Delete


@router.delete("/delete/{card_id}")
async def delete_card_by_id(card_id: str):
    deleted_card = await db.delete_card(id=card_id)

    if deleted_card:
        return JSONResponse({"message": f"Card with id {card_id} deleted."}, status_code=200)
    else:
        return JSONResponse({"message": f"Card with id {card_id} not deleted."}, status_code=404)
