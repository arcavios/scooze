import scooze.database.card as db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from scooze.models.card import CardModelIn

router = APIRouter(
    prefix="/card",
    tags=["card"],
    responses={404: {"description": "Card Not Found"}},
)


@router.get("/", summary="Get a card at random")
async def card_root():
    cards = await db.get_cards_random(limit=1)
    if cards is not None:
        card = cards[0]
        return JSONResponse(card.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": "No cards found in the database."}, status_code=404)


# Create


@router.post("/add", summary="Create a new card")
async def add_card(card: CardModelIn):
    new_card = await db.add_card(card=card)
    if new_card is not None:
        return JSONResponse(new_card.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Failed to create a new card."}, status_code=400)


# Read


@router.get("/id/{card_id}", summary="Get a card by ID")
async def get_card_by_id(card_id: str):
    """
    Get the card with the given scooze ID.

    - **card_id** - the scooze ID of the card to get
    """

    card = await db.get_card_by_property(property_name="_id", value=card_id)
    if card is not None:
        return JSONResponse(card.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Card with id {card_id} not found."}, status_code=404)


@router.get("/name/{card_name}", summary="Get a card by name")
async def get_card_by_name(card_name: str):
    """
    Get a card by its name.

    If more than 1 version of the card is present, returns the first one found.

    - **card_name** - the name of the card to get
    """

    card = await db.get_card_by_property(property_name="name", value=card_name)
    if card is not None:
        return JSONResponse(card.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Card with name {card_name} not found."}, status_code=404)


# Update


@router.patch("/update/{card_id}", summary="Update an existing card")
async def update_card(card_id: str, card: CardModelIn):
    """
    Update an existing card with the given scooze ID and payload.

    Fields will be updated according to the given payload. If a field is not
    present in the payload, it will not be updated.

    - **card_id** - the scooze ID of the card to update
    """

    updated_card = await db.update_card(id=card_id, card=card)

    if updated_card is not None:
        return JSONResponse(updated_card.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Card with id {card_id} not found."}, status_code=404)


# Delete


@router.delete("/delete/{card_id}", summary="Delete an existing card")
async def delete_card_by_id(card_id: str):
    """
    Delete an existing card with the given scooze ID.

    - **card_id** - the scooze ID of the card to delete
    """

    deleted_card = await db.delete_card(id=card_id)

    if deleted_card is not None:
        return JSONResponse({"message": f"Card with id {card_id} deleted."}, status_code=200)
    else:
        return JSONResponse({"message": f"Card with id {card_id} not deleted."}, status_code=404)
