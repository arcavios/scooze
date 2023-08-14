from collections import Counter

import pytest
from scooze.data.card import DecklistCard
from scooze.data.deck import Deck
from scooze.data.deckpart import DeckPart
from scooze.enums import DecklistFormatter, InThe


@pytest.fixture
def cards(
    card_boseiju_who_endures,
    card_omnath_locus_of_creation,
    card_prismatic_ending,
) -> Counter[DecklistCard]:
    return Counter(
        {
            card_boseiju_who_endures: 1,
            card_omnath_locus_of_creation: 1,
            card_prismatic_ending: 1,
        }
    )


@pytest.fixture
def cmdr_cards(card_omnath_locus_of_creation, card_supreme_verdict) -> Counter[DecklistCard]:
    return Counter(
        {
            card_omnath_locus_of_creation: 1,
            card_supreme_verdict: 1,
        }
    )


@pytest.fixture
def cmdr_part(cmdr_cards) -> DeckPart:
    return DeckPart(cards=cmdr_cards)


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
def test_diff_cmdr(deck_modern_4c, cmdr_part, card_omnath_locus_of_creation, card_supreme_verdict):
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
            card_omnath_locus_of_creation: (0, 1),
            card_supreme_verdict: (0, 1),
        },
    }


@pytest.mark.deck_add_cards
def test_add_card_main_one(main_modern_4c, card_boseiju_who_endures):
    deck = Deck(archetype="test_add_card_main_one", main=main_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=1, in_the=InThe.MAIN)
    main_modern_4c.add_card(card=card_boseiju_who_endures, quantity=1)
    assert deck.main == main_modern_4c


@pytest.mark.deck_add_cards
def test_add_card_main_many(main_modern_4c, card_boseiju_who_endures):
    deck = Deck(archetype="test_add_card_main_many", main=main_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=2, in_the=InThe.MAIN)
    main_modern_4c.add_card(card=card_boseiju_who_endures, quantity=2)
    assert deck.main == main_modern_4c


@pytest.mark.deck_add_cards
def test_add_card_side_one(side_modern_4c, card_boseiju_who_endures):
    deck = Deck(archetype="test_add_card_side_one", side=side_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=1, in_the=InThe.SIDE)
    side_modern_4c.add_card(card=card_boseiju_who_endures, quantity=1)
    assert deck.side == side_modern_4c


@pytest.mark.deck_add_cards
def test_add_card_side_many(side_modern_4c, card_boseiju_who_endures):
    deck = Deck(archetype="test_add_card_side_many", side=side_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=2, in_the=InThe.SIDE)
    side_modern_4c.add_card(card=card_boseiju_who_endures, quantity=2)
    assert deck.side == side_modern_4c


@pytest.mark.deck_add_cards
def test_add_card_cmdr_one(cmdr_part, card_omnath_locus_of_creation):
    deck = Deck(archetype="test_add_card_cmdr_one", cmdr=cmdr_part)
    deck.add_card(card=card_omnath_locus_of_creation, quantity=1, in_the=InThe.CMDR)
    cmdr_part.add_card(card=card_omnath_locus_of_creation, quantity=1)
    assert deck.cmdr == cmdr_part


@pytest.mark.deck_add_cards
def test_add_card_cmdr_many(cmdr_part, card_omnath_locus_of_creation):
    deck = Deck(archetype="test_add_card_cmdr_many", cmdr=cmdr_part)
    deck.add_card(card=card_omnath_locus_of_creation, quantity=2, in_the=InThe.CMDR)
    cmdr_part.add_card(card=card_omnath_locus_of_creation, quantity=2)
    assert deck.cmdr == cmdr_part


@pytest.mark.deck_add_cards
def test_add_cards_main(main_modern_4c, cards):
    deck = Deck(archetype="test_add_cards_main", main=main_modern_4c)
    deck.add_cards(cards=cards, in_the=InThe.MAIN)
    main_modern_4c.add_cards(cards=cards)
    assert deck.main == main_modern_4c


@pytest.mark.deck_add_cards
def test_add_cards_side(side_modern_4c, cards):
    deck = Deck(archetype="test_add_cards_side", side=side_modern_4c)
    deck.add_cards(cards=cards, in_the=InThe.SIDE)
    side_modern_4c.add_cards(cards=cards)
    assert deck.side == side_modern_4c


@pytest.mark.deck_add_cards
def test_add_cards_cmdr(cmdr_part, cards):
    deck = Deck(archetype="test_add_cards_cmdr", cmdr=cmdr_part)
    deck.add_cards(cards=cards, in_the=InThe.CMDR)
    cmdr_part.add_cards(cards=cards)
    assert deck.cmdr == cmdr_part


