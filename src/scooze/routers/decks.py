from typing import Any

import scooze.database.deck as db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from scooze.models.deck import DeckModelIn

router = APIRouter(
    prefix="/decks",
    tags=["decks"],
    responses={404: {"description": "Decks Not Found"}},
)


@router.get("/", summary="Get decks at random")
async def decks_root(limit: int = 3):
    """
    Get random decks up to the given limit.

    - **limit** - the maximum number of decks to get
    """

    decks = await db.get_decks_random(limit=limit)
    if decks is not None:
        return JSONResponse([deck.model_dump(mode="json") for deck in decks], status_code=200)
    else:
        return JSONResponse({"message": "No decks found in the database."}, status_code=404)


# Create


@router.post("/add", summary="Create new decks")
async def add_decks(decks: list[DeckModelIn]):
    inserted_ids = await db.add_decks(decks=decks)
    if inserted_ids is not None:
        return JSONResponse({"message": f"Created {len(inserted_ids)} deck(s)."}, status_code=200)
    else:
        return JSONResponse({"message": "Failed to create any new decks."}, status_code=400)


@router.post("/by", summary="Get decks by property")
async def get_decks_by(
    property_name: str, values: list[Any], paginated: bool = False, page: int = 1, page_size: int = 10
):
    """
    Get decks where the given property matches any of the given values.

    - **property_name** - the property to check against
    - **values** - matching values of the given property
    - **paginated** - return paginated results if True, return all matches if
    False
    - **page** - return matches from the given page
    - **page_size** - the number of results per page
    """

    decks = await db.get_decks_by_property(
        property_name=property_name, values=values, paginated=paginated, page=page, page_size=page_size
    )
    if decks is not None:
        return JSONResponse([deck.model_dump(mode="json") for deck in decks], status_code=200)
    else:
        return JSONResponse({"message": "Decks not found."}, status_code=404)


# Delete


@router.delete("/delete/all", summary="Delete all decks")
async def delete_decks_all():
    deleted_count = await db.delete_decks_all()

    if deleted_count is not None:
        return JSONResponse({"message": f"Deleted {deleted_count} deck(s)."}, status_code=200)
    else:
        return JSONResponse({"message": "No decks deleted."}, status_code=404)
