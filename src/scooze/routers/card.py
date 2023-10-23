from beanie import PydanticObjectId
from bson.errors import InvalidId
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from scooze.models.card import CardModel

router = APIRouter(
    prefix="/card",
    tags=["card"],
    responses={404: {"description": "Card Not Found"}},
)


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

    if cards is None:
        raise HTTPException(status_code=404, detail="No cards found in the database.")

    return cards[0]


# Create


@router.post("/add", summary="Create a new card")
async def add_card(card: CardModel) -> CardModel:
    """
    Add a card to the database.

    Returns:
        The created card.

    Raises:
        HTTPException: 400 - Create failed, passes along the error message.
    """

    try:
        # NOTE: would like to add the dupe protection back in
        return await card.create()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create a new card. Error: {e}")


# Read


@router.get("/id/{card_id}", summary="Get a card by ID")
async def get_card_by_id(card_id: str) -> CardModel:
    """
    Get the card with the given ID.

    Args:
        card_id: The ID of the card to get.

    Returns:
        The requested card.

    Raises:
        HTTPException: 400 - Bad id given.
        HTTPException: 404 - Card wasn't found.
    """
    try:
        card_obj_id = PydanticObjectId(card_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Must give a valid id.")

    card = await CardModel.get(card_obj_id)

    if card is None:
        raise HTTPException(status_code=404, detail=f"Card with id {card_obj_id} not found.")

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
        raise HTTPException(status_code=404, detail=f"Card with name {card_name} not found.")

    return card


# Update


@router.patch("/update/{card_id}", summary="Update an existing card")
async def update_card(card_id: str, card_req: CardModel) -> CardModel:
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
        HTTPException: 400 - Bad id given.
        HTTPException: 404 - Card wasn't found, pre-update.
        HTTPException: 404 - Card wasn't found, post-update.
    """

    try:
        card_obj_id = PydanticObjectId(card_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Must give a valid id.")

    field_updates = {k: v for k, v in card_req.dict().items() if v is not None}
    card = await CardModel.get(card_obj_id)

    if card is None:
        raise HTTPException(status_code=404, detail=f"Card with id {card_obj_id} not found.")

    # NOTE: This could be slightly less verbose by chaining a la CardModel.get().update() but
    # the typing gets weird from things on Beanie's end so I broke it up like this
    _ = await card.set(field_updates)
    updated_card = await CardModel.get(card_obj_id)

    if updated_card is None:
        raise HTTPException(status_code=404, detail=f"Card with id {card_obj_id} not found post-update.")

    return updated_card


# Delete


@router.delete("/delete/{card_id}", summary="Delete an existing card")
async def delete_card_by_id(card_id: str) -> JSONResponse:
    """
    Delete an existing card with the given ID.

    Args:
        card_id: The ID of the card to delete.

    Returns:
        A message that either the card was deleted or not deleted.

    Raises:
        HTTPException: 400 - Bad id given.
        HTTPException: 400 - Card wasn't deleted.
        HTTPException: 404 - Card wasn't found.
    """

    try:
        card_obj_id = PydanticObjectId(card_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Must give a valid id.")

    card_to_delete = await CardModel.get(card_obj_id)

    if card_to_delete is None:
        raise HTTPException(status_code=404, detail=f"Card with id {card_obj_id} not found.")

    delete_result = await card_to_delete.delete()

    if delete_result is None:
        raise HTTPException(status_code=400, detail=f"Card with id {card_obj_id} not deleted.")

    return JSONResponse(f"Card with id {card_obj_id} deleted.")
