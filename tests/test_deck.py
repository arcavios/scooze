import math
import re
from collections import Counter
from copy import deepcopy

import pytest
from bson import ObjectId
from scooze.card import OracleCard
from scooze.catalogs import DecklistFormatter, Format, InThe
from scooze.deck import Deck
from scooze.deckpart import DeckDiff, DeckPart
from scooze.models.deck import DeckModel
from scooze.utils import DictDiff

# region Fixtures


@pytest.fixture
def cards(
    card_boseiju_who_endures,
    card_omnath_locus_of_creation,
    card_prismatic_ending,
) -> Counter[OracleCard]:
    return Counter[OracleCard](
        {
            card_boseiju_who_endures: 1,
            card_omnath_locus_of_creation: 1,
            card_prismatic_ending: 1,
        }
    )


@pytest.fixture
def cmdr_cards(card_omnath_locus_of_creation, card_supreme_verdict) -> Counter[OracleCard]:
    return Counter[OracleCard](
        {
            card_omnath_locus_of_creation: 1,
            card_supreme_verdict: 1,
        }
    )


@pytest.fixture
def cmdr_part(cmdr_cards) -> DeckPart[OracleCard]:
    return DeckPart[OracleCard](cards=cmdr_cards)


@pytest.fixture
def dictdiff_empty() -> DictDiff:
    return DictDiff(contents={})


@pytest.fixture
def power9_object_ids() -> Counter[ObjectId]:
    return Counter(
        {
            ObjectId("6517e3abf15f7b84861971c9"): 1,
            ObjectId("6517e3abf15f7b84861971ca"): 1,
            ObjectId("6517e3abf15f7b84861971cb"): 1,
            ObjectId("6517e3abf15f7b84861971cc"): 1,
            ObjectId("6517e3abf15f7b84861971cd"): 1,
            ObjectId("6517e3abf15f7b84861971ce"): 1,
            ObjectId("6517e3abf15f7b84861971cf"): 1,
            ObjectId("6517e3abf15f7b84861971d0"): 1,
            ObjectId("6517e3abf15f7b84861971d1"): 1,
        }
    )


# endregion


# TODO: testing normalizers and lookups on ID this has to be mocked before this can be merged.
# TODO: write tests for date_played
def test_card_lookup_by_id(power9_object_ids):
    model = DeckModel(main=power9_object_ids)
    print(model.model_dump())
    deck = Deck.from_model(model)
    print(deck.export())


# region Magic Methods

# region Init


def test_archetype(archetype_modern_4c):
    deck = Deck[OracleCard](archetype=archetype_modern_4c)
    assert deck.archetype == archetype_modern_4c


def test_format():
    deck = Deck[OracleCard](archetype="test_format", format=Format.MODERN)
    assert deck.format is Format.MODERN


def test_main(main_modern_4c):
    deck = Deck[OracleCard](archetype="test_main", main=main_modern_4c)
    assert deck.main == main_modern_4c


def test_side(side_modern_4c):
    deck = Deck[OracleCard](archetype="test_main", side=side_modern_4c)
    assert deck.side == side_modern_4c


def test_cmdr(cmdr_part):
    deck = Deck[OracleCard](archetype="test_cmdr", cmdr=cmdr_part)
    assert deck.cmdr == cmdr_part


# endregion


def test_eq(deck_modern_4c):
    deck = deepcopy(deck_modern_4c)
    assert deck == deck_modern_4c


def test_eq_after_add_card(deck_modern_4c, card_kaheera_the_orphanguard):
    deck = deepcopy(deck_modern_4c)
    deck.add_card(card_kaheera_the_orphanguard)
    deck_modern_4c.add_card(card_kaheera_the_orphanguard)
    assert deck == deck_modern_4c


# endregion


def test_average_cmc(deck_modern_4c):
    # 141 / 75
    assert math.isclose(deck_modern_4c.average_cmc(), 1.88)


def test_average_words(deck_modern_4c):
    # 2118 / 75
    assert math.isclose(deck_modern_4c.average_words(), 28.24)


@pytest.mark.deck_diff
def test_diff_none(deck_modern_4c, dictdiff_empty):
    assert deck_modern_4c.diff(deck_modern_4c) == DeckDiff(
        main=dictdiff_empty, side=dictdiff_empty, cmdr=dictdiff_empty
    )


