import asyncio
from contextlib import AbstractContextManager
from functools import cache
from typing import Any, List

import scooze.api.bulkdata as bulkdata_api
import scooze.api.card as card_api
import scooze.database.card as db_card
import scooze.database.mongo as mongo
from scooze.card import Card, CardT, FullCard
from scooze.enums import ScryfallBulkFile

CONTEXT_ERROR_STR = "Scooze used outside of 'with' context"


class Scooze(AbstractContextManager):
    """
    # TODO(#7): docstring
    """

    def __init__(self, card_class: type[CardT] = FullCard):
        self.card_class = card_class

    def __enter__(self):
        mongo.mongo_connect()
        self.safe_context = True

        # TODO(#7): start local mongod, if not already running
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        mongo.mongo_close()
        # TODO(#7): stop running mongod, if we started it

    # region Single card lookup
    @cache
    def get_card_by_name(self, name: str) -> Card | None:
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)

        return card_api.get_card_by(
            property_name="name",
            value=name,
            card_class=self.card_class,
        )

    @cache
    def get_card_by_id(self, card_id: str) -> Card | None:
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)

        return card_api.get_card_by(
            property_name="_id",
            value=card_id,
            card_class=self.card_class,
        )

    # endregion

    # region Convenience methods for cards

    # TODO(#7): more convenience methods
    #   - get_cards_by_format(format)
    #   - get_card_by_scryfall_id
    #   - get_card_by_oracle_id
    #   - get_card_by_name
    #   - get_cards_by_set
    #   - get_cards_by_format (plus legality filters?)

    # endregion

    # region Multiple card lookup

    def get_cards_by(
        self,
        property_name: str,
        values: list[Any],
        paginated: bool = True,
        page: int = 1,
        page_size: int = 10,
    ) -> List[CardT]:
        return card_api.get_cards_by(
            property_name=property_name,
            values=values,
            card_class=self.card_class,
            paginated=paginated,
            page=page,
            page_size=page_size,
        )

    # endregion

    def get_cards_by_set(self, set_name: str) -> List[CardT]:
        return card_api.get_cards_by(
            property_name="set",
            values=[set_name],
            card_class=self.card_class,
        )

    # region Bulk data I/O
    def load_card_file(self, file_type: ScryfallBulkFile, bulk_file_dir: str):
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)
        return bulkdata_api.load_card_file(
            file_type=file_type,
            bulk_file_dir=bulk_file_dir,
        )

    # endregion