@pytest.mark.deck_remove_cards
def test_remove_card_main_one(main_modern_4c, card_boseiju_who_endures):
    deck = Deck(archetype="test_remove_card_main_one", main=main_modern_4c)
    deck.remove_card(card=card_boseiju_who_endures, quantity=1, in_the=InThe.MAIN)
    main_modern_4c.remove_card(card=card_boseiju_who_endures, quantity=1)
    assert deck.main == main_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_main_many(main_modern_4c, card_omnath_locus_of_creation):
    deck = Deck(archetype="test_remove_card_main_many", main=main_modern_4c)
    deck.remove_card(card=card_omnath_locus_of_creation, quantity=2, in_the=InThe.MAIN)
    main_modern_4c.remove_card(card=card_omnath_locus_of_creation, quantity=2)
    assert deck.main == main_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_main_all(main_modern_4c, card_omnath_locus_of_creation):
    deck = Deck(archetype="test_remove_card_main_all", main=main_modern_4c)
    deck.remove_card(card=card_omnath_locus_of_creation, in_the=InThe.MAIN)
    main_modern_4c.remove_card(card=card_omnath_locus_of_creation)
    assert deck.main == main_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_side_one(side_modern_4c, card_chalice_of_the_void):
    deck = Deck(archetype="test_remove_card_side_one", side=side_modern_4c)
    deck.remove_card(card=card_chalice_of_the_void, quantity=1, in_the=InThe.SIDE)
    side_modern_4c.remove_card(card=card_chalice_of_the_void, quantity=1)
    assert deck.side == side_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_side_many(side_modern_4c, card_chalice_of_the_void):
    deck = Deck(archetype="test_remove_card_side_many", side=side_modern_4c)
    deck.remove_card(card=card_chalice_of_the_void, quantity=2, in_the=InThe.SIDE)
    side_modern_4c.remove_card(card=card_chalice_of_the_void, quantity=2)
    assert deck.side == side_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_side_all(side_modern_4c, card_chalice_of_the_void):
    deck = Deck(archetype="test_remove_card_side_all", side=side_modern_4c)
    deck.remove_card(card=card_chalice_of_the_void, in_the=InThe.SIDE)
    side_modern_4c.remove_card(card=card_chalice_of_the_void)
    assert deck.side == side_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_cmdr(cmdr_part, card_omnath_locus_of_creation):
    deck = Deck(archetype="test_remove_card_cmdr", cmdr=cmdr_part)
    deck.remove_card(card=card_omnath_locus_of_creation, quantity=1, in_the=InThe.CMDR)
    cmdr_part.remove_card(card=card_omnath_locus_of_creation, quantity=1)
    assert deck.cmdr == cmdr_part


@pytest.mark.deck_remove_cards
def test_remove_cards_main(main_modern_4c, cards):
    deck = Deck(archetype="test_remove_cards_main", main=main_modern_4c)
    deck.remove_cards(cards=cards, in_the=InThe.MAIN)
    main_modern_4c.remove_cards(cards=cards)
    assert deck.main == main_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_cards_side(side_modern_4c, cards):
    deck = Deck(archetype="test_remove_cards_side", side=side_modern_4c)
    deck.remove_cards(cards=cards, in_the=InThe.SIDE)
    side_modern_4c.remove_cards(cards=cards)
    assert deck.side == side_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_cards_cmdr(cmdr_part, cmdr_cards):
    deck = Deck(archetype="test_remove_cards_cmdr", cmdr=cmdr_part)
    deck.remove_cards(cards=cmdr_cards, in_the=InThe.CMDR)
    cmdr_part.remove_cards(cards=cmdr_cards)
    assert deck.cmdr == cmdr_part


def test_to_decklist_default(deck_modern_4c, main_modern_4c_str, side_modern_4c_str):
    assert deck_modern_4c.to_decklist() == f"{main_modern_4c_str}\n{side_modern_4c_str}"


def test_to_decklist_default_no_side(main_modern_4c, main_modern_4c_str):
    deck = Deck(archetype="test_to_decklist_default_no_side", main=main_modern_4c)
    assert deck.to_decklist() == f"{main_modern_4c_str}"


def test_to_decklist_default_cmdr(main_modern_4c, main_modern_4c_str, cmdr_part):
    deck = Deck(archetype="test_to_decklist_default_cmdr", main=main_modern_4c, cmdr=cmdr_part)
    assert deck.to_decklist() == f"Commander\n{cmdr_part}\n{main_modern_4c_str}"


def test_to_decklist_arena(main_modern_4c, side_modern_4c, main_modern_4c_str, side_modern_4c_str):
    deck = Deck(archetype="test_to_decklist_arena", main=main_modern_4c, side=side_modern_4c)
    assert deck.to_decklist(DecklistFormatter.ARENA) == f"{main_modern_4c_str}\nSideboard\n{side_modern_4c_str}"


def test_to_decklist_mtgo(main_modern_4c, side_modern_4c, main_modern_4c_str, side_modern_4c_str):
    deck = Deck(archetype="test_to_decklist_mtgo", main=main_modern_4c, side=side_modern_4c)
    assert deck.to_decklist(DecklistFormatter.MTGO) == f"{main_modern_4c_str}\nSIDEBOARD:\n{side_modern_4c_str}"
