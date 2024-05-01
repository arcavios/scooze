from collections import Counter
from sys import maxsize

import pytest
from scooze.card import Card
from scooze.cardlist import CardList
from scooze.utils import DictDiff

# region Fixtures


@pytest.fixture
def some_cards(card_chalice_of_the_void, card_hallowed_moonlight, card_veil_of_summer) -> Counter[Card]:
    cards = Counter[Card](
        {
            card_chalice_of_the_void: 4,
            card_hallowed_moonlight: 2,
            card_veil_of_summer: 1,
        }
    )
    return cards


# endregion


def test_no_mutable_defaults():
    card_list_1 = CardList()
    card_list_2 = CardList()
    assert id(card_list_1.cards) != id(card_list_2.cards)


def test_cards(some_cards):
    card_list = CardList(cards=some_cards)
    assert card_list.cards == some_cards


def test_eq(some_cards):
    listA = CardList(cards=some_cards)
    listB = CardList(cards=some_cards)
    assert listA == listB


def test_ne(some_cards):
    listA = CardList(cards=some_cards)
    listB = CardList()
    assert listA != listB


def test_str_empty():
    card_list = CardList()
    assert str(card_list) == ""


def test_str(main_modern_4c, main_modern_4c_str):
    assert str(main_modern_4c) == main_modern_4c_str


def test_total(main_modern_4c):
    assert main_modern_4c.total() == 60


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
    card_list = CardList(cards=some_cards)
    diff = side_modern_4c.diff(card_list)
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


def test_add_card_one(some_cards, card_veil_of_summer):
    card_list = CardList(cards=some_cards)
    card_list.add_card(card=card_veil_of_summer)
    some_cards.update({card_veil_of_summer: 1})
    assert card_list.cards == some_cards


def test_add_card_many(some_cards, card_veil_of_summer):
    card_list = CardList(cards=some_cards)
    card_list.add_card(card=card_veil_of_summer, quantity=3)
    some_cards.update({card_veil_of_summer: 3})
    assert card_list.cards == some_cards


def test_add_cards(some_cards):
    card_list = CardList(cards=some_cards)
    card_list.add_cards(some_cards)
    some_cards.update(some_cards)
    assert card_list.cards == some_cards


def test_remove_card_one(some_cards, card_chalice_of_the_void):
    card_list = CardList(cards=some_cards)
    card_list.remove_card(card=card_chalice_of_the_void, quantity=1)
    some_cards = some_cards - Counter[Card]({card_chalice_of_the_void: 1})
    assert card_list.cards == some_cards


def test_remove_card_many(some_cards, card_chalice_of_the_void):
    card_list = CardList(cards=some_cards)
    card_list.remove_card(card=card_chalice_of_the_void, quantity=3)
    some_cards = some_cards - Counter[Card]({card_chalice_of_the_void: 3})
    assert card_list.cards == some_cards


def test_remove_card_all(some_cards, card_chalice_of_the_void):
    card_list = CardList(cards=some_cards)
    card_list.remove_card(card=card_chalice_of_the_void)
    some_cards = some_cards - Counter[Card]({card_chalice_of_the_void: maxsize})
    assert card_list.cards == some_cards


def test_remove_cards(some_cards):
    card_list = CardList(cards=some_cards)
    card_list.remove_cards(some_cards)
    some_cards = some_cards - some_cards
    assert card_list.cards == some_cards
