from typing import Any

import scooze.database.core as db_core
from scooze.enums import DbCollection
from scooze.models.deck import DeckModelIn, DeckModelOut

# TODO(#119): database docstrings

# region Deck


async def add_deck(deck: DeckModelIn) -> DeckModelOut:
    """
    Adds the given deck to the database

    :param deck: the deck to insert
    :returns: the deck that was inserted, or None if it was unable
    """

    new_deck = await db_core.insert_document(
        DbCollection.DECKS,
        deck.model_dump(
            mode="json",
            by_alias=True,
        ),
    )
    if new_deck:
        return DeckModelOut(**new_deck)


async def get_deck_by_property(property_name: str, value) -> DeckModelOut:
    """
    Search the database for the first deck that matches the given criteria

    :param property_name: the property name to check
    :param value: the value to match on
    :returns: the first matching deck, or None if none were found
    """

    deck = await db_core.get_document_by_property(DbCollection.DECKS, property_name, value)
    if deck:
        return DeckModelOut(**deck)


async def update_deck(id: str, deck: DeckModelIn) -> DeckModelOut:
    """
    Updates the deck with the given id with the given values

    :param id: the id of the deck to update
    :param deck: the values to update
    :returns: the updated deck, or None if it was unable to update or find the deck
    """

    updated_deck = await db_core.update_document(
        DbCollection.DECKS,
        id,
        deck.model_dump(
            mode="json",
            by_alias=True,
            include=deck.model_fields_set,
        ),
    )

    if updated_deck:
        return DeckModelOut(**updated_deck)


async def delete_deck(id: str) -> DeckModelOut:
    """
    Deletes the deck with the given id

    :param id: the id of the deck to delete
    :returns: the deleted deck, or None if unable to delete or find the deck
    """

    deleted_deck = await db_core.delete_document(DbCollection.DECKS, id)

    if deleted_deck:
        return DeckModelOut(**deleted_deck)


# endregion

# region Decks


async def add_decks(decks: list[DeckModelIn]) -> list[str]:
    """
    Adds the given list of decks to the database

    :param decks: the list of deck to insert
    :returns: the list of ids for decks that were inserted, or None if unable
    """

    insert_many_result = await db_core.insert_many_documents(
        DbCollection.DECKS,
        [
            deck.model_dump(
                mode="json",
                by_alias=True,
            )
            for deck in decks
        ],
    )

    if insert_many_result:
        return insert_many_result.inserted_ids


async def get_decks_random(limit: int) -> list[DeckModelOut]:
    """
    Get a random assortment of decks from the database

    :param limit: the number of decks to return
    :returns: a random list of decks, or None if none were found
    """

    decks = await db_core.get_random_documents(DbCollection.DECKS, limit)
    if len(decks) > 0:
        return [DeckModelOut(**deck) for deck in decks]


async def get_decks_by_property(
    property_name: str, values: list[Any], paginated: bool = True, page: int = 1, page_size: int = 10
) -> list[DeckModelOut]:
    """
    Search the database for the decks that match the given criteria, with options for pagination

    :param property_name: the property name to check
    :param values: a list of values to match on
    :param paginated: whether to paginate the results
    :param page: the page to return, if paginated
    :param page_size: the size of each page, if paginated
    :returns: a list of decks matching the search criteria, or None if none were found
    """

    decks = await db_core.get_documents_by_property(
        DbCollection.DECKS, property_name, values, paginated, page, page_size
    )

    if len(decks) > 0:
        return [DeckModelOut(**deck) for deck in decks]


async def delete_decks_all() -> int:
    """Delete all decks in the database"""

    delete_many_result = await db_core.delete_documents(DbCollection.DECKS)
    if delete_many_result:
        return delete_many_result


# endregion