@pytest.mark.deck_diff
def test_diff_main(deck_modern_4c, card_kaheera_the_orphanguard, dictdiff_empty):
    other = deepcopy(deck_modern_4c)
    other.add_card(card=card_kaheera_the_orphanguard, quantity=1, in_the=InThe.MAIN)
    assert deck_modern_4c.diff(other) == DeckDiff(
        main=DictDiff({card_kaheera_the_orphanguard: (0, 1)}),
        side=dictdiff_empty,
        cmdr=dictdiff_empty,
    )


@pytest.mark.deck_diff
def test_diff_side(deck_modern_4c, card_kaheera_the_orphanguard, dictdiff_empty):
    other = deepcopy(deck_modern_4c)
    other.add_card(card=card_kaheera_the_orphanguard, quantity=1, in_the=InThe.SIDE)
    assert deck_modern_4c.diff(other) == DeckDiff(
        main=dictdiff_empty,
        side=DictDiff({card_kaheera_the_orphanguard: (1, 2)}),
        cmdr=dictdiff_empty,
    )


@pytest.mark.deck_diff
def test_diff_cmdr(deck_modern_4c, cmdr_part, card_omnath_locus_of_creation, card_supreme_verdict, dictdiff_empty):
    other = Deck[OracleCard](
        archetype=deck_modern_4c.archetype,
        format=deck_modern_4c.format,
        main=deck_modern_4c.main,
        side=deck_modern_4c.side,
        cmdr=cmdr_part,
    )
    assert deck_modern_4c.diff(other) == DeckDiff(
        main=dictdiff_empty,
        side=dictdiff_empty,
        cmdr=DictDiff(
            {
                card_omnath_locus_of_creation: (0, 1),
                card_supreme_verdict: (0, 1),
            }
        ),
    )


def test_decklist_equals(deck_modern_4c, main_modern_4c, side_modern_4c, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](
        archetype="test_decklist_equals",
        format=Format.NONE,
        main=deepcopy(main_modern_4c),
        side=deepcopy(side_modern_4c),
    )
    assert deck.archetype != deck_modern_4c.archetype
    assert deck.decklist_equals(deck_modern_4c)

    deck.add_card(card=card_omnath_locus_of_creation)
    assert not deck.decklist_equals(deck_modern_4c)


def test_export_default(deck_modern_4c, main_modern_4c_str, side_modern_4c_str):
    assert deck_modern_4c.export() == f"{main_modern_4c_str}\nSideboard\n{side_modern_4c_str}"


def test_export_default_no_side(main_modern_4c, main_modern_4c_str):
    deck = Deck[OracleCard](archetype="test_export_default_no_side", main=main_modern_4c)
    assert deck.export() == f"{main_modern_4c_str}"


def test_export_default_cmdr(main_modern_4c, main_modern_4c_str, cmdr_part):
    deck = Deck[OracleCard](archetype="test_export_default_cmdr", main=main_modern_4c, cmdr=cmdr_part)
    assert deck.export() == f"Commander\n{cmdr_part}\n{main_modern_4c_str}"


def test_export_arena(main_modern_4c, side_modern_4c, main_modern_4c_str, side_modern_4c_str):
    deck = Deck[OracleCard](archetype="test_export_arena", main=main_modern_4c, side=side_modern_4c)
    assert deck.export(DecklistFormatter.ARENA) == f"{main_modern_4c_str}\nSideboard\n{side_modern_4c_str}"


def test_export_mtgo(main_modern_4c, side_modern_4c, main_modern_4c_str, side_modern_4c_str):
    deck = Deck[OracleCard](archetype="test_export_mtgo", main=main_modern_4c, side=side_modern_4c)
    assert deck.export(DecklistFormatter.MTGO) == f"{main_modern_4c_str}\nSIDEBOARD:\n{side_modern_4c_str}"


