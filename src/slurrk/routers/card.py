import slurrk.database as db
from bson import ObjectId
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
        return JSONResponse({"card": f"Failed to create a new card."}, status_code=400)


# Read


@router.get("/id/{id}")
async def get_card_by_id(card_id: str):
    card = await db.get_card_by_property(property_name="_id", value=card_id)
    if card:
        return JSONResponse({"card": card.model_dump(mode="json")})
    else:
        return JSONResponse({"card": f"Card with id {card_id} not found."}, status_code=404)


@router.get("/oracle_id/{oracle_id}")
async def get_card_by_oracle_id(oracle_id: str):
    card = await db.get_card_by_property(property_name="oracle_id", value=oracle_id)
    if card:
        return JSONResponse({"card": card.model_dump(mode="json")})
    else:
        return JSONResponse({"card": f"Card with oracle_id {oracle_id} not found."}, status_code=404)


@router.get("/name/{card_name}")
async def get_card_by_name(card_name: str):
    card = await db.get_card_by_property(property_name="name", value=card_name)
    if card:
        return JSONResponse({"card": card.model_dump(mode="json")})
    else:
        return JSONResponse({"card": f"Card with name {card_name} not found."}, status_code=404)


# Update


@router.patch("/update/{card_id}")
async def update_card(card_id: str, card: Card):
    updated_card = await db.update_card(id=card_id, card=card)

    print(f"Updated card: {updated_card}")

    if updated_card:
        # TODO: along with all the rest, should this be update_card: "message"? or some other convention?
        return JSONResponse({"card": f"Card with id {card_id} updated."}, status_code=200)
    else:
        # TODO: NOTE: in this setup, there isn't a way to distinguish between actually
        # changing a value and finding something but not changing, do we care?
        return JSONResponse({"card": f"Card with id {card_id} not updated."}, status_code=400)


# Delete


@router.delete("/delete/{card_id}")
async def delete_card_by_id(card_id):
    deleted_card = await db.delete_card(id=card_id)

    if deleted_card:
        return JSONResponse({"card": f"Card with id {card_id} deleted."}, status_code=200)
    else:
        return JSONResponse({"card": f"Card with id {card_id} not deleted."}, status_code=404)
