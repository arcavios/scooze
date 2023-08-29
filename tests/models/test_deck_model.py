from collections import Counter
from datetime import datetime, timezone

import pytest
from scooze.enums import Format
from scooze.models.card import CardModel
from scooze.models.deck import DeckModel

# region Fixtures


@pytest.fixture
def archetype() -> str:
    return "Amulet Titan"


@pytest.fixture
def today() -> datetime:
    return datetime.now(timezone.utc).date()


@pytest.fixture
def main_cards() -> Counter:
    main_cards = Counter(
        {
            CardModel.model_construct(name="Expedition Map", mana_value=1): 2,
            CardModel.model_construct(name="Boseiju, Who Endures", mana_value=0): 2,
            CardModel.model_construct(name="Forest", mana_value=0): 6,
        }
    )
    return main_cards


@pytest.fixture
def side_cards() -> Counter:
    side_cards = Counter(
        {
            CardModel.model_construct(name="Pithing Needle", mana_value=1): 1,
            CardModel.model_construct(name="Trail of Crumbs", mana_value=2, colors=["G"]): 2,
            CardModel.model_construct(name="Forest", mana_value=0): 9,
            CardModel.model_construct(name="Expedition Map", mana_value=1): 2,
        }
    )
    return side_cards


@pytest.fixture
def cmdr_cards() -> Counter:
    cmdr_cards = Counter(
        {
            CardModel.model_construct(name="Mayael the Anima", mana_value=3): 1,
        }
    )
    return cmdr_cards


# endregion


def test_archetype(archetype):
    deck = DeckModel.model_construct(archetype=archetype)
    assert deck.archetype == archetype


def test_format(main_cards):
    deck = DeckModel.model_construct(archetype="test_format", format=Format.MODERN, main=main_cards)
    assert deck.format == Format.MODERN


@pytest.mark.deck_validation
def test_format_validation():
    with pytest.raises(ValueError) as _:
        DeckModel.model_validate({"archetype": "test_format_validation", "format": "not a real format"})


def test_date_played(today):
    deck = DeckModel.model_construct(archetype="test_date_played", date_played=today)
    assert deck.date_played == today


def test_main(main_cards):
    deck = DeckModel.model_construct(archetype="test_main", main=main_cards)
    assert deck.main == main_cards


@pytest.mark.deck_validation
def test_main_validation(main_cards):
    with pytest.raises(ValueError) as _:
        DeckModel.model_validate({"archetype": "test_main_validation", "format": Format.MODERN, "main": main_cards})


def test_side(side_cards):
    deck = DeckModel.model_construct(archetype="test_side", side=side_cards)
    assert deck.side == side_cards


@pytest.mark.deck_validation
def test_side_validation(side_cards):
    with pytest.raises(ValueError) as _:
        DeckModel.model_validate({"archetype": "test_side_validation", "format": Format.COMMANDER, "side": side_cards})


def test_cmdr(cmdr_cards):
    deck = DeckModel.model_construct(archetype="test_cmdr", cmdr=cmdr_cards)
    assert deck.cmdr == cmdr_cards


@pytest.mark.deck_validation
def test_cmdr_validation(cmdr_cards):
    with pytest.raises(ValueError) as _:
        DeckModel.model_validate({"archetype": "test_cmdr_validation", "format": Format.COMMANDER, "cmdr": cmdr_cards})


def test_eq(archetype, today, main_cards, side_cards):
    deckA = DeckModel.model_construct(
        archetype=archetype,
        format=Format.MODERN,
        date_played=today,
        main=main_cards,
        side=side_cards,
    )
    deckB = DeckModel.model_construct(
        archetype=archetype,
        format=Format.MODERN,
        date_played=today,
        main=main_cards,
        side=side_cards,
    )
    assert deckA == deckB