def test_is_legal(deck_modern_4c):
    assert not deck_modern_4c.is_legal(Format.ALCHEMY)
    assert not deck_modern_4c.is_legal(Format.BRAWL)
    assert not deck_modern_4c.is_legal(Format.COMMANDER)
    assert not deck_modern_4c.is_legal(Format.DUEL)
    assert not deck_modern_4c.is_legal(Format.EXPLORER)
    assert not deck_modern_4c.is_legal(Format.FUTURE)
    assert not deck_modern_4c.is_legal(Format.GLADIATOR)
    assert not deck_modern_4c.is_legal(Format.HISTORIC)
    assert not deck_modern_4c.is_legal(Format.HISTORICBRAWL)
    assert not deck_modern_4c.is_legal(Format.LEGACY)
    assert deck_modern_4c.is_legal(Format.LIMITED)
    assert deck_modern_4c.is_legal(Format.MODERN)
    assert deck_modern_4c.is_legal(Format.NONE)
    assert not deck_modern_4c.is_legal(Format.OATHBREAKER)
    assert not deck_modern_4c.is_legal(Format.OLDSCHOOL)
    assert not deck_modern_4c.is_legal(Format.PAUPER)
    assert not deck_modern_4c.is_legal(Format.PAUPERCOMMANDER)
    assert not deck_modern_4c.is_legal(Format.PENNY)
    assert not deck_modern_4c.is_legal(Format.PIONEER)
    assert not deck_modern_4c.is_legal(Format.PREDH)
    assert not deck_modern_4c.is_legal(Format.PREMODERN)
    assert not deck_modern_4c.is_legal(Format.STANDARD)
    assert not deck_modern_4c.is_legal(Format.VINTAGE)

    assert deck_modern_4c.is_legal()  # self.format
    deck_modern_4c.format = None
    assert deck_modern_4c.is_legal()  # format = None


def test_total_cards(deck_modern_4c):
    assert deck_modern_4c.total_cards() == 75


def test_total_cmc(deck_modern_4c):
    assert deck_modern_4c.total_cmc() == 141


def test_total_words(deck_modern_4c):
    assert deck_modern_4c.total_words() == 2118


# region Mutating Methods


