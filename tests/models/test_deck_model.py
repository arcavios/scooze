from collections import Counter
from datetime import datetime, timezone

import pytest
from pydantic_core import ValidationError
from scooze.enums import Format, InThe
from scooze.models.card import DecklistCardModel
from scooze.models.deck import DecklistFormatter, DeckModel

# region Fixtures


@pytest.fixture
def archetype() -> str:
    return "Amulet Titan"


@pytest.fixture
def format() -> Format:
    return Format.MODERN


@pytest.fixture
def today() -> datetime:
    return datetime.now(timezone.utc).date


@pytest.fixture
def existing_card() -> str:
    return DecklistCardModel.model_construct(
        name="Expedition Map",
        mana_value=1,
    )


@pytest.fixture
def new_card() -> str:
    return DecklistCardModel.model_construct(
        name="Primeval Titan",
        mana_value=6,
        colors=["G"],
    )


@pytest.fixture
def main_string() -> str:
    return "2 Expedition Map\n2 Boseiju, Who Endures\n56 Forest"


@pytest.fixture
def main_cards() -> Counter:
    main_cards = Counter(
        {
            DecklistCardModel.model_construct(name="Expedition Map", mana_value=1): 2,
            DecklistCardModel.model_construct(name="Boseiju, Who Endures", mana_value=0): 2,
            DecklistCardModel.model_construct(name="Forest", mana_value=0): 56,
        }
    )
    return main_cards


@pytest.fixture
def side_string() -> str:
    return "1 Pithing Needle\n2 Trail of Crumbs\n9 Forest\n2 Expedition Map"


@pytest.fixture
def side_cards() -> Counter:
    side_cards = Counter(
        {
            DecklistCardModel.model_construct(name="Pithing Needle", mana_value=1): 1,
            DecklistCardModel.model_construct(name="Trail of Crumbs", mana_value=2, colors=["G"]): 2,
            DecklistCardModel.model_construct(name="Forest", mana_value=0): 9,
            DecklistCardModel.model_construct(name="Expedition Map", mana_value=1): 2,
        }
    )
    return side_cards


# endregion


def test_archetype(archetype):
    deck = DeckModel.model_construct(archetype=archetype)
    assert deck.archetype == archetype


def test_format(format, main_cards):
    deck = DeckModel.model_construct(format=format, main=main_cards)
    assert deck.format == format


@pytest.mark.deck_validation
def test_format_validation():
    with pytest.raises(ValueError) as e:
        DeckModel.model_validate({"archetype": "test_format_validation", "format": "not a real format"})


def test_date_played(today):
    deck = DeckModel.model_construct(date_played=today)
    assert deck.date_played == today


# def test_str(archetype, format, today, main_cards, side_cards):
#     deck = DeckModel.model_construct(
#         archetype=archetype,
#         format=format,
#         date_played=today,
#         main=main_cards,
#         side=side_cards,
#     )
#     decklist = deck.to_decklist()
#     deck_str = (
#         f"""Archetype: {archetype}\n"""
#         f"""Format: {format}\n"""
#         f"""Date Played: {today}\n"""
#         f"""Decklist:\n{decklist}\n""" # NOTE: not implemented
#     )
#     assert str(deck) == deck_str


def test_eq(archetype, format, today, main_cards, side_cards):
    deckA = DeckModel.model_construct(
        archetype=archetype,
        format=format,
        date_played=today,
        main=main_cards,
        side=side_cards,
    )
    deckB = DeckModel.model_construct(
        archetype=archetype,
        format=format,
        date_played=today,
        main=main_cards,
        side=side_cards,
    )
    assert deckA == deckB
