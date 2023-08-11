from collections import Counter
from datetime import datetime, timezone
from sys import maxsize

import pytest
from pydantic_core import ValidationError
from scooze.enums import Format
from scooze.models.card import DecklistCardModel
from scooze.models.deck import Deck, DecklistFormatter, InThe

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
    deck = Deck.model_construct(archetype=archetype)
    assert deck.archetype == archetype


def test_format(format, main_cards):
    deck = Deck.model_construct(format=format, main=main_cards)
    assert deck.format == format


@pytest.mark.deck_validation
def test_format_validation():
    with pytest.raises(ValueError) as e:
        Deck.model_validate({"archetype": "test_format_validation", "format": "not a real format"})


def test_date_played(today):
    deck = Deck.model_construct(date_played=today)
    assert deck.date_played == today


def test_str(archetype, format, today, main_cards, side_cards):
    deck = Deck.model_construct(
        archetype=archetype,
        format=format,
        date_played=today,
        main=main_cards,
        side=side_cards,
    )
    decklist = deck.to_decklist()
    deck_str = (
        f"""Archetype: {archetype}\n"""
        f"""Format: {format}\n"""
        f"""Date Played: {today}\n"""
        f"""Decklist:\n{decklist}\n"""
    )
    assert str(deck) == deck_str


def test_eq(archetype, format, today, main_cards, side_cards):
    deckA = Deck.model_construct(
        archetype=archetype,
        format=format,
        date_played=today,
        main=main_cards,
        side=side_cards,
    )
    deckB = Deck.model_construct(
        archetype=archetype,
        format=format,
        date_played=today,
        main=main_cards,
        side=side_cards,
    )
    assert deckA == deckB


@pytest.mark.deck_add_cards
def test_add_card_new(new_card, main_cards):
    deck = Deck.model_construct(archetype="test_add_card_new", main=main_cards)
    deck.add_card(card=new_card)
    main_cards.update({new_card: 1})
    assert deck.main == main_cards


@pytest.mark.deck_add_cards
def test_add_card_side(existing_card, side_cards):
    deck = Deck.model_construct(archetype="test_add_card_side", side=side_cards)
    deck.add_card(card=existing_card, in_the=InThe.SIDE)
    side_cards.update({existing_card: 1})
    assert deck.side == side_cards


@pytest.mark.deck_add_cards
def test_add_card_multi(new_card, main_cards):
    quantity = 4
    deck = Deck.model_construct(archetype="test_add_card_multi", main=main_cards)
    deck.add_card(card=new_card, quantity=quantity)
    main_cards.update({new_card: quantity})
    assert deck.main == main_cards


@pytest.mark.deck_add_cards
def test_add_cards_main(main_cards):
    deck = Deck.model_construct(archetype="test_add_cards_main", main=main_cards)
    deck.add_cards(cards=main_cards, in_the=InThe.MAIN)
    main_cards.update(main_cards)
    assert deck.main == main_cards


@pytest.mark.deck_add_cards
def test_add_cards_side(side_cards):
    deck = Deck.model_construct(archetype="test_add_cards_side", main=main_cards)
    deck.add_cards(cards=side_cards, in_the=InThe.SIDE)
    assert deck.side == side_cards


@pytest.mark.deck_add_cards
def test_add_cards_main_and_side(main_cards, side_cards):
    deck = Deck.model_construct(archetype="test_add_cards_main_and_side")
    deck.add_cards(cards=main_cards, in_the=InThe.MAIN)
    deck.add_cards(cards=side_cards, in_the=InThe.SIDE)
    assert deck.main == main_cards and deck.side == side_cards


@pytest.mark.deck_add_cards
@pytest.mark.deck_validation
def test_add_cards_side_validation(format, main_cards, side_cards):
    deck = Deck.model_validate(
        {
            "archetype": "test_add_cards_validation",
            "format": format,
            "main": main_cards,
            "side": side_cards,
        }
    )
    with pytest.raises(ValueError) as e:
        deck.add_cards(cards=side_cards, in_the=InThe.SIDE, revalidate_after=True)  # more than 15 in the sideboard


