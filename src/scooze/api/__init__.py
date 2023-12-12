import asyncio
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from functools import cache
from typing import Any

import scooze.api.bulkdata as bulkdata_api
import scooze.api.card as card_api
from beanie import PydanticObjectId, init_beanie
from scooze.api.utils import _check_for_safe_context, _safe_cache
from scooze.card import CardT, FullCard
from scooze.catalogs import ScryfallBulkFile
from scooze.config import CONFIG
from scooze.models.card import CardModel
from scooze.mongo import db, mongo_close, mongo_connect


class ScoozeApi(AbstractContextManager):
    """
    Context manager object for doing I/O from a Mongo database.

    Sample usage:
        >>> with ScoozeApi() as s:
                green_cards = s.get_cards_by("colors", [Color.GREEN])
                woe_cards = s.get_cards_by_set("woe")
                black_lotus = s.get_card_by_scryfall_id("b0faa7f2-b547-42c4-a810-839da50dadfe")
                print(black_lotus.total_words())
    """

    def __init__(self, card_class: type[CardT] = FullCard):
        self.card_class = card_class
        self.safe_context = False

    def __enter__(self):
        self.safe_context = True
        asyncio.get_event_loop().run_until_complete(mongo_connect())
        asyncio.get_event_loop().run_until_complete(
            init_beanie(database=db.client[CONFIG.mongo_db], document_models=[CardModel])
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        asyncio.get_event_loop().run_until_complete(mongo_close())

    # region Card endpoints

    @_safe_cache
    @_check_for_safe_context
    def get_card_by(self, property_name: str, value) -> CardT:
        """
        Search the database for the first card that matches the given criteria.

        Args:
            property_name: The property to check.
            value: The value to match on.

        Returns:
            The first matching card, or None if none were found.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(
            card_api.get_card_by(property_name=property_name, value=value, card_class=self.card_class)
        )

    @_check_for_safe_context
    def get_cards_by(
        self,
        property_name: str,
        values: list[Any],
        paginated: bool = False,
        page: int = 1,
        page_size: int = 10,
    ) -> list[CardT]:
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

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(
            card_api.get_cards_by(
                property_name=property_name,
                values=values,
                card_class=self.card_class,
                paginated=paginated,
                page=page,
                page_size=page_size,
            )
        )

    # region Convenience methods for single-card lookup

    @cache
    @_check_for_safe_context
    def get_card_by_name(self, name: str) -> CardT:
        """
        Search the database for a card with the given name.

        Args:
            name: The card name to search for.

        Returns:
            A card with the given name if found, or None if none were found.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(
            card_api.get_card_by(
                property_name="name",
                value=name,
                card_class=self.card_class,
            )
        )

    @cache
    @_check_for_safe_context
    def get_card_by_oracle_id(self, oracle_id: str) -> CardT:
        """
        Search the database for a card with the given Oracle ID.

        Args:
            oracle_id: The card [Oracle ID](https://scryfall.com/docs/api/cards) to search for.

        Returns:
            A card with the given Oracle ID if found, or None if none were found.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(
            card_api.get_card_by(
                property_name="oracle_id",
                value=oracle_id,
                card_class=self.card_class,
            )
        )

    @cache
    @_check_for_safe_context
    def get_card_by_scryfall_id(self, scryfall_id: str) -> CardT:
        """
        Search the database for a card with the given Scryfall ID.

        Args:
            scryfall_id: The card [Scryfall ID](https://scryfall.com/docs/api/cards) to search for.

        Returns:
            A card with the given Scryfall ID if found, or None if none were found.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(
            card_api.get_card_by(
                property_name="scryfall_id",
                value=scryfall_id,
                card_class=self.card_class,
            )
        )

    # endregion

    # region Convenience methods for multiple card lookup

    @_check_for_safe_context
    def get_cards_by_set(self, set_code: str) -> list[CardT]:
        """
         Search the database for all cards in the given set.
         Expects the 3-letter [set code](https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_sets)
         for a set (e.g. "CMD")

         Args:
             set_code: The set code to search for.

         Returns:
            A list of cards from the given set, or empty list if none were found.

        Raises:
             RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(
            card_api.get_cards_by(
                property_name="set",
                values=[set_code],
                card_class=self.card_class,
            )
        )

    @_check_for_safe_context
    def get_cards_all(self) -> list[CardT]:
        """
        Get all cards from the database. WARNING: may be extremely large.

        Returns:
            A list of all cards in the database.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(card_api.get_cards_all(self.card_class))

    # TODO(#146): add function get_cards_by_format (format, legality)

    # endregion

    @_check_for_safe_context
    def add_card(self, card: CardT) -> PydanticObjectId:
        """
        Add a card to the database.

        Args:
            card: The card to insert.

        Returns:
            The ID of the inserted card, or None if it was unable.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(card_api.add_card(card=card))

    @_check_for_safe_context
    def add_cards(self, cards: list[CardT]) -> list[PydanticObjectId]:
        """
        Add a list of cards to the database.

        Args:
            cards: The list of card to insert.

        Returns:
            The IDs of the inserted cards, or empty list if unable.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(card_api.add_cards(cards=cards))

    @_check_for_safe_context
    def delete_card(self, id: str) -> bool:
        """
        Delete a card from the database.

        Args:
            id: The ID of the card to delete.

        Returns:
            True if the card is deleted, False otherwise.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(card_api.delete_card(id=id))

    @_check_for_safe_context
    def delete_cards_all(self) -> int:
        """
        Delete all cards in the database.

        Returns:
            The number of cards deleted, or None if none could be deleted.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(card_api.delete_cards_all())

    # endregion

    # region Deck endpoints

    # TODO(#145): add deck endpoints to python api

    # endregion

    # region Bulk data I/O

    @_check_for_safe_context
    def load_card_file(self, file_type: ScryfallBulkFile, bulk_file_dir: str):
        """
        Loads the desired file from the given directory into a local Mongo
        database. Attempts to download it from Scryfall if it isn't found.

        Args:
            file_type: The type of [ScryfallBulkFile](https://scryfall.com/docs/api/bulk-data)
            to insert into the database.
            bulk_file_dir: The path to the folder containing the ScryfallBulkFile.

        Raises:
            RuntimeError: If used outside a `with` context.
        """

        return asyncio.get_event_loop().run_until_complete(
            bulkdata_api.load_card_file(
                file_type=file_type,
                bulk_file_dir=bulk_file_dir,
            )
        )

    # endregion


class AsyncScoozeApi(AbstractAsyncContextManager):
    """
    Async context manager object for doing I/O from a Mongo database.
    Most commonly used in asynchronous contexts like Jupyter Notebooks or other
    web applications.

    Sample usage:
        >>> async with AsyncScoozeApi() as s:
                green_cards = await s.get_cards_by("colors", [Color.GREEN])
                woe_cards = await s.get_cards_by_set("woe")
                black_lotus = await s.get_card_by_scryfall_id("b0faa7f2-b547-42c4-a810-839da50dadfe")
                print(black_lotus.total_words())
    """

    def __init__(self, card_class: type[CardT] = FullCard):
        self.card_class = card_class
        self.safe_context = False

    async def __aenter__(self):
        self.safe_context = True
        await mongo_connect()
        await init_beanie(database=db.client[CONFIG.mongo_db], document_models=[CardModel])

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await mongo_close()

    # region Card endpoints

    @_safe_cache
    @_check_for_safe_context
    async def get_card_by(self, property_name: str, value) -> CardT:
        """
        Search the database for the first card that matches the given criteria.

        Args:
            property_name: The property to check.
            value: The value to match on.

        Returns:
            The first matching card, or None if none were found.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.get_card_by(property_name=property_name, value=value, card_class=self.card_class)

    @_check_for_safe_context
    async def get_cards_by(
        self,
        property_name: str,
        values: list[Any],
        paginated: bool = False,
        page: int = 1,
        page_size: int = 10,
    ) -> list[CardT]:
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

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.get_cards_by(
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
    async def get_card_by_name(self, name: str) -> CardT:
        """
        Search the database for a card with the given name.

        Args:
            name: The card name to search for.

        Returns:
            A card with the given name if found, or None if none were found.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.get_card_by(
            property_name="name",
            value=name,
            card_class=self.card_class,
        )

    @cache
    @_check_for_safe_context
    async def get_card_by_oracle_id(self, oracle_id: str) -> CardT:
        """
        Search the database for a card with the given Oracle ID.

        Args:
            oracle_id: The card [Oracle ID](https://scryfall.com/docs/api/cards) to search for.

        Returns:
            A card with the given Oracle ID if found, or None if none were found.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.get_card_by(
            property_name="oracle_id",
            value=oracle_id,
            card_class=self.card_class,
        )

    @cache
    @_check_for_safe_context
    async def get_card_by_scryfall_id(self, scryfall_id: str) -> CardT:
        """
        Search the database for a card with the given Scryfall ID.

        Args:
            scryfall_id: The card [Scryfall ID](https://scryfall.com/docs/api/cards) to search for.

        Returns:
            A card with the given Scryfall ID if found, or None if none were found.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.get_card_by(
            property_name="scryfall_id",
            value=scryfall_id,
            card_class=self.card_class,
        )

    # endregion

    # region Convenience methods for multiple card lookup

    @_check_for_safe_context
    async def get_cards_by_set(self, set_code: str) -> list[CardT]:
        """
        Search the database for all cards in the given set.
        Expects the 3-letter [set code](https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_sets)
        for a set (e.g. "CMD")

        Args:
            set_code: The set code to search for.

        Returns:
            A list of cards from the given set, or empty list if none were found.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.get_cards_by(
            property_name="set",
            values=[set_code],
            card_class=self.card_class,
        )

    @_check_for_safe_context
    async def get_cards_all(self) -> list[CardT]:
        """
        Get all cards from the database. WARNING: may be extremely large.

        Returns:
            A list of all cards in the database.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.get_cards_all(self.card_class)

    # TODO(#146): add function get_cards_by_format (format, legality)

    # endregion

    @_check_for_safe_context
    async def add_card(self, card: CardT) -> PydanticObjectId:
        """
        Add a card to the database.

        Args:
            card: The card to insert.

        Returns:
            The ID of the inserted card, or None if it was unable.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.add_card(card=card)

    @_check_for_safe_context
    async def add_cards(self, cards: list[CardT]) -> list[PydanticObjectId]:
        """
        Add a list of cards to the database.

        Args:
            cards: The list of card to insert.

        Returns:
            The IDs of the inserted cards, or empty list if unable.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.add_cards(cards=cards)

    @_check_for_safe_context
    async def delete_card(self, id: str) -> bool | None:
        """
        Delete a card from the database.

        Args:
            id: The ID of the card to delete.

        Returns:
            True if the card is deleted, False otherwise.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.delete_card(id=id)

    @_check_for_safe_context
    async def delete_cards_all(self) -> int | None:
        """
        Delete all cards in the database.

        Returns:
            The number of cards deleted, or None if none could be deleted.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await card_api.delete_cards_all()

    # endregion

    # region Deck endpoints

    # TODO(#145): add deck endpoints to python api

    # endregion

    # region Bulk data I/O

    @_check_for_safe_context
    async def load_card_file(self, file_type: ScryfallBulkFile, bulk_file_dir: str):
        """
        Loads the desired file from the given directory into a local Mongo
        database. Attempts to download it from Scryfall if it isn't found.

        Args:
            file_type: The type of [ScryfallBulkFile](https://scryfall.com/docs/api/bulk-data)
            to insert into the database.
            bulk_file_dir: The path to the folder containing the ScryfallBulkFile.

        Raises:
            RuntimeError: If used outside an `async with` context.
        """

        return await bulkdata_api.load_card_file(
            file_type=file_type,
            bulk_file_dir=bulk_file_dir,
        )

    # endregion
