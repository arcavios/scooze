import slurrk.database as db
from fastapi import APIRouter
from slurrk.models.card import Card

router = APIRouter(
    prefix="/card",
    tags=["card"],
    responses={404: {"description": "Card not found"}},
)


@router.get("/")
def card_root():
    return {"Documentation": f"{router.docs_url}"}


# Create


@router.post("/add")
def add_card(card: Card):
    # TODO: create our card
    return {
        "card.id": card.id,
        "card.name": card.name,
        "card.color": card.color,
    }


# Read


@router.get("/id/{card_id}")
def get_card_by_id(card_id: str):
    # TODO: do oracle id lookup for card
    return {"card": f"Card associated with {card_id}"}


@router.get("/name/{card_name}")
def get_card_by_name(card_name: str):
    # TODO: do name (case sensitive) lookup for card
    return {"card": f"Card named {card_name}"}


# Update


@router.put("/update/{card_id}")
def update_card_by_id(card_id: str, card: Card):
    # TODO: update card values
    return {
        "card.id": card.id,
        "card.name": card.name,
        "card.color": card.color,
    }


# Delete


@router.delete("/{card_id}")
def delete_card_by_id(card_id):
    # TODO: delete card
    return {"Deleted card id": card_id}
