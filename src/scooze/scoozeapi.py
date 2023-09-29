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


class ScoozeApi(AbstractContextManager):
    """
    Context manager object for doing I/O from a Mongo database.

    Sample usage:
        >>> with ScoozeApi as s:
                green_cards = s.get_cards_by("colors", [Color.GREEN])
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
        """
        Ensure an instance method of ScoozeApi is called in a safe context.
        """

        if not self.safe_context:
            raise RuntimeError("ScoozeApi used outside of 'with' context")

    # region Card endpoints

    @cache
    def get_card_by(self, property_name: str, value) -> CardT:
        """
        Search the database for the first card that matches the given criteria.

        Args:
            property_name: The property to check.
            value: The value to match on.

        Returns:
            The first matching card, or None if none were found.
        """

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
        """
        Search the database for cards matching the given criteria, with options for
        pagination.

        Args:
            property_name: The property to check.
            values: A list of values to match on.
            paginated: Whether to paginate the results.
            page: The page to look at, if paginated.
            page_size: The size of each page, if paginated.

        Returns:
            A list of cards matching the search criteria, or empty list if none
            were found.
        """

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
        """
        Search the database for a card with the given name.

        Args:
            name: The card name to search for.

        Returns:
            A card with the given name if found, or None if none were found.
        """

        self._check_for_safe_context()
        return card_api.get_card_by(
            property_name="name",
            value=name,
            card_class=self.card_class,
        )

    @cache
    def get_card_by_oracle_id(self, oracle_id: str) -> CardT:
        """
        Search the database for a card with the given Oracle ID.

        Args:
            oracle_id: The card [Oracle ID](https://scryfall.com/docs/api/cards) to search for.

        Returns:
            A card with the given Oracle ID if found, or None if none were found.
        """

        self._check_for_safe_context()
        return card_api.get_card_by(
            property_name="oracle_id",
            value=oracle_id,
            card_class=self.card_class,
        )

    @cache
    def get_card_by_scryfall_id(self, scryfall_id: str) -> CardT:
        """
        Search the database for a card with the given Scryfall ID.

        Args:
            scryfall_id: The card [Scryfall ID](https://scryfall.com/docs/api/cards) to search for.

        Returns:
            A card with the given Scryfall ID if found, or None if none were found.
        """

        self._check_for_safe_context()
        return card_api.get_card_by(
            property_name="scryfall_id",
            value=scryfall_id,
            card_class=self.card_class,
        )

    # endregion

    # region Convenience methods for multiple card lookup

    def get_cards_by_set(self, set_code: str) -> List[CardT]:
        """
        Search the database for all cards in the given set.
        Expects the 3-letter [set code](https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_sets)
        for a set (e.g. "CMD")

        Args:
            set_code: The set code to search for.

        Returns:
           A list of cards from the given set, or empty list if none were found.
        """

        self._check_for_safe_context()
        return card_api.get_cards_by(
            property_name="set",
            values=[set_code],
            card_class=self.card_class,
        )

    # TODO(#146): add function get_cards_by_format (format, legality)

    # endregion

    def add_card(self, card: CardT) -> ObjectId:
        """
        Add a card to the database.

        Args:
            card: The card to insert.

        Returns:
            The ID of the inserted card, or None if it was unable.
        """

        self._check_for_safe_context()
        return card_api.add_card(card=card)

    def add_cards(self, cards: List[CardT]) -> List[ObjectId]:
        """
        Add a list of cards to the database.

        Args:
            cards: The list of card to insert.

        Returns:
            The IDs of the inserted cards, or empty list if unable.
        """

        self._check_for_safe_context()
        return card_api.add_cards(cards=cards)

    def delete_card(self, id: str) -> bool:
        """
        Delete a card from the database.

        Args:
            id: The ID of the card to delete.

        Returns:
            True if the card is deleted, False otherwise.
        """

        self._check_for_safe_context()
        return card_api.delete_card(id=id)

    def delete_cards_all(self) -> int:
        """
        Delete all cards in the database.

        Returns:
            The number of cards deleted, or None if none could be deleted.
        """

        self._check_for_safe_context()
        return card_api.delete_cards_all()

    # endregion

    # region Deck endpoints

    # TODO(#145): add deck endpoints to python api

    # endregion

    # region Bulk data I/O

    def load_card_file(self, file_type: ScryfallBulkFile, bulk_file_dir: str):
        """
        Loads the desired file from the given directory into a local Mongo
        database. Attempts to download it from Scryfall if it isn't found.

        Args:
            file_type: The type of [ScryfallBulkFile](https://scryfall.com/docs/api/bulk-data)
            to insert into the database.
            bulk_file_dir: The path to the folder containing the ScryfallBulkFile.
        """

        self._check_for_safe_context()
        return bulkdata_api.load_card_file(
            file_type=file_type,
            bulk_file_dir=bulk_file_dir,
        )

    # endregion
