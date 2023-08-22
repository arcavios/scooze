from collections import Counter
from sys import maxsize

import pytest
from scooze.card import Card
from scooze.deckpart import DeckPart
from scooze.enums import Color
from scooze.utils import DictDiff


@pytest.fixture
def some_cards(card_chalice_of_the_void, card_hallowed_moonlight, card_veil_of_summer) -> Counter[Card]:
    cards = Counter(
        {
            card_chalice_of_the_void: 4,
            card_hallowed_moonlight: 2,
            card_veil_of_summer: 1,
        }
    )
    return cards


def test_cards(some_cards):
    part = DeckPart(cards=some_cards)
    assert part.cards == some_cards


def test_eq(some_cards):
    partA = DeckPart(cards=some_cards)
    partB = DeckPart(cards=some_cards)
    assert partA == partB


def test_ne(some_cards):
    partA = DeckPart(cards=some_cards)
    partB = DeckPart()
    assert partA != partB


def test_str_empty():
    part = DeckPart()
    assert str(part) == ""


def test_str(main_modern_4c, main_modern_4c_str):
    assert str(main_modern_4c) == main_modern_4c_str


def test_total(main_modern_4c):
    assert main_modern_4c.total() == 60


@pytest.mark.deck_diff
def test_diff(
    side_modern_4c,
    some_cards,
    card_aether_gust,
    card_boseiju_who_endures,
    card_chalice_of_the_void,
    card_dovins_veto,
    card_dress_down,
    card_flusterstorm,
    card_hallowed_moonlight,
    card_kaheera_the_orphanguard,
    card_prismatic_ending,
    card_supreme_verdict,
    card_veil_of_summer,
    card_wear_tear,
):
    part = DeckPart(cards=some_cards)
    diff = side_modern_4c.diff(part)
    assert diff == DictDiff(
        {
            card_aether_gust: (1, 0),
            card_boseiju_who_endures: (1, 0),
            card_chalice_of_the_void: (2, 4),
            card_dovins_veto: (1, 0),
            card_dress_down: (1, 0),
            card_flusterstorm: (1, 0),
            card_kaheera_the_orphanguard: (1, 0),
            card_prismatic_ending: (1, 0),
            card_supreme_verdict: (1, 0),
            card_veil_of_summer: (2, 1),
            card_wear_tear: (1, 0),
        }
    )


@pytest.mark.deck_add_cards
def test_add_card_one(some_cards, card_veil_of_summer):
    part = DeckPart(cards=some_cards)
    part.add_card(card=card_veil_of_summer)
    some_cards.update({card_veil_of_summer: 1})
    assert part.cards == some_cards


@pytest.mark.deck_add_cards
def test_add_card_many(some_cards, card_veil_of_summer):
    part = DeckPart(cards=some_cards)
    part.add_card(card=card_veil_of_summer, quantity=3)
    some_cards.update({card_veil_of_summer: 3})
    assert part.cards == some_cards


@pytest.mark.deck_add_cards
def test_add_cards(some_cards):
    part = DeckPart(cards=some_cards)
    part.add_cards(some_cards)
    some_cards.update(some_cards)
    assert part.cards == some_cards


@pytest.mark.deck_remove_cards
def test_remove_card_one(some_cards, card_chalice_of_the_void):
    part = DeckPart(cards=some_cards)
    part.remove_card(card=card_chalice_of_the_void, quantity=1)
    some_cards = some_cards - Counter({card_chalice_of_the_void: 1})
    assert part.cards == some_cards


@pytest.mark.deck_remove_cards
def test_remove_card_many(some_cards, card_chalice_of_the_void):
    part = DeckPart(cards=some_cards)
    part.remove_card(card=card_chalice_of_the_void, quantity=3)
    some_cards = some_cards - Counter({card_chalice_of_the_void: 3})
    assert part.cards == some_cards


@pytest.mark.deck_remove_cards
def test_remove_card_all(some_cards, card_chalice_of_the_void):
    part = DeckPart(cards=some_cards)
    part.remove_card(card=card_chalice_of_the_void)
    some_cards = some_cards - Counter({card_chalice_of_the_void: maxsize})
    assert part.cards == some_cards


@pytest.mark.deck_remove_cards
def test_remove_cards(some_cards):
    part = DeckPart(cards=some_cards)
    part.remove_cards(some_cards)
    some_cards = some_cards - some_cards
    assert part.cards == some_cards
