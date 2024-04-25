from http import HTTPStatus
from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from scooze.models.deck import DeckModel, DeckModelData
from scooze.utils import to_lower_camel

router = APIRouter(
    prefix="/decks",
    tags=["decks"],
    responses={HTTPStatus.NOT_FOUND: {"description": "Decks Not Found"}},
)


@router.get("/", summary="Get decks at random")
async def decks_root(limit: int = 3) -> list[DeckModel]:
    """
    Get random decks from the database.

    Args:
        limit: The maximum number of decks to get.

    Returns:
        Random decks from the database.

    Raises:
        HTTPException: 404 - No decks found in the database.
    """

    decks = await DeckModel.aggregate([{"$sample": {"size": limit}}], projection_model=DeckModel).to_list()

    if decks is None or not decks:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No decks found in the database.")

    return decks


# Create


@router.post("/add", summary="Create new decks")
async def add_decks(decks: list[DeckModelData]) -> JSONResponse:
    """
    Add a list of decks to the database.

    Args:
        decks: A list of dicts conforming to DeckModelData's schema.

    Returns:
        A message stating how many decks were created.

    Raises:
        HTTPException: 400 - Create failed, passes along the error message.
    """

    try:
        decks_to_insert = [DeckModel.model_validate(deck.model_dump()) for deck in decks]
        insert_result = await DeckModel.insert_many(decks_to_insert)
        return JSONResponse(f"Created {len(insert_result.inserted_ids)} deck(s).")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Failed to create new decks.")


@router.post("/by", summary="Get decks by property")
async def get_decks_by(
    property_name: str,
    values: list[Any],
    paginated: bool = False,
    page: int = 1,
    page_size: int = 10,
) -> list[DeckModel]:
    """
    Get decks where the given property matches any of the given values.

    Args:
        property_name: The property to check against.
        values: Matching values of the given property.
        paginated: Return paginated results if True, or all matches if False.
        page: The page to return matches from.
        page_size: The number of results per page.

    Returns:
        A list of decks matching the search criteria.

    Raises:
        HTTPException: 404 - Decks weren't found.
    """

    match property_name:
        case "_id" | "id":
            prop_name = "_id"
            vals = [PydanticObjectId(v) for v in values]  # Normalize Mongo IDs
        case _:
            prop_name = to_lower_camel(property_name)
            vals = values

    skip = (page - 1) * page_size if paginated else 0
    limit = page_size if paginated else None
    decks = await DeckModel.find({"$or": [{prop_name: v} for v in vals]}, skip=skip, limit=limit).to_list()

    if len(decks) == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Decks not found.")

    return decks


# Delete


@router.delete("/delete/all", summary="Delete all decks")
async def delete_decks_all() -> JSONResponse:
    """
    Deletes all decks in the database.

    Returns:
        A message that the decks were deleted.

    Raises:
        HTTPException: 400 - Decks weren't deleted.
    """

    delete_result = await DeckModel.delete_all()

    if delete_result is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Decks weren't deleted.")

    return JSONResponse(f"Deleted {delete_result.deleted_count} deck(s).")
