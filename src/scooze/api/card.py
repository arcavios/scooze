import asyncio

import scooze.database.card as db
from scooze.deckpart import CardT


# region Reading out cards
def get_card_by_name(name: str, card_class: CardT) -> CardT | None:
    card_model = asyncio.run(db.get_card_by_property("name", name))
    return CardT.from_model(card_model)


# endregion
