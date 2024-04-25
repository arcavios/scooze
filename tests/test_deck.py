import math
from collections import Counter
from copy import deepcopy

import pytest
from scooze.card import OracleCard
from scooze.cardlist import CardList
from scooze.catalogs import Format
from scooze.deck import Deck, DeckDiff, DecklistFormatter, InThe
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
def cmdr_part(cmdr_cards) -> CardList[OracleCard]:
    return CardList[OracleCard](cards=cmdr_cards)


@pytest.fixture
def attraction_cards(
    attraction_balloon_stand,
    attraction_bounce_chamber,
    attraction_bumper_cars,
    attraction_clown_extruder,
    attraction_concession_stand,
    attraction_costume_shop,
    attraction_drop_tower,
    attraction_ferris_wheel,
    attraction_foam_weapons_kiosk,
    attraction_fortune_teller,
) -> Counter[OracleCard]:
    return Counter[OracleCard](
        {
            attraction_balloon_stand: 1,
            attraction_bounce_chamber: 1,
            attraction_bumper_cars: 1,
            attraction_clown_extruder: 1,
            attraction_concession_stand: 1,
            attraction_costume_shop: 1,
            attraction_drop_tower: 1,
            attraction_ferris_wheel: 1,
            attraction_foam_weapons_kiosk: 1,
            attraction_fortune_teller: 1,
        }
    )


@pytest.fixture
def attraction_part(attraction_cards) -> CardList[OracleCard]:
    return CardList[OracleCard](cards=attraction_cards)


@pytest.fixture
def sticker_cards(
    sticker_ancestral_hotdog_minotaur,
    sticker_carnival_elephant_meteor,
    sticker_contortionist_otter_storm,
    sticker_cool_fluffy_loxodon,
    sticker_cursed_firebreathing_yogurt,
    sticker_deepfried_plague_myr,
    sticker_demonic_tourist_laser,
    sticker_eldrazi_guacamole_tightrope,
    sticker_elemental_time_flamingo,
    sticker_eternal_acrobat_toast,
) -> Counter[OracleCard]:
    return Counter[OracleCard](
        {
            sticker_ancestral_hotdog_minotaur: 1,
            sticker_carnival_elephant_meteor: 1,
            sticker_contortionist_otter_storm: 1,
            sticker_cool_fluffy_loxodon: 1,
            sticker_cursed_firebreathing_yogurt: 1,
            sticker_deepfried_plague_myr: 1,
            sticker_demonic_tourist_laser: 1,
            sticker_eldrazi_guacamole_tightrope: 1,
            sticker_elemental_time_flamingo: 1,
            sticker_eternal_acrobat_toast: 1,
        }
    )


@pytest.fixture
def sticker_part(sticker_cards) -> CardList[OracleCard]:
    return CardList[OracleCard](cards=sticker_cards)


@pytest.fixture
def dictdiff_empty() -> DictDiff:
    return DictDiff(contents={})


# endregion

# region Magic Methods

# region Init


def test_no_mutable_defaults():
    deck_1 = Deck()
    deck_2 = Deck()
    assert id(deck_1.main) != id(deck_2.main)
    assert id(deck_1.side) != id(deck_2.side)
    assert id(deck_1.cmdr) != id(deck_2.cmdr)


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


def test_diff_none(deck_modern_4c, dictdiff_empty):
    assert deck_modern_4c.diff(deck_modern_4c) == DeckDiff(main=dictdiff_empty)


def test_diff_main(deck_modern_4c, card_kaheera_the_orphanguard):
    other = deepcopy(deck_modern_4c)
    other.add_card(card=card_kaheera_the_orphanguard, quantity=1, in_the=InThe.MAIN)
    assert deck_modern_4c.diff(other) == DeckDiff(
        main=DictDiff({card_kaheera_the_orphanguard: (0, 1)}),
    )


