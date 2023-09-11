from typing import Any

import scooze.database.card as db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from scooze.models.card import CardModelIn

router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    responses={404: {"description": "Cards Not Found"}},
)


@router.get("/")
async def cards_root(limit: int = 3):
    cards = await db.get_cards_random(limit=limit)
    if cards:
        return JSONResponse([card.model_dump(mode="json") for card in cards], status_code=200)
    else:
        return JSONResponse({"message": "No cards found in the database."}, status_code=404)


# Create


@router.post("/add")
async def add_cards(cards: list[CardModelIn]):
    inserted_ids = await db.add_cards(cards=cards)
    if inserted_ids:
        return JSONResponse({"message": f"Created {len(inserted_ids)} cards."}, status_code=200)
    else:
        return JSONResponse({"message": f"Failed to create a new card."}, status_code=400)


@router.post("/by")
async def get_cards_by(
    property_name: str, items: list[Any], paginated: bool = True, page: int = 1, page_size: int = 10
):
    cards = await db.get_cards_by_property(
        property_name=property_name, items=items, paginated=paginated, page=page, page_size=page_size
    )
    if cards:
        return JSONResponse([card.model_dump(mode="json") for card in cards], status_code=200)
    else:
        return JSONResponse({"message": f"Cards not found."}, status_code=404)


# Delete


@router.delete("/delete/all/")
async def delete_cards_all():
    deleted_count = await db.delete_cards_all()

    if deleted_count:
        return JSONResponse({"message": f"Deleted {deleted_count} cards."}, status_code=200)
    else:
        return JSONResponse({"message": f"No cards deleted."}, status_code=404)
