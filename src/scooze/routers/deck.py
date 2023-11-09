import scooze.database.deck as db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from scooze.models.deck import DeckModelIn

router = APIRouter(
    prefix="/deck",
    tags=["deck"],
    responses={404: {"description": "Deck Not Found"}},
)


@router.get("/", summary="Get a deck at random")
async def deck_root():
    decks = await db.get_decks_random(limit=1)
    if decks is not None:
        deck = decks[0]
        return JSONResponse(deck.model_dump(mode="json"), status_code=200)


# Create


@router.post("/add", summary="Create a new deck")
async def add_deck(deck: DeckModelIn):
    new_deck = await db.add_deck(deck=deck)
    if new_deck is not None:
        return JSONResponse(new_deck.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Failed to create a new deck."}, status_code=400)


# Read


@router.get("/id/{deck_id}", summary="Get a deck by ID")
async def get_deck_by_id(deck_id: str):
    """
    Get the deck with the given scooze ID.

    - **deck_id** - the scooze ID of the deck to get
    """

    deck = await db.get_deck_by_property(property_name="_id", value=deck_id)
    if deck is not None:
        return JSONResponse(deck.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Deck with id {deck_id} not found."}, status_code=404)


# Update


@router.patch("/update/{deck_id}", summary="Update an existing deck")
async def update_deck(deck_id: str, deck: DeckModelIn):
    """
    Update an existing deck with the given scooze ID and payload.

    Fields will be updated according to the given payload. If a field is not
    present in the payload, it will not be updated.

    - **deck_id** - the scooze ID of the deck to update
    """

    updated_deck = await db.update_deck(id=deck_id, deck=deck)

    if updated_deck is not None:
        return JSONResponse(updated_deck.model_dump(mode="json"), status_code=200)
    else:
        return JSONResponse({"message": f"Deck with id {deck_id} not found."}, status_code=404)


# Delete


@router.delete("/delete/{deck_id}", summary="Delete an existing deck")
async def delete_deck_by_id(deck_id: str):
    """
    Delete an existing deck with the given scooze ID.

    - **deck_id** - the scooze ID of the deck to delete
    """

    deleted_deck = await db.delete_deck(id=deck_id)

    if deleted_deck is not None:
        return JSONResponse({"message": f"Deck with id {deck_id} deleted."}, status_code=200)
    else:
        return JSONResponse({"message": f"Deck with id {deck_id} not deleted."}, status_code=400)
