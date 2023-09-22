import asyncio
from contextlib import AbstractContextManager
from functools import cache
from typing import Any, List

import scooze.api.bulkdata as bulkdata_api
import scooze.api.card as card_api
import scooze.database.mongo as mongo
from bson import ObjectId
from scooze.card import CardT, FullCard
from scooze.catalogs import Format, Legality, ScryfallBulkFile

CONTEXT_ERROR_MSG = "Scooze used outside of 'with' context"

# TODO(#7): docstrings here


class ScoozeApi(AbstractContextManager):
    """
    Context manager object for doing I/O from a MongoDB.

    Sample usage:
        >>> with ScoozeApi as s:
                pioneer_cards = s.get_cards_by_format(Format.PIONEER)
                woe_cards = s.get_cards_by_set("woe")
                black_lotus = s.get_card_by_scryfall_id("b0faa7f2-b547-42c4-a810-839da50dadfe")
    """

    def __init__(self, card_class: type[CardT] = FullCard):
        self.card_class = card_class

    def __enter__(self):
        asyncio.run(mongo.mongo_connect())
        self.safe_context = True

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        asyncio.run(mongo.mongo_close())

    def _check_for_safe_context(self):
        if not self.safe_context:
            raise RuntimeError(CONTEXT_ERROR_MSG)

    # region Card endpoints

    def get_card_by(self, property_name: str, value) -> CardT:
        self._check_for_safe_context()
        return card_api.get_card_by(property_name, value, self.card_class)

    def get_cards_by(
        self,
        property_name: str,
        values: list[Any],
        paginated: bool = True,
        page: int = 1,
        page_size: int = 10,
    ) -> List[CardT]:
        self._check_for_safe_context()
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
        self._check_for_safe_context()
        return card_api.get_card_by(
            property_name="name",
            value=name,
            card_class=self.card_class,
        )

    @cache
    def get_card_by_oracle_id(self, oracle_id: str) -> CardT:
        self._check_for_safe_context()
        return card_api.get_card_by(
            property_name="oracle_id",
            value=oracle_id,
            card_class=self.card_class,
        )

    @cache
    def get_card_by_scryfall_id(self, scryfall_id: str) -> CardT:
        self._check_for_safe_context()
        return card_api.get_card_by(
            property_name="_id",
            value=scryfall_id,
            card_class=self.card_class,
        )

    # endregion

    # region Convenience methods for multiple card lookup

    def get_cards_by_set(self, set_name: str) -> List[CardT]:
        self._check_for_safe_context()
        return card_api.get_cards_by(
            property_name="set",
            values=[set_name],
            card_class=self.card_class,
        )

    # TODO(#146) - add function get_cards_by_format (format, legality)

    # endregion

    def add_card(self, card: CardT) -> ObjectId:
        self._check_for_safe_context()
        return card_api.add_card(card=card)

    def add_cards(self, cards: List[CardT]) -> List[ObjectId]:
        self._check_for_safe_context()
        return card_api.add_cards(cards=cards)

    def delete_card(self, id: str) -> CardT:
        self._check_for_safe_context()
        return card_api.delete_card(id=id)

    def delete_cards_all(self) -> int:
        self._check_for_safe_context()
        return card_api.delete_cards_all()

    # endregion

    # region Deck endpoints

    # TODO(#145) - add deck endpoints to python api

    # endregion

    # region Bulk data I/O

    def load_card_file(self, file_type: ScryfallBulkFile, bulk_file_dir: str):
        self._check_for_safe_context()
        return bulkdata_api.load_card_file(
            file_type=file_type,
            bulk_file_dir=bulk_file_dir,
        )

    # endregion
