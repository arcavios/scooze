import json
from collections import Counter

import pendulum
import pytest
from pydantic_core import ValidationError
from scooze.models.card import Card
from scooze.models.deck import Deck, InThe
from scooze.models.utils import DecklistFormatter, Format

# region Fixtures


@pytest.fixture
def archetype() -> str:
    return "Amulet Titan"


@pytest.fixture
def format() -> Format:
    return Format.MODERN


@pytest.fixture
def today() -> pendulum.DateTime:
    return pendulum.today("UTC")


@pytest.fixture
def existing_card() -> str:
    return Card.model_validate(
        {
            "name": "Expedition Map",
            "manaValue": 1,
        }
    )


@pytest.fixture
def new_card() -> str:
    return Card.model_validate(
        {
            "name": "Primeval Titan",
            "manaValue": 6,
        }
    )


@pytest.fixture
def main_string() -> str:
    return "1 Expedition Map\n2 Boseiju, Who Endures\n57 Forest"


@pytest.fixture
def main_cards() -> Counter:
    main_cards = Counter(
        {
            Card.model_validate({"name": "Expedition Map", "manaValue": 1}): 1,
            Card.model_validate({"name": "Boseiju, Who Endures", "manaValue": 0}): 2,
            Card.model_validate({"name": "Forest", "manaValue": 0}): 57,
        }
    )
    return main_cards


@pytest.fixture
def side_string() -> str:
    return "1 Pithing Needle\n2 Trail of Crumbs\n11 Forest"


@pytest.fixture
def side_cards() -> Counter:
    side_cards = Counter(
        {
            Card.model_validate({"name": "Pithing Needle", "manaValue": 1}): 1,
            Card.model_validate({"name": "Trail of Crumbs", "manaValue": 2}): 2,
            Card.model_validate({"name": "Forest", "manaValue": 0}): 11,
        }
    )
    return side_cards


# endregion


def test_archetype(archetype):
    deck = Deck.model_validate({"archetype": archetype})
    assert deck.archetype == archetype


def test_format(format, main_cards):
    deck = Deck.model_validate({"format": format, "main": main_cards})
    assert deck.format == format


@pytest.mark.deck_validation
def test_format_validation(format, main_cards):
    with pytest.raises(ValueError) as e:
        Deck.model_validate({"archetype": "test_format_validation", "format": "not a real format"})


def test_date_played(today):
    deck = Deck.model_validate({"datePlayed": today})
    assert deck.date_played == today


@pytest.mark.deck_add_cards
def test_add_card_new(new_card, main_cards):
    deck = Deck.model_validate({"archetype": "test_add_card_new", "main": main_cards})
    deck.add_card(card=new_card)
    main_cards.update({new_card: 1})
    assert deck.main == main_cards


@pytest.mark.deck_add_cards
def test_add_card_side(existing_card, main_cards, side_cards):
    deck = Deck.model_validate({"archetype": "test_add_card_side", "main": main_cards, "side": side_cards})
    deck.add_card(card=existing_card, in_the=InThe.SIDE)
    side_cards.update({existing_card: 1})
    assert deck.side == side_cards


@pytest.mark.deck_add_cards
def test_add_card_multi(new_card, main_cards):
    quantity = 4
    deck = Deck.model_validate({"archetype": "test_add_card_multi", "main": main_cards})
    deck.add_card(card=new_card, quantity=quantity)
    main_cards.update({new_card: quantity})
    assert deck.main == main_cards


@pytest.mark.deck_add_cards
def test_add_cards_main(main_cards):
    deck = Deck.model_validate({"archetype": "test_add_cards_main", "main": main_cards})
    deck.add_cards(cards=main_cards, in_the=InThe.MAIN)
    main_cards.update(main_cards)
    assert deck.main == main_cards


@pytest.mark.deck_add_cards
def test_add_cards_side(main_cards, side_cards):
    deck = Deck.model_validate({"archetype": "test_add_cards_side", "main": main_cards})
    deck.add_cards(cards=side_cards, in_the=InThe.SIDE)
    assert deck.side == side_cards


@pytest.mark.deck_add_cards
def test_add_cards_main_and_side(main_cards, side_cards):
    deck = Deck.model_validate({"archetype": "test_add_cards_main_and_side"})
    deck.add_cards(cards=main_cards, in_the=InThe.MAIN)
    deck.add_cards(cards=side_cards, in_the=InThe.SIDE)
    assert deck.main == main_cards and deck.side == side_cards


@pytest.mark.deck_add_cards
@pytest.mark.deck_validation
def test_remove_card_main_validation(format, main_cards, existing_card):
    deck = Deck.model_validate({"archetype": "test_add_cards_validation", "format": format, "main": main_cards})
    with pytest.raises(ValueError) as e:
        deck.add_card(card=existing_card, quantity=-1, in_the=InThe.MAIN)  # fewer than 60 in the main


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
        deck.add_cards(cards=side_cards, in_the=InThe.SIDE)  # more than 15 in the sideboard


@pytest.mark.deck_count
def test_count(main_cards, side_cards):
    deck = Deck.model_validate({"archetype": "test_count", "main": main_cards, "side": side_cards})
    assert deck.count() == main_cards.total() + side_cards.total()


@pytest.mark.deck_export
def test_to_decklist_default(main_cards, side_cards, main_string, side_string):
    deck = Deck.model_validate({"archetype": "test_to_decklist_default", "main": main_cards, "side": side_cards})
    assert deck.to_decklist() == f"{main_string}\n\n{side_string}"


@pytest.mark.deck_export
def test_to_decklist_no_side(main_cards, main_string):
    deck = Deck.model_validate({"archetype": "test_to_decklist_no_side", "main": main_cards})
    assert deck.to_decklist() == f"{main_string}"


@pytest.mark.deck_export
def test_to_decklist_arena(main_cards, side_cards, main_string, side_string):
    deck = Deck.model_validate({"archetype": "test_to_decklist_arena", "main": main_cards, "side": side_cards})
    assert deck.to_decklist(DecklistFormatter.ARENA) == f"{main_string}\n\nSideboard\n{side_string}"


@pytest.mark.deck_export
def test_to_decklist_mtgo(main_cards, side_cards, main_string, side_string):
    deck = Deck.model_validate({"archetype": "test_to_decklist_mtgo", "main": main_cards, "side": side_cards})
    assert deck.to_decklist(DecklistFormatter.MTGO) == f"{main_string}\n\nSIDEBOARD:\n{side_string}"
