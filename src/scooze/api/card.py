import asyncio
import json
from typing import Any, List

import scooze.database.card as db
from scooze.card import CardT
from scooze.models.card import CardModelIn


# region Reading out single cards


def get_card_by(property_name: str, value, card_class: CardT) -> CardT:
    card_model = asyncio.run(
        db.get_card_by_property(
            property_name=property_name,
            value=value,
        )
    )
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


# endregion

# region Convenience methods for common lookups


def get_cards_by_set(set_name: str, card_class: CardT) -> List[CardT]:
    return get_cards_by(
        property_name="set",
        values=[set_name],
        card_class=card_class,
    )

# TODO(#7): more convenience methods

# endregion

# region Adding/removing cards


def add_card_to_db(card: CardT):
    card_model = CardModelIn.from_json(json.dumps(card))
    asyncio.run(db.add_card(card_model))


def add_cards_to_db(cards: List[CardT]):
    card_models = [CardModelIn.from_json(json.dumps(card)) for card in cards]
    asyncio.run(db.add_cards(card_models))

# TODO(#127): delete single card

def remove_all_cards_from_db() -> int:
    return asyncio.run(db.delete_cards_all())


# endregion