@pytest.mark.deck_add_cards
@pytest.mark.deck_validation
def test_remove_card_main_validation(format, main_cards, existing_card):
    deck = Deck.model_validate(
        {
            "archetype": "test_remove_card_main_validation",
            "format": format,
            "main": main_cards,
        }
    )
    with pytest.raises(ValueError) as e:
        deck.remove_card(
            card=existing_card, quantity=1, in_the=InThe.MAIN, revalidate_after=True
        )  # fewer than 60 in the main


@pytest.mark.deck_remove_cards
def test_remove_card(main_cards, existing_card):
    deck = Deck.model_construct(archetype="test_remove_card", main=main_cards)
    deck.remove_card(card=existing_card, quantity=1)
    main_cards = main_cards - Counter({existing_card: 1})
    assert deck.main == main_cards


@pytest.mark.deck_remove_cards
def test_remove_card_all(main_cards, existing_card):
    deck = Deck.model_construct(archetype="test_remove_card_all", main=main_cards)
    deck.remove_card(card=existing_card)
    main_cards = main_cards - Counter({existing_card: maxsize})
    assert deck.main == main_cards


@pytest.mark.deck_remove_cards
def test_remove_card_side(side_cards, existing_card):
    deck = Deck.model_construct(archetype="test_remove_card_side", side=side_cards)
    deck.remove_card(card=existing_card, quantity=1, in_the=InThe.SIDE)
    side_cards = side_cards - Counter({existing_card: 1})
    assert deck.side == side_cards


@pytest.mark.deck_remove_cards
def test_remove_cards(main_cards):
    double_main = main_cards + main_cards
    deck = Deck.model_construct(archetype="test_remove_cards", main=double_main)
    deck.remove_cards(main_cards)
    assert deck.main == main_cards


@pytest.mark.deck_count
def test_count(main_cards, side_cards):
    deck = Deck.model_construct(archetype="test_count", main=main_cards, side=side_cards)
    assert deck.count() == main_cards.total() + side_cards.total()


@pytest.mark.deck_export
def test_to_decklist_default(main_cards, side_cards, main_string, side_string):
    deck = Deck.model_construct(archetype="test_to_decklist_default", main=main_cards, side=side_cards)
    assert deck.to_decklist() == f"{main_string}\n\n{side_string}"


@pytest.mark.deck_export
def test_to_decklist_no_side(main_cards, main_string):
    deck = Deck.model_construct(archetype="test_to_decklist_no_side", main=main_cards)
    assert deck.to_decklist() == f"{main_string}"


@pytest.mark.deck_export
def test_to_decklist_arena(main_cards, side_cards, main_string, side_string):
    deck = Deck.model_construct(archetype="test_to_decklist_arena", main=main_cards, side=side_cards)
    assert deck.to_decklist(DecklistFormatter.ARENA) == f"{main_string}\n\nSideboard\n{side_string}"


@pytest.mark.deck_export
def test_to_decklist_arena_no_side(main_cards, main_string):
    deck = Deck.model_construct(archetype="test_to_decklist_arena_no_side", main=main_cards)
    assert deck.to_decklist(DecklistFormatter.ARENA) == f"{main_string}"


@pytest.mark.deck_export
def test_to_decklist_mtgo(main_cards, side_cards, main_string, side_string):
    deck = Deck.model_construct(archetype="test_to_decklist_mtgo", main=main_cards, side=side_cards)
    assert deck.to_decklist(DecklistFormatter.MTGO) == f"{main_string}\n\nSIDEBOARD:\n{side_string}"


@pytest.mark.deck_export
def test_to_decklist_mtgo_no_side(main_cards, main_string):
    deck = Deck.model_construct(archetype="test_to_decklist_mtgo_no_side", main=main_cards)
    assert deck.to_decklist(DecklistFormatter.MTGO) == f"{main_string}"
