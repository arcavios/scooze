from collections import Counter
from unittest.mock import MagicMock, patch

import pytest
from bson import ObjectId
from scooze.catalogs import Format
from scooze.deck import Deck
from scooze.models.deck import DeckModel
from scooze.models.utils import ObjectIdT

# region Fixtures


@pytest.fixture
def archetype() -> str:
    return "Amulet Titan"


@pytest.fixture
def main_cards() -> Counter[ObjectIdT]:
    main_cards = Counter(
        {
            ObjectId(): 2,
            ObjectId(): 2,
            ObjectId(): 6,
        }
    )
    return main_cards


@pytest.fixture
def side_cards() -> Counter[ObjectIdT]:
    side_cards = Counter(
        {
            ObjectId(): 1,
            ObjectId(): 2,
            ObjectId(): 9,
            ObjectId(): 2,
        }
    )
    return side_cards


@pytest.fixture
def cmdr_cards() -> Counter[ObjectIdT]:
    cmdr_cards = Counter(
        {
            ObjectId(): 1,
        }
    )
    return cmdr_cards


# endregion


def test_archetype(archetype):
    deck = DeckModel.model_construct(archetype=archetype)
    assert deck.archetype == archetype


def test_format(main_cards):
    deck = DeckModel.model_construct(archetype="test_format", format=Format.MODERN, main=main_cards)
    assert deck.format is Format.MODERN


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


@patch("scooze.api.card.get_card_by")
def test_model_from_deck(
    mock_get_card: MagicMock,
    mock_cards_collection,
    archetype_modern_4c,
    today,
    main_modern_4c,
    main_modern_4c_dict,
    side_modern_4c,
    side_modern_4c_dict,
):
    dummy_model = DeckModel.model_validate(
        archetype=archetype_modern_4c,
        date_played=today,
        format=Format.MODERN,
        main_cards=main_modern_4c_dict,
        side_cards=side_modern_4c_dict,
    )
    # TODO: get card ids from card names in the main/side
    # TODO: use those counters of ids to make a new model in addition to **deck
    deck = Deck(
        archetype=archetype_modern_4c,
        date_played=today,
        format=Format.MODERN,
        main=main_modern_4c,
        side=side_modern_4c,
    )
    pass
