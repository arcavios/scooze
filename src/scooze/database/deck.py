from typing import Any

import scooze.database.core as db_core
from scooze.enums import Collection
from scooze.models.deck import DeckModelIn, DeckModelOut

# region Deck


async def add_deck(deck: DeckModelIn) -> DeckModelOut:
    # TODO(#45): router docstrings
    new_deck = await db_core.insert_document(
        Collection.DECK,
        deck.model_dump(
            mode="json",
            by_alias=True,
        ),
    )
    if new_deck:
        return DeckModelOut(**new_deck)


async def get_deck_by_property(property_name: str, value) -> DeckModelOut:
    # TODO(#45): router docstrings
    deck = await db_core.get_document_by_property(Collection.DECK, property_name, value)
    if deck:
        return DeckModelOut(**deck)


async def update_deck(id: str, deck: DeckModelIn) -> DeckModelOut:
    # TODO(#45): router docstrings
    updated_deck = await db_core.update_document(
        Collection.DECK,
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
    # TODO(#45): router docstrings
    deleted_deck = await db_core.delete_document(Collection.DECK, id)

    if deleted_deck:
        return DeckModelOut(**deleted_deck)


# endregion

# region Decks


async def add_decks(decks: list[DeckModelIn]) -> list[str]:
    # TODO(#45): router docstrings
    insert_many_result = await db_core.insert_many_documents(
        Collection.DECK,
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


async def get_decks_by_property(
    property_name: str, items: list[Any], paginated: bool = True, page: int = 1, page_size: int = 10
) -> list[DeckModelOut]:
    # TODO(#45): router docstrings
    decks = await db_core.get_documents_by_property(Collection.DECK, property_name, items, paginated, page, page_size)

    if len(decks) > 0:
        return [DeckModelOut(**deck) for deck in decks]


async def delete_decks_all() -> int:
    # TODO(#45): router docstrings
    delete_many_result = await db_core.delete_documents(Collection.DECK)
    if delete_many_result:
        return delete_many_result


# endregion