@pytest.mark.deck_add_cards
def test_add_card_main_one(main_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_add_card_main_one", main=main_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=1, in_the=InThe.MAIN)
    main_modern_4c.add_card(card=card_boseiju_who_endures, quantity=1)
    assert deck.main == main_modern_4c


@pytest.mark.deck_add_cards
def test_add_card_main_many(main_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_add_card_main_many", main=main_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=2, in_the=InThe.MAIN)
    main_modern_4c.add_card(card=card_boseiju_who_endures, quantity=2)
    assert deck.main == main_modern_4c


@pytest.mark.deck_add_cards
def test_add_card_side_one(side_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_add_card_side_one", side=side_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=1, in_the=InThe.SIDE)
    side_modern_4c.add_card(card=card_boseiju_who_endures, quantity=1)
    assert deck.side == side_modern_4c


@pytest.mark.deck_add_cards
def test_add_card_side_many(side_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_add_card_side_many", side=side_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=2, in_the=InThe.SIDE)
    side_modern_4c.add_card(card=card_boseiju_who_endures, quantity=2)
    assert deck.side == side_modern_4c


@pytest.mark.deck_add_cards
def test_add_card_cmdr_one(cmdr_part, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_add_card_cmdr_one", cmdr=cmdr_part)
    deck.add_card(card=card_omnath_locus_of_creation, quantity=1, in_the=InThe.CMDR)
    cmdr_part.add_card(card=card_omnath_locus_of_creation, quantity=1)
    assert deck.cmdr == cmdr_part


@pytest.mark.deck_add_cards
def test_add_card_cmdr_many(cmdr_part, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_add_card_cmdr_many", cmdr=cmdr_part)
    deck.add_card(card=card_omnath_locus_of_creation, quantity=2, in_the=InThe.CMDR)
    cmdr_part.add_card(card=card_omnath_locus_of_creation, quantity=2)
    assert deck.cmdr == cmdr_part


@pytest.mark.deck_add_cards
def test_add_cards_main(main_modern_4c, cards):
    deck = Deck[OracleCard](archetype="test_add_cards_main", main=main_modern_4c)
    deck.add_cards(cards=cards, in_the=InThe.MAIN)
    main_modern_4c.add_cards(cards=cards)
    assert deck.main == main_modern_4c


@pytest.mark.deck_add_cards
def test_add_cards_side(side_modern_4c, cards):
    deck = Deck[OracleCard](archetype="test_add_cards_side", side=side_modern_4c)
    deck.add_cards(cards=cards, in_the=InThe.SIDE)
    side_modern_4c.add_cards(cards=cards)
    assert deck.side == side_modern_4c


@pytest.mark.deck_add_cards
def test_add_cards_cmdr(cmdr_part, cards):
    deck = Deck[OracleCard](archetype="test_add_cards_cmdr", cmdr=cmdr_part)
    deck.add_cards(cards=cards, in_the=InThe.CMDR)
    cmdr_part.add_cards(cards=cards)
    assert deck.cmdr == cmdr_part


@pytest.mark.deck_remove_cards
def test_remove_card_main_one(main_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_remove_card_main_one", main=main_modern_4c)
    deck.remove_card(card=card_boseiju_who_endures, quantity=1, in_the=InThe.MAIN)
    main_modern_4c.remove_card(card=card_boseiju_who_endures, quantity=1)
    assert deck.main == main_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_main_many(main_modern_4c, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_remove_card_main_many", main=main_modern_4c)
    deck.remove_card(card=card_omnath_locus_of_creation, quantity=2, in_the=InThe.MAIN)
    main_modern_4c.remove_card(card=card_omnath_locus_of_creation, quantity=2)
    assert deck.main == main_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_main_all(main_modern_4c, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_remove_card_main_all", main=main_modern_4c)
    deck.remove_card(card=card_omnath_locus_of_creation, in_the=InThe.MAIN)
    main_modern_4c.remove_card(card=card_omnath_locus_of_creation)
    assert deck.main == main_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_side_one(side_modern_4c, card_chalice_of_the_void):
    deck = Deck[OracleCard](archetype="test_remove_card_side_one", side=side_modern_4c)
    deck.remove_card(card=card_chalice_of_the_void, quantity=1, in_the=InThe.SIDE)
    side_modern_4c.remove_card(card=card_chalice_of_the_void, quantity=1)
    assert deck.side == side_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_side_many(side_modern_4c, card_chalice_of_the_void):
    deck = Deck[OracleCard](archetype="test_remove_card_side_many", side=side_modern_4c)
    deck.remove_card(card=card_chalice_of_the_void, quantity=2, in_the=InThe.SIDE)
    side_modern_4c.remove_card(card=card_chalice_of_the_void, quantity=2)
    assert deck.side == side_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_side_all(side_modern_4c, card_chalice_of_the_void):
    deck = Deck[OracleCard](archetype="test_remove_card_side_all", side=side_modern_4c)
    deck.remove_card(card=card_chalice_of_the_void, in_the=InThe.SIDE)
    side_modern_4c.remove_card(card=card_chalice_of_the_void)
    assert deck.side == side_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_card_cmdr(cmdr_part, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_remove_card_cmdr", cmdr=cmdr_part)
    deck.remove_card(card=card_omnath_locus_of_creation, quantity=1, in_the=InThe.CMDR)
    cmdr_part.remove_card(card=card_omnath_locus_of_creation, quantity=1)
    assert deck.cmdr == cmdr_part


@pytest.mark.deck_remove_cards
def test_remove_cards_main(main_modern_4c, cards):
    deck = Deck[OracleCard](archetype="test_remove_cards_main", main=main_modern_4c)
    deck.remove_cards(cards=cards, in_the=InThe.MAIN)
    main_modern_4c.remove_cards(cards=cards)
    assert deck.main == main_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_cards_side(side_modern_4c, cards):
    deck = Deck[OracleCard](archetype="test_remove_cards_side", side=side_modern_4c)
    deck.remove_cards(cards=cards, in_the=InThe.SIDE)
    side_modern_4c.remove_cards(cards=cards)
    assert deck.side == side_modern_4c


@pytest.mark.deck_remove_cards
def test_remove_cards_cmdr(cmdr_part, cmdr_cards):
    deck = Deck[OracleCard](archetype="test_remove_cards_cmdr", cmdr=cmdr_part)
    deck.remove_cards(cards=cmdr_cards, in_the=InThe.CMDR)
    cmdr_part.remove_cards(cards=cmdr_cards)
    assert deck.cmdr == cmdr_part


# endregion
