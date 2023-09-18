import asyncio
from contextlib import AbstractContextManager
from functools import cache
from typing import Any, List

import scooze.api.bulkdata as bulkdata_api
import scooze.api.card as card_api
import scooze.database.mongo as mongo
from scooze.card import CardT, FullCard
from scooze.enums import Format, Legality, ScryfallBulkFile

CONTEXT_ERROR_STR = "Scooze used outside of 'with' context"


class Scooze(AbstractContextManager):
    """
    Context manager object for doing I/O from a MongoDB.

    Sample usage:
        with Scooze[OracleCard] as s:
            pioneer_cards = s.get_cards_by_format(Format.PIONEER)
            woe_cards = s.get_cards_by_set("woe")
            black_lotus = s.get_card_by_scryfall_id
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

    def get_card_by(self, property_name: str, value) -> CardT:
        return card_api.get_card_by(property_name, value, self.card_class)

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

    # region Convenience methods for single-card lookup
    @cache
    def get_card_by_name(self, name: str) -> CardT:
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)

        return card_api.get_card_by(
            property_name="name",
            value=name,
            card_class=self.card_class,
        )

    @cache
    def get_card_by_scryfall_id(self, scryfall_id: str) -> CardT:
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)
        return card_api.get_card_by(
            property_name="_id",
            value=scryfall_id,
            card_class=self.card_class,
        )

    @cache
    def get_card_by_oracle_id(self, oracle_id: str) -> CardT:
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)
        return card_api.get_card_by(
            property_name="oracle_id",
            value=oracle_id,
            card_class=self.card_class,
        )

    # endregion

    # region Convenience methods for multiple card lookup

    def get_cards_by_set(self, set_name: str) -> List[CardT]:
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)
        return card_api.get_cards_by(
            property_name="set",
            values=[set_name],
            card_class=self.card_class,
        )

    def get_cards_by_format(self, format: Format, legality: Legality = Legality.LEGAL) -> List[CardT]:
        # TODO(#7)
        raise NotImplementedError("unable to get cards by format")

    # endregion

    # region Bulk data I/O
    def load_card_file(self, file_type: ScryfallBulkFile, bulk_file_dir: str):
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_STR)
        return bulkdata_api.load_card_file(
            file_type=file_type,
            bulk_file_dir=bulk_file_dir,
        )

    # endregion