def test_diff_side(deck_modern_4c, card_kaheera_the_orphanguard, dictdiff_empty):
    other = deepcopy(deck_modern_4c)
    other.add_card(card=card_kaheera_the_orphanguard, quantity=1, in_the=InThe.SIDE)
    assert deck_modern_4c.diff(other) == DeckDiff(
        main=dictdiff_empty,
        side=DictDiff({card_kaheera_the_orphanguard: (1, 2)}),
    )


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
    assert deck_modern_4c.export() == f"Deck:\n{main_modern_4c_str}\nSideboard:\n{side_modern_4c_str}"


def test_export_default_no_side(main_modern_4c, main_modern_4c_str):
    deck = Deck[OracleCard](archetype="test_export_default_no_side", main=main_modern_4c)
    assert deck.export() == f"Deck:\n{main_modern_4c_str}"


def test_export_default_cmdr(main_modern_4c, main_modern_4c_str, cmdr_part):
    deck = Deck[OracleCard](archetype="test_export_default_cmdr", main=main_modern_4c, cmdr=cmdr_part)
    assert deck.export() == f"Commander(s):\n{cmdr_part}\nDeck:\n{main_modern_4c_str}"


def test_export_default_attractions(main_modern_4c, main_modern_4c_str, attraction_part):
    deck = Deck[OracleCard](
        archetype="test_export_default_attractions", main=main_modern_4c, attractions=attraction_part
    )
    assert deck.export() == f"Deck:\n{main_modern_4c_str}\nAttractions:\n{attraction_part}"


def test_export_default_stickers(main_modern_4c, main_modern_4c_str, sticker_part):
    deck = Deck[OracleCard](archetype="test_export_default_attractions", main=main_modern_4c, stickers=sticker_part)
    assert deck.export() == f"Deck:\n{main_modern_4c_str}\nStickers:\n{sticker_part}"


def test_export_arena(main_modern_4c, side_modern_4c, main_modern_4c_str, side_modern_4c_str):
    deck = Deck[OracleCard](archetype="test_export_arena", main=main_modern_4c, side=side_modern_4c)
    assert deck.export(DecklistFormatter.ARENA) == f"Deck\n{main_modern_4c_str}\nSideboard\n{side_modern_4c_str}"


def test_export_arena_companion(
    main_modern_4c, side_modern_4c, main_modern_4c_str, side_modern_4c_str, card_kaheera_the_orphanguard
):
    deck = Deck[OracleCard](
        archetype="test_export_arena", main=main_modern_4c, side=side_modern_4c, companion=card_kaheera_the_orphanguard
    )
    assert (
        deck.export(DecklistFormatter.ARENA)
        == f"Companion\n{card_kaheera_the_orphanguard.name}\nDeck\n{main_modern_4c_str}\nSideboard\n{side_modern_4c_str}"
    )


def test_export_arena_companion(main_modern_4c, side_modern_4c, main_modern_4c_str, side_modern_4c_str, cmdr_part):
    deck = Deck[OracleCard](archetype="test_export_arena", main=main_modern_4c, side=side_modern_4c, cmdr=cmdr_part)
    assert (
        deck.export(DecklistFormatter.ARENA)
        == f"Commander\n{cmdr_part}\nDeck\n{main_modern_4c_str}\nSideboard\n{side_modern_4c_str}"
    )


def test_export_mtgo(main_modern_4c, side_modern_4c, main_modern_4c_str, side_modern_4c_str):
    deck = Deck[OracleCard](archetype="test_export_mtgo", main=main_modern_4c, side=side_modern_4c)
    assert deck.export(DecklistFormatter.MTGO) == f"{main_modern_4c_str}\n{side_modern_4c_str}"


def test_export_mtgo_cmdr(main_modern_4c, main_modern_4c_str, cmdr_part):
    deck = Deck[OracleCard](archetype="test_export_mtgo", main=main_modern_4c, cmdr=cmdr_part)
    assert deck.export(DecklistFormatter.MTGO) == f"{main_modern_4c_str}\n{cmdr_part}"


def test_is_legal(deck_modern_4c):
    assert not deck_modern_4c.is_legal(Format.ALCHEMY)
    assert not deck_modern_4c.is_legal(Format.BRAWL)
    assert not deck_modern_4c.is_legal(Format.COMMANDER)
    assert not deck_modern_4c.is_legal(Format.DUEL)
    assert not deck_modern_4c.is_legal(Format.EXPLORER)
    assert not deck_modern_4c.is_legal(Format.FUTURE)
    assert not deck_modern_4c.is_legal(Format.GLADIATOR)
    assert not deck_modern_4c.is_legal(Format.HISTORIC)
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


