from collections import Counter

import pytest
from scooze.data.card import DecklistCard
from scooze.data.deck import Deck, DeckPart
from scooze.enums import InThe


@pytest.fixture
def cmdr_card(card_omnath_locus_of_creation) -> DecklistCard:
    return card_omnath_locus_of_creation


@pytest.fixture
def cmdr_part(cmdr_card) -> DeckPart:
    cards = Counter({cmdr_card: 1})
    return DeckPart(cards=cards)


def test_archetype(archetype_modern_4c):
    deck = Deck(archetype=archetype_modern_4c)
    assert deck.archetype == archetype_modern_4c


def test_format(format_modern):
    deck = Deck(archetype="test_format", format=format_modern)
    assert deck.format == format_modern


def test_main(main_modern_4c):
    deck = Deck(archetype="test_main", main=main_modern_4c)
    assert deck.main == main_modern_4c


def test_side(side_modern_4c):
    deck = Deck(archetype="test_main", side=side_modern_4c)
    assert deck.side == side_modern_4c


def test_cmdr(cmdr_part):
    deck = Deck(archetype="test_cmdr", cmdr=cmdr_part)
    assert deck.cmdr == cmdr_part


def test_total(deck_modern_4c):
    assert deck_modern_4c.total() == 75


@pytest.mark.deck_diff
def test_diff_none(deck_modern_4c):
    assert deck_modern_4c.diff(deck_modern_4c) == {"main_diff": {}, "side_diff": {}, "cmdr_diff": {}}


@pytest.mark.deck_diff
def test_diff_main(deck_modern_4c, card_kaheera_the_orphanguard):
    other = Deck(
        archetype=deck_modern_4c.archetype,
        format=deck_modern_4c.format,
        main=deck_modern_4c.main,
        side=deck_modern_4c.side,
    )  # TODO(#66): replace with __copy__ or __deepcopy__
    other.add_card(card=card_kaheera_the_orphanguard, quantity=1, in_the=InThe.MAIN)
    assert deck_modern_4c.diff(other) == {
        "main_diff": {
            card_kaheera_the_orphanguard: (0, 1),
        },
        "side_diff": {},
        "cmdr_diff": {},
    }


@pytest.mark.deck_diff
def test_diff_side(deck_modern_4c, card_kaheera_the_orphanguard):
    other = Deck(
        archetype=deck_modern_4c.archetype,
        format=deck_modern_4c.format,
        main=deck_modern_4c.main,
        side=deck_modern_4c.side,
    )  # TODO(#66): replace with __copy__ or __deepcopy__
    other.add_card(card=card_kaheera_the_orphanguard, quantity=1, in_the=InThe.SIDE)
    assert deck_modern_4c.diff(other) == {
        "main_diff": {},
        "side_diff": {
            card_kaheera_the_orphanguard: (1, 2),
        },
        "cmdr_diff": {},
    }


@pytest.mark.deck_diff
def test_diff_cmdr(deck_modern_4c, cmdr_part, cmdr_card):
    other = Deck(
        archetype=deck_modern_4c.archetype,
        format=deck_modern_4c.format,
        main=deck_modern_4c.main,
        side=deck_modern_4c.side,
        cmdr=cmdr_part,
    )  # TODO(#66): replace with __copy__ or __deepcopy__
    assert deck_modern_4c.diff(other) == {
        "main_diff": {},
        "side_diff": {},
        "cmdr_diff": {
            cmdr_card: (0, 1),
        },
    }

# TODO: UPDATE THESE TESTS

@pytest.mark.deck_add_cards
def test_add_card_main_one():
    pass

@pytest.mark.deck_add_cards
def test_add_card_main_many():
    pass

@pytest.mark.deck_add_cards
def test_add_card_side_one():
    pass

@pytest.mark.deck_add_cards
def test_add_card_side_many():
    pass

@pytest.mark.deck_add_cards
def test_add_card_side_one():
    pass

@pytest.mark.deck_add_cards
def test_add_card_side_many():
    pass

@pytest.mark.deck_add_cards
def test_add_cards_main():
    pass

@pytest.mark.deck_add_cards
def test_add_cards_side():
    pass

@pytest.mark.deck_add_cards
def test_add_cards_cmdr():
    pass

@pytest.mark.deck_remove_cards
def test_remove_card_main_one():
    pass

@pytest.mark.deck_remove_cards
def test_remove_card_main_many():
    pass

@pytest.mark.deck_remove_cards
def test_remove_card_main_all():
    pass

@pytest.mark.deck_remove_cards
def test_remove_card_side_one():
    pass

@pytest.mark.deck_remove_cards
def test_remove_card_side_many():
    pass

@pytest.mark.deck_remove_cards
def test_remove_card_side_all():
    pass

@pytest.mark.deck_remove_cards
def test_remove_card_cmdr():
    pass

@pytest.mark.deck_remove_cards
def test_remove_cards_main():
    pass

@pytest.mark.deck_remove_cards
def test_remove_cards_side():
    pass

@pytest.mark.deck_remove_cards
def test_remove_cards_cmdr():
    pass


# TODO: decklist requires, main, side, cmdr, and various DecklistFormats
def test_to_decklist():
    pass

# @pytest.mark.deck_export
# def test_to_decklist_default(main_cards, side_cards, main_string, side_string):
#     deck = Deck(archetype="test_to_decklist_default", main=main_cards, side=side_cards)
#     assert deck.to_decklist() == f"{main_string}\n\n{side_string}"


# @pytest.mark.deck_export
# def test_to_decklist_no_side(main_cards, main_string):
#     deck = Deck(archetype="test_to_decklist_no_side", main=main_cards)
#     assert deck.to_decklist() == f"{main_string}"


# @pytest.mark.deck_export
# def test_to_decklist_arena(main_cards, side_cards, main_string, side_string):
#     deck = Deck(archetype="test_to_decklist_arena", main=main_cards, side=side_cards)
#     assert deck.to_decklist(DecklistFormatter.ARENA) == f"{main_string}\n\nSideboard\n{side_string}"


# @pytest.mark.deck_export
# def test_to_decklist_mtgo(main_cards, side_cards, main_string, side_string):
#     deck = Deck(archetype="test_to_decklist_mtgo", main=main_cards, side=side_cards)
#     assert deck.to_decklist(DecklistFormatter.MTGO) == f"{main_string}\n\nSIDEBOARD:\n{side_string}"
