from typing import Any

import scooze.database.core as db_core
from scooze.enums import Collection
from scooze.models.card import CardModelIn, CardModelOut

# region Card


async def add_card(card: CardModelIn) -> CardModelOut:
    # TODO(#45): router docstrings
    new_card = await db_core.insert_document(
        Collection.CARDS,
        card.model_dump(
            mode="json",
            by_alias=True,
        ),
    )
    if new_card:
        return CardModelOut(**new_card)


async def get_card_by_property(property_name: str, value) -> CardModelOut:
    # TODO(#45): router docstrings
    card = await db_core.get_document_by_property(Collection.CARDS, property_name, value)
    if card:
        return CardModelOut(**card)


async def update_card(id: str, card: CardModelIn) -> CardModelOut:
    # TODO(#45): router docstrings
    updated_card = await db_core.update_document(
        Collection.CARDS,
        id,
        card.model_dump(
            mode="json",
            by_alias=True,
            include=card.model_fields_set,
        ),
    )
    if updated_card:
        return CardModelOut(**updated_card)


async def delete_card(id: str) -> CardModelOut:
    # TODO(#45): router docstrings
    deleted_card = await db_core.delete_document(Collection.CARDS, id)

    if deleted_card:
        return CardModelOut(**deleted_card)


# endregion


# region Cards


async def add_cards(cards: list[CardModelIn]) -> list[str]:
    # TODO(#45): router docstrings
    insert_many_result = await db_core.insert_many_documents(
        Collection.CARDS,
        [
            card.model_dump(
                mode="json",
                by_alias=True,
            )
            for card in cards
        ],
    )
    if insert_many_result:
        return insert_many_result.inserted_ids


async def get_cards_random(limit: int) -> list[CardModelOut]:
    # TODO(#45): router docstrings
    cards = await db_core.get_random_documents(Collection.CARDS, limit)
    if len(cards) > 0:
        return [CardModelOut(**card) for card in cards]


async def get_cards_by_property(
    property_name: str, items: list[Any], paginated: bool = True, page: int = 1, page_size: int = 10
) -> list[CardModelOut]:
    # TODO(#45): router docstrings
    cards = await db_core.get_documents_by_property(Collection.CARDS, property_name, items, paginated, page, page_size)

    if len(cards) > 0:
        return [CardModelOut(**card) for card in cards]


async def delete_cards_all() -> int:
    # TODO(#45): router docstrings
    delete_many_result = await db_core.delete_documents(Collection.CARDS)
    if delete_many_result:
        return delete_many_result.deleted_count


# endregion