def test_is_legal_attractions_stickers(
    card_forest, attraction_part, sticker_part, attraction_balloon_stand, sticker_ancestral_hotdog_minotaur
):
    main = CardList[OracleCard](Counter[OracleCard]({card_forest: 60}))
    deck = Deck[OracleCard](
        archetype="test_is_legal_attractions_stickers", main=main, attractions=attraction_part, stickers=sticker_part
    )
    assert deck.is_legal(Format.LEGACY)
    deck.add_card(attraction_balloon_stand, in_the=InThe.ATTRACTIONS)
    assert not deck.is_legal(Format.LEGACY)
    deck.add_card(sticker_ancestral_hotdog_minotaur, in_the=InThe.STICKERS)
    assert not deck.is_legal(Format.LEGACY)


def test_is_legal_16_sideboard(deck_modern_4c, card_aether_gust):
    deck_modern_4c.add_card(card_aether_gust, in_the=InThe.SIDE)
    assert not deck_modern_4c.is_legal(Format.MODERN)


# TODO(#229): Add a test for a commander or oathbreaker deck that exceeds the formats maximum size


def test_total_cards(deck_modern_4c):
    assert deck_modern_4c.total_cards() == 75


def test_total_cmc(deck_modern_4c):
    assert deck_modern_4c.total_cmc() == 141


def test_total_words(deck_modern_4c):
    assert deck_modern_4c.total_words() == 2118


# region Mutating Methods


