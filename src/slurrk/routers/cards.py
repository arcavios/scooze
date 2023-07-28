from typing import List

import slurrk.database as db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from slurrk.models.card import CardIn, CardOut
from slurrk.models.utils import ModelAttribute

router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    responses={404: {"description": "Cards Not Found"}},
)


@router.get("/")
async def cards_root(limit: int = 3):
    cards = await db.get_cards_random(limit=limit)
    if cards:
        return JSONResponse({"cards": [card.model_dump(mode="json") for card in cards]}, status_code=200)
    else:
        return JSONResponse({"message": "No cards found in the database."}, status_code=404)


# Create


@router.post("/add")
async def add_cards(cards: List[CardIn]):
    insert_many_result = await db.add_cards(cards=cards)
    if insert_many_result:
        return JSONResponse({"message": f"Created {len(insert_many_result.inserted_ids)} cards."}, status_code=200)
    else:
        return JSONResponse({"message": f"Failed to create a new card."}, status_code=400)


@router.post("/by")
async def get_cards_by(property_name: str, items: List[ModelAttribute]):
    cards = await db.get_cards_by_property(property_name=property_name, items=items)
    if cards:
        return JSONResponse({"cards": [card.model_dump(mode="json") for card in cards]}, status_code=200)
    else:
        return JSONResponse({"message": f"Cards not found."}, status_code=404)


# Delete


@router.delete("/delete_all/")
async def delete_cards_all():
    delete_many_response = await db.delete_cards_all()

    if delete_many_response:
        return JSONResponse({"message": f"Deleted {delete_many_response.deleted_count} cards."}, status_code=200)
    else:
        return JSONResponse({"message": f"No cards deleted."}, status_code=404)
