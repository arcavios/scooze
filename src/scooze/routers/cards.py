from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from scooze.models.card import CardModel, CardModelData
from scooze.utils import to_lower_camel

router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    responses={404: {"description": "Cards Not Found"}},
)


@router.get("/", summary="Get cards at random")
async def cards_root(limit: int = 3) -> list[CardModel]:
    """
    Get a random card from the database.

    Args:
        limit: The maximum number of cards to get.

    Returns:
        Random cards from the database.

    Raises:
        HTTPException: 404 - No cards found in the database.
    """

    cards = await CardModel.aggregate([{"$sample": {"size": limit}}], projection_model=CardModel).to_list()

    if cards is None or len(cards) == 0:
        raise HTTPException(status_code=404, detail="No cards found in the database.")

    return cards


# Create


@router.post("/add", summary="Create new cards")
async def add_cards(cards: list[CardModelData]) -> JSONResponse:
    """
    Add a list of cards to the database.

    Args:
        cards: A list of dicts conforming to CardModelData's schema.

    Returns:
        A message stating how many cards were created.

    Raises:
        HTTPException: 400 - Create failed, passes along the error message.
    """

    try:
        cards_to_insert = [CardModel.model_validate(card.model_dump(mode="json", by_alias=True)) for card in cards]
        insert_result = await CardModel.insert_many(cards_to_insert)
        return JSONResponse(f"Created {len(insert_result.inserted_ids)} card(s).")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create new cards. Error: {e}")


# Read


@router.post("/by", summary="Get cards by property")
async def get_cards_by(
    property_name: str,
    values: list[Any],
    paginated: bool = False,
    page: int = 1,
    page_size: int = 10,
) -> list[CardModel]:
    """
    Get cards where the given property matches any of the given values.

    Args:
        property_name: The property to check against.
        values: Matching values for the given property
        paginated: Return paginated results if True, or all matches if False
        page: The page to return matches from.
        page_size: The number of results per page.

    Returns:
        A list of cards matching the search criteria.

    Raises:
        HTTPException: 404 - Cards weren't found.
    """

    match property_name:
        case "_id" | "id":
            prop_name = "_id"
            vals = [PydanticObjectId(v) for v in values]  # Normalize Mongo ids
        case _:
            prop_name = to_lower_camel(property_name)
            vals = values

    skip = (page - 1) * page_size if paginated else 0
    limit = page_size if paginated else None
    cards = await CardModel.find({"$or": [{prop_name: v} for v in vals]}, skip=skip, limit=limit).to_list()

    if len(cards) == 0:
        raise HTTPException(status_code=404, detail="Cards not found.")

    return cards


# Delete


@router.delete("/delete/all", summary="Delete all cards")
async def delete_cards_all() -> JSONResponse:
    """
    Deletes all cards in the database.

    Returns:
        A message that the cards were deleted.

    Raises:
        HTTPException: 400 - Cards weren't deleted.
    """

    delete_result = await CardModel.delete_all()

    if delete_result is None:
        raise HTTPException(status_code=400, detail="Cards weren't deleted.")

    return JSONResponse(f"Deleted {delete_result.deleted_count} card(s).")