def test_add_card_main_one(main_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_add_card_main_one", main=main_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=1, in_the=InThe.MAIN)
    main_modern_4c.add_card(card=card_boseiju_who_endures, quantity=1)
    assert deck.main == main_modern_4c


def test_add_card_main_many(main_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_add_card_main_many", main=main_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=2, in_the=InThe.MAIN)
    main_modern_4c.add_card(card=card_boseiju_who_endures, quantity=2)
    assert deck.main == main_modern_4c


def test_add_card_side_one(side_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_add_card_side_one", side=side_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=1, in_the=InThe.SIDE)
    side_modern_4c.add_card(card=card_boseiju_who_endures, quantity=1)
    assert deck.side == side_modern_4c


def test_add_card_side_many(side_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_add_card_side_many", side=side_modern_4c)
    deck.add_card(card=card_boseiju_who_endures, quantity=2, in_the=InThe.SIDE)
    side_modern_4c.add_card(card=card_boseiju_who_endures, quantity=2)
    assert deck.side == side_modern_4c


def test_add_card_cmdr_one(cmdr_part, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_add_card_cmdr_one", cmdr=cmdr_part)
    deck.add_card(card=card_omnath_locus_of_creation, quantity=1, in_the=InThe.CMDR)
    cmdr_part.add_card(card=card_omnath_locus_of_creation, quantity=1)
    assert deck.cmdr == cmdr_part


def test_add_card_cmdr_many(cmdr_part, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_add_card_cmdr_many", cmdr=cmdr_part)
    deck.add_card(card=card_omnath_locus_of_creation, quantity=2, in_the=InThe.CMDR)
    cmdr_part.add_card(card=card_omnath_locus_of_creation, quantity=2)
    assert deck.cmdr == cmdr_part


def test_add_cards_main(main_modern_4c, cards):
    deck = Deck[OracleCard](archetype="test_add_cards_main", main=main_modern_4c)
    deck.add_cards(cards=cards, in_the=InThe.MAIN)
    main_modern_4c.add_cards(cards=cards)
    assert deck.main == main_modern_4c


def test_add_cards_side(side_modern_4c, cards):
    deck = Deck[OracleCard](archetype="test_add_cards_side", side=side_modern_4c)
    deck.add_cards(cards=cards, in_the=InThe.SIDE)
    side_modern_4c.add_cards(cards=cards)
    assert deck.side == side_modern_4c


def test_add_cards_cmdr(cmdr_part, cards):
    deck = Deck[OracleCard](archetype="test_add_cards_cmdr", cmdr=cmdr_part)
    deck.add_cards(cards=cards, in_the=InThe.CMDR)
    cmdr_part.add_cards(cards=cards)
    assert deck.cmdr == cmdr_part


def test_remove_card_main_one(main_modern_4c, card_boseiju_who_endures):
    deck = Deck[OracleCard](archetype="test_remove_card_main_one", main=main_modern_4c)
    deck.remove_card(card=card_boseiju_who_endures, quantity=1, in_the=InThe.MAIN)
    main_modern_4c.remove_card(card=card_boseiju_who_endures, quantity=1)
    assert deck.main == main_modern_4c


def test_remove_card_main_many(main_modern_4c, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_remove_card_main_many", main=main_modern_4c)
    deck.remove_card(card=card_omnath_locus_of_creation, quantity=2, in_the=InThe.MAIN)
    main_modern_4c.remove_card(card=card_omnath_locus_of_creation, quantity=2)
    assert deck.main == main_modern_4c


def test_remove_card_main_all(main_modern_4c, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_remove_card_main_all", main=main_modern_4c)
    deck.remove_card(card=card_omnath_locus_of_creation, in_the=InThe.MAIN)
    main_modern_4c.remove_card(card=card_omnath_locus_of_creation)
    assert deck.main == main_modern_4c


def test_remove_card_side_one(side_modern_4c, card_chalice_of_the_void):
    deck = Deck[OracleCard](archetype="test_remove_card_side_one", side=side_modern_4c)
    deck.remove_card(card=card_chalice_of_the_void, quantity=1, in_the=InThe.SIDE)
    side_modern_4c.remove_card(card=card_chalice_of_the_void, quantity=1)
    assert deck.side == side_modern_4c


def test_remove_card_side_many(side_modern_4c, card_chalice_of_the_void):
    deck = Deck[OracleCard](archetype="test_remove_card_side_many", side=side_modern_4c)
    deck.remove_card(card=card_chalice_of_the_void, quantity=2, in_the=InThe.SIDE)
    side_modern_4c.remove_card(card=card_chalice_of_the_void, quantity=2)
    assert deck.side == side_modern_4c


def test_remove_card_side_all(side_modern_4c, card_chalice_of_the_void):
    deck = Deck[OracleCard](archetype="test_remove_card_side_all", side=side_modern_4c)
    deck.remove_card(card=card_chalice_of_the_void, in_the=InThe.SIDE)
    side_modern_4c.remove_card(card=card_chalice_of_the_void)
    assert deck.side == side_modern_4c


def test_remove_card_cmdr(cmdr_part, card_omnath_locus_of_creation):
    deck = Deck[OracleCard](archetype="test_remove_card_cmdr", cmdr=cmdr_part)
    deck.remove_card(card=card_omnath_locus_of_creation, quantity=1, in_the=InThe.CMDR)
    cmdr_part.remove_card(card=card_omnath_locus_of_creation, quantity=1)
    assert deck.cmdr == cmdr_part


def test_remove_cards_main(main_modern_4c, cards):
    deck = Deck[OracleCard](archetype="test_remove_cards_main", main=main_modern_4c)
    deck.remove_cards(cards=cards, in_the=InThe.MAIN)
    main_modern_4c.remove_cards(cards=cards)
    assert deck.main == main_modern_4c


def test_remove_cards_side(side_modern_4c, cards):
    deck = Deck[OracleCard](archetype="test_remove_cards_side", side=side_modern_4c)
    deck.remove_cards(cards=cards, in_the=InThe.SIDE)
    side_modern_4c.remove_cards(cards=cards)
    assert deck.side == side_modern_4c


def test_remove_cards_cmdr(cmdr_part, cmdr_cards):
    deck = Deck[OracleCard](archetype="test_remove_cards_cmdr", cmdr=cmdr_part)
    deck.remove_cards(cards=cmdr_cards, in_the=InThe.CMDR)
    cmdr_part.remove_cards(cards=cmdr_cards)
    assert deck.cmdr == cmdr_part


# endregion
