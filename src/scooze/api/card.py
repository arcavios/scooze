import asyncio

import scooze.database.card as db
from scooze.deckpart import CardT
from typing import Any, List


# region Reading out single cards
def get_card_by_name(name: str, card_class: CardT) -> CardT | None:
    card_model = asyncio.run(db.get_card_by_property("name", name))
    return card_class.from_model(card_model)


# endregion


# region Reading out multiple cards


def get_cards_by(
    property_name: str,
    values: list[Any],
    card_class: CardT,
    paginated: bool = True,
    page: int = 1,
    page_size: int = 10,
) -> List[CardT]:
    card_models = asyncio.run(db.get_cards_by_property(
        property_name=property_name,
        values=values,
        paginated=paginated,
        page=page,
        page_size=page_size
    ))
    return [card_class.from_model(m) for m in card_models]


# endregion
