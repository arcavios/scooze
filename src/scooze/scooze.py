import scooze.bulkdata as bulkdata
import scooze.database.mongo as mongo
import scooze.database.card as db_card
import scooze.database.deck as db_deck
from contextlib import AbstractContextManager
import asyncio
from scooze.card import Card
from functools import cache


CONTEXT_ERROR_STR = "Scooze used outside of 'with' context"


class Scooze(AbstractContextManager):
    """
    # TODO(#7): docstring
    """
    def __init__(self):
        pass

    def __enter__(self):
        mongo.mongo_connect()
        self.safe_context = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        mongo.mongo_close()

    @cache
    def get_card_by_name(self, name: str) -> Card | None:
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)

        card_model = asyncio.run(db_card.get_card_by_property("name", name))
        return Card.from_model(card_model)

    @cache
    def get_card_by_id(self, card_id: str) -> Card | None:
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)

        card_model = asyncio.run(db_card.get_card_by_property("_id", card_id))
        return Card.from_model(card_model)


