import asyncio
from contextlib import AbstractContextManager
from functools import cache
from typing import Any, List

import scooze.api.bulkdata as bulkdata_api
import scooze.api.card as card_api
import scooze.database.mongo as mongo
from bson import ObjectId
from scooze.card import CardT, FullCard
from scooze.catalogs import ScryfallBulkFile

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

    def _check_for_safe_context(self, func):
        def wrapper(*args, **kwargs):
            if not self.safe_context:
                raise RuntimeError(CONTEXT_ERROR_MSG)
            return func(args, kwargs)

        return wrapper

    # region Card endpoints

    @_check_for_safe_context
    def get_card_by(self, property_name: str, value) -> CardT:
        return card_api.get_card_by(property_name, value, self.card_class)

    @_check_for_safe_context
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
    @_check_for_safe_context
    def get_card_by_name(self, name: str) -> CardT:
        return card_api.get_card_by(
            property_name="name",
            value=name,
            card_class=self.card_class,
        )

    @cache
    @_check_for_safe_context
    def get_card_by_oracle_id(self, oracle_id: str) -> CardT:
        return card_api.get_card_by(
            property_name="oracle_id",
            value=oracle_id,
            card_class=self.card_class,
        )

    @cache
    @_check_for_safe_context
    def get_card_by_scryfall_id(self, scryfall_id: str) -> CardT:
        return card_api.get_card_by(
            property_name="_id",
            value=scryfall_id,
            card_class=self.card_class,
        )

    # endregion

    # region Convenience methods for multiple card lookup

    @_check_for_safe_context
    def get_cards_by_set(self, set_name: str) -> List[CardT]:
        return card_api.get_cards_by(
            property_name="set",
            values=[set_name],
            card_class=self.card_class,
        )

    # TODO(#146) - add function get_cards_by_format (format, legality)

    # endregion

    @_check_for_safe_context
    def add_card(self, card: CardT) -> ObjectId:
        return card_api.add_card(card=card)

    @_check_for_safe_context
    def add_cards(self, cards: List[CardT]) -> List[ObjectId]:
        return card_api.add_cards(cards=cards)

    @_check_for_safe_context
    def delete_card(self, id: str) -> CardT:
        return card_api.delete_card(id=id)

    @_check_for_safe_context
    def delete_cards_all(self) -> int:
        return card_api.delete_cards_all()

    # endregion

    # region Deck endpoints

    # TODO(#145) - add deck endpoints to python api

    # endregion

    # region Bulk data I/O

    @_check_for_safe_context
    def load_card_file(self, file_type: ScryfallBulkFile, bulk_file_dir: str):
        return bulkdata_api.load_card_file(
            file_type=file_type,
            bulk_file_dir=bulk_file_dir,
        )

    # endregion
