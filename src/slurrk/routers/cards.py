from typing import Annotated, List

import slurrk.database as db
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from slurrk.models.card import CardIn, CardOut

router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    responses={404: {"description": "Cards Not Found"}},
)


@router.get("/")
def cards_root():
    # TODO: return a few random cards
    return {"Documentation": f"hello world"}


# Create


@router.post("/add")
async def add_cards(cards: List[CardIn]):
    insert_many_result = await db.add_cards(cards=cards)
    if insert_many_result:
        return JSONResponse({"message": f"Created {len(insert_many_result.inserted_ids)} cards."}, status_code=200)
    else:
        return JSONResponse({"message": f"Failed to create a new card."}, status_code=400)


### TODO: get many
### TODO: update many ???


# Delete


@router.delete("/delete_all/")
async def delete_cards_all():
    delete_many_response = await db.delete_cards_all()

    if delete_many_response:
        return JSONResponse({"message": f"Deleted {delete_many_response.deleted_count} cards."}, status_code=200)
    else:
        return JSONResponse({"message": f"No cards deleted."}, status_code=404)
