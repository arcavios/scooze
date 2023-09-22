import asyncio
from typing import Any, List

import scooze.database.card as db
from bson import ObjectId
from scooze.card import CardT, FullCard
from scooze.models.card import CardModelIn, CardModelOut


def get_card_by(property_name: str, value, card_class: CardT = FullCard) -> CardT:
    card_model = asyncio.run(
        db.get_card_by_property(
            property_name=property_name,
            value=value,
        )
    )
    if card_model:
        return card_class.from_model(card_model)


def get_cards_by(
    property_name: str,
    values: list[Any],
    card_class: CardT = FullCard,
    paginated: bool = True,
    page: int = 1,
    page_size: int = 10,
) -> List[CardT]:
    card_models = asyncio.run(
        db.get_cards_by_property(
            property_name=property_name,
            values=values,
            paginated=paginated,
            page=page,
            page_size=page_size,
        )
    )
    return [card_class.from_model(m) for m in card_models]


def add_card(card: CardT) -> ObjectId:
    card_model = CardModelIn.model_validate(card.__dict__)
    model = asyncio.run(db.add_card(card=card_model))
    if model:
        return model.id


def add_cards(cards: List[CardT]) -> List[ObjectId]:
    card_models = [CardModelIn.model_validate(card.__dict__) for card in cards]
    return asyncio.run(db.add_cards(cards=card_models))


def delete_card(id: str) -> CardModelOut:
    return asyncio.run(db.delete_card(id=id))


def delete_cards_all() -> int:
    return asyncio.run(db.delete_cards_all())
