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


@router.get("/")
async def decks_root(limit: int = 3):
    decks = await db.get_decks_random(limit=limit)
    if decks:
        return JSONResponse([deck.model_dump(mode="json") for deck in decks], status_code=200)
    else:
        return JSONResponse({"message": "No decks found in the database."}, status_code=404)


# Create


@router.post("/add")
async def add_decks(decks: list[DeckModelIn]):
    inserted_ids = await db.add_decks(decks=decks)
    if inserted_ids:
        return JSONResponse({"message": f"Created {len(inserted_ids)} decks."}, status_code=200)
    else:
        return JSONResponse({"message": f"Failed to create a new deck."}, status_code=400)


@router.post("/by")
async def get_decks_by(
    property_name: str, values: list[Any], paginated: bool = True, page: int = 1, page_size: int = 10
):
    decks = await db.get_decks_by_property(
        property_name=property_name, values=values, paginated=paginated, page=page, page_size=page_size
    )
    if decks:
        return JSONResponse([deck.model_dump(mode="json") for deck in decks], status_code=200)
    else:
        return JSONResponse({"message": f"Decks not found."}, status_code=404)


# Delete


@router.delete("/delete/all/")
async def delete_decks_all():
    deleted_count = await db.delete_decks_all()

    if deleted_count:
        return JSONResponse({"message": f"Deleted {deleted_count} decks."}, status_code=200)
    else:
        return JSONResponse({"message": f"No decks deleted."}, status_code=404)
