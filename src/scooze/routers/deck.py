from http import HTTPStatus

from beanie import PydanticObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from scooze.models.deck import DeckModel, DeckModelData

router = APIRouter(
    prefix="/deck",
    tags=["deck"],
    responses={HTTPStatus.NOT_FOUND: {"description": "Deck Not Found"}},
)


def _validate_deck_id(deck_id: str) -> PydanticObjectId:
    """
    Helper to validate incoming strings as Deck IDs.

    Args:
        deck_id: Incoming string to test.

    Returns:
        Valid PydanticObjectId.

    Raises:
        HTTPException: 422 - String was not a valid id.
    """

    try:
        return PydanticObjectId(deck_id)
    except InvalidId:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Must give a valid ID.")


@router.get("/", summary="Get a deck at random")
async def deck_root() -> DeckModel:
    """
    Get a random deck from the database.

    Returns:
        A random deck from the database.

    Raises:
        HTTPException: 404 - No decks found in the database.
    """

    decks = await DeckModel.aggregate([{"$sample": {"size": 1}}], projection_model=DeckModel).to_list()

    if decks is None or not decks:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No decks found in the database.")

    return decks[0]


# Create


@router.post("/add", summary="Create a new deck")
async def add_deck(deck_data: DeckModelData) -> DeckModel:
    """
    Add a deck to the database.

    Args:
        deck_data: A dict conforming to DeckModelData's schema.

    Returns:
        The created deck.

    Raises:
        HTTPException: 400 - Create failed, passes along the error message.
    """

    try:
        # NOTE: would like to add the dupe protection back in
        deck = DeckModel.model_validate(deck_data.model_dump())
        return await deck.create()
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Failed to create a new deck. Error: {e}")


# Read


@router.get("/id/{deck_id}", summary="Get a deck by ID")
async def get_deck_by_id(deck_id: PydanticObjectId = Depends(_validate_deck_id)) -> DeckModel:
    """
    Get the deck with the given ID.

    Args:
        deck_id: The ID of the deck to get

    Returns:
        The requested deck.

    Raises:
        HTTPException: 404 - Deck wasn't found.
        HTTPException: 422 - Bad ID given.
    """

    deck = await DeckModel.get(deck_id)

    if deck is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Deck with ID {deck_id} not found.")

    return deck


# Update


@router.patch("/update/{deck_id}", summary="Update an existing deck")
async def update_deck(deck_req: DeckModel, deck_id: PydanticObjectId = Depends(_validate_deck_id)) -> DeckModel:
    """
    Update an existing deck with the given scooze ID and payload.

    Fields will be updated according to the given payload. If a field is not
    present in the payload, it will not be updated.

    Args:
        deck_id: The ID of the deck to update.
        deck_req: The fields to update.

    Returns:
        The updated deck.

    Raises:
        HTTPException: 404 - Deck wasn't found, pre-update.
        HTTPException: 404 - Deck wasn't found, post-update.
        HTTPException: 422 - Bad ID given.
    """

    field_updates = {k: v for k, v in deck_req.model_dump().items() if v is not None}
    deck = await DeckModel.get(deck_id)

    if deck is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Deck with ID {deck_id} not found.")

    _ = await deck.set(field_updates)
    updated_deck = await DeckModel.get(deck_id)

    if updated_deck is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Deck with ID {deck_id} not found.")

    return updated_deck


# Delete


@router.delete("/delete/{deck_id}", summary="Delete an existing deck")
async def delete_deck_by_id(deck_id: PydanticObjectId = Depends(_validate_deck_id)) -> JSONResponse:
    """
    Delete an existing deck with the given scooze ID.

    Args:
        deck_id: The ID of the deck to delete.

    Returns:
        A message that either the deck was deleted or not deleted.

    Raises:
        HTTPException: 400 - Deck wasn't deleted.
        HTTPException: 404 - Deck wasn't found.
        HTTPException: 422 - Bad ID given.
    """

    deck_to_delete = await DeckModel.get(deck_id)

    if deck_to_delete is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Deck with ID {deck_id} not found.")

    delete_result = await deck_to_delete.delete()

    if delete_result is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Deck with ID {deck_id} not deleted.")

    return JSONResponse(f"Deck with ID {deck_id} deleted.")
