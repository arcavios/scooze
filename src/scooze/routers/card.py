from beanie import PydanticObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from scooze.models.card import CardModel, CardModelData

router = APIRouter(
    prefix="/card",
    tags=["card"],
    responses={404: {"description": "Card Not Found"}},
)


def _validate_card_id(card_id: str) -> PydanticObjectId:
    """
    Helper to validate incoming strings as Card IDs

    Args:
        card_id: Incoming string to test.

    Returns:
        Valid PydanticObjectId.

    Raises:
        HTTPException: 422 - String was not a valid id.
    """

    try:
        return PydanticObjectId(card_id)
    except InvalidId:
        raise HTTPException(status_code=422, detail="Must give a valid ID.")


@router.get("/", summary="Get a card at random")
async def card_root() -> CardModel:
    """
    Get a random card from the database.

    Returns:
        A random card from the database.

    Raises:
        HTTPException: 404 - No cards found in the database.
    """

    cards = await CardModel.aggregate([{"$sample": {"size": 1}}], projection_model=CardModel).to_list()

    if cards is None or len(cards) == 0:
        raise HTTPException(status_code=404, detail="No cards found in the database.")

    return cards[0]


# Create


@router.post("/add", summary="Create a new card")
async def add_card(card_data: CardModelData) -> CardModel:
    """
    Add a card to the database.

    Args:
        card_data: A dict conforming to CardModelData's schema.

    Returns:
        The created card.

    Raises:
        HTTPException: 400 - Create failed, passes along the error message.
    """

    try:
        # NOTE: would like to add the dupe protection back in
        card = CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True))
        return await card.create()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create a new card. Error: {e}")


# Read


@router.get("/id/{card_id}", summary="Get a card by ID")
async def get_card_by_id(card_id: PydanticObjectId = Depends(_validate_card_id)) -> CardModel:
    """
    Get the card with the given ID.

    Args:
        card_id: The ID of the card to get.

    Returns:
        The requested card.

    Raises:
        HTTPException: 404 - Card wasn't found.
        HTTPException: 422 - Bad ID given.
    """

    card = await CardModel.get(card_id)

    if card is None:
        raise HTTPException(status_code=404, detail=f"Card with ID {card_id} not found.")

    return card


@router.get("/name/{card_name}", summary="Get a card by name")
async def get_card_by_name(card_name: str) -> CardModel:
    """
    Get a card by its name.

    If more than 1 version of the card is present, returns the first one found.

    Args:
        card_name: The name of the card to get.

    Returns:
        The requested card.

    Raises:
        HTTPException: 404 - Card wasn't found.
    """

    card = await CardModel.find_one({"name": card_name})

    if card is None:
        raise HTTPException(status_code=404, detail=f"Card with name '{card_name}' not found.")

    return card


# Update


@router.patch("/update/{card_id}", summary="Update an existing card")
async def update_card(card_req: CardModel, card_id: PydanticObjectId = Depends(_validate_card_id)) -> CardModel:
    """
    Update an existing card with the given scooze ID and payload.

    Fields will be updated according to the given payload. If a field is not
    present in the payload, it will not be updated.

    Args:
        card_id: The ID of the card to update.
        card_req: The fields to update.

    Returns:
        The updated card.

    Raises:
        HTTPException: 404 - Card wasn't found, pre-update.
        HTTPException: 404 - Card wasn't found, post-update.
        HTTPException: 422 - Bad ID given.
    """

    field_updates = {k: v for k, v in card_req.dict().items() if v is not None}
    card = await CardModel.get(card_id)

    if card is None:
        raise HTTPException(status_code=404, detail=f"Card with ID {card_id} not found.")

    # NOTE: This could be slightly less verbose by chaining a la CardModel.get().update() but
    # the typing gets weird from things on Beanie's end so I broke it up like this
    _ = await card.set(field_updates)
    updated_card = await CardModel.get(card_id)

    if updated_card is None:
        raise HTTPException(status_code=404, detail=f"Card with ID {card_id} not found post-update.")

    return updated_card


# Delete


@router.delete("/delete/{card_id}", summary="Delete an existing card")
async def delete_card_by_id(card_id: PydanticObjectId = Depends(_validate_card_id)) -> JSONResponse:
    """
    Delete an existing card with the given ID.

    Args:
        card_id: The ID of the card to delete.

    Returns:
        A message that either the card was deleted or not deleted.

    Raises:
        HTTPException: 400 - Card wasn't deleted.
        HTTPException: 404 - Card wasn't found.
        HTTPException: 422 - Bad ID given.
    """

    card_to_delete = await CardModel.get(card_id)

    if card_to_delete is None:
        raise HTTPException(status_code=404, detail=f"Card with ID {card_id} not found.")

    delete_result = await card_to_delete.delete()

    if delete_result is None:
        raise HTTPException(status_code=400, detail=f"Card with ID {card_id} not deleted.")

    return JSONResponse(f"Card with ID {card_id} deleted.")
