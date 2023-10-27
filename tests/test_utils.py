from collections import Counter
from sys import maxsize

import pytest
from scooze.catalogs import Format
from scooze.utils import (
    CostSymbol,
    DictDiff,
    cmdr_size,
    main_size,
    max_card_quantity,
    max_relentless_quantity,
    parse_cost,
    side_size,
)

# region Utils

# region Fixtures


@pytest.fixture
def dictA() -> dict[str, int]:
    return {
        "Blackcleave Cliffs": 4,
        "Unlucky Witness": 3,
    }


@pytest.fixture
def dictB() -> dict[str, int]:
    return {
        "Annihilating Glare": 1,
        "Blackcleave Cliffs": 2,
        "Unlucky Witness": 4,
        "Urborg, Tomb of Yawgmoth": 1,
    }


@pytest.fixture
def diffAB() -> dict[str, tuple[int, int]]:
    return {
        "Annihilating Glare": (0, 1),
        "Blackcleave Cliffs": (4, 2),
        "Unlucky Witness": (3, 4),
        "Urborg, Tomb of Yawgmoth": (0, 1),
    }


@pytest.fixture
def diffAB_str() -> str:
    return (
        "Annihilating Glare: (0, 1)\n"
        "Blackcleave Cliffs: (4, 2)\n"
        "Unlucky Witness: (3, 4)\n"
        "Urborg, Tomb of Yawgmoth: (0, 1)\n"
    )


# region Main Size


@pytest.fixture
def main_size_40() -> tuple[int, int]:
    return 40, maxsize


@pytest.fixture
def main_size_58() -> tuple[int, int]:
    return 58, 58


@pytest.fixture
def main_size_60() -> tuple[int, int]:
    return 60, maxsize


@pytest.fixture
def main_size_98() -> tuple[int, int]:
    return 98, 99


@pytest.fixture
def main_size_99() -> tuple[int, int]:
    return 99, 99


@pytest.fixture
def main_size_100() -> tuple[int, int]:
    return 100, 100


@pytest.fixture
def main_size_any() -> tuple[int, int]:
    return 0, maxsize


@pytest.fixture
def mana_cost_one_symbol() -> str:
    return "{W}"


@pytest.fixture
def mana_cost_multiple_symbols() -> str:
    return "{W}{B}"


@pytest.fixture
def mana_cost_with_generic() -> str:
    return "{2}{W}{B}"


# endregion

# region Side Size


@pytest.fixture
def side_size_0() -> tuple[int, int]:
    return 0, 0


@pytest.fixture
def side_size_15() -> tuple[int, int]:
    return 0, 15


@pytest.fixture
def side_size_any() -> tuple[int, int]:
    return 0, maxsize


# endregion

# region Cmdr Size


@pytest.fixture
def cmdr_size_0() -> tuple[int, int]:
    return 0, 0


@pytest.fixture
def cmdr_size_1() -> tuple[int, int]:
    return 1, 1


@pytest.fixture
def cmdr_size_1_or_2() -> tuple[int, int]:
    return 1, 2


@pytest.fixture
def cmdr_size_2() -> tuple[int, int]:
    return 2, 2


@pytest.fixture
def cmdr_size_any() -> tuple[int, int]:
    return 0, maxsize


# endregion

# endregion

# region Tests


@pytest.mark.dict_diff
def test_get_diff(dictA, dictB, diffAB):
    assert DictDiff.get_diff(dictA, dictB, NO_KEY=0).contents == diffAB


@pytest.mark.dict_diff
def test_dictdiff_eq(dictA, dictB, diffAB):
    dict_diff = DictDiff.get_diff(dictA, dictB, NO_KEY=0)
    assert dict_diff == DictDiff(diffAB)


@pytest.mark.dict_diff
def test_dictdiff_str(diffAB, diffAB_str):
    dict_diff = DictDiff(diffAB)
    assert str(dict_diff) == diffAB_str


# region Test Format Max Card Quantity


# region Relentless Cards


@pytest.mark.card_quantity
def test_basicland_max_relentless_quantity():
    assert max_relentless_quantity
    assert max_relentless_quantity("Plains") == maxsize
    assert max_relentless_quantity("Island") == maxsize
    assert max_relentless_quantity("Swamp") == maxsize
    assert max_relentless_quantity("Mountain") == maxsize
    assert max_relentless_quantity("Forest") == maxsize
    assert max_relentless_quantity("Wastes") == maxsize
    assert max_relentless_quantity("Snow-Covered Plains") == maxsize
    assert max_relentless_quantity("Snow-Covered Island") == maxsize
    assert max_relentless_quantity("Snow-Covered Swamp") == maxsize
    assert max_relentless_quantity("Snow-Covered Mountain") == maxsize
    assert max_relentless_quantity("Snow-Covered Forest") == maxsize


@pytest.mark.card_quantity
def test_sevendwarves_max_relentless_quantity():
    assert max_relentless_quantity("Seven Dwarves") == 7


@pytest.mark.card_quantity
def test_nazgul_max_relentless_quantity():
    assert max_relentless_quantity("Nazgûl") == 9
    assert max_relentless_quantity("Nazgul") == 9


@pytest.mark.card_quantity
def test_relentless_max_relentless_quantity():
    assert max_relentless_quantity("Relentless Rats") == maxsize
    assert max_relentless_quantity("Dragon's Approach") == maxsize
    assert max_relentless_quantity("Persistent Petitioners") == maxsize
    assert max_relentless_quantity("Rat Colony") == maxsize
    assert max_relentless_quantity("Relentless Rats") == maxsize
    assert max_relentless_quantity("Shadowborn Apostle") == maxsize


@pytest.mark.card_quantity
def test_normal_max_relentless_quantity():
    assert max_relentless_quantity("Python") == 0
    assert max_relentless_quantity("Scavenging Ooze") == 0


# endregion

# region Normal Cards

# match fmt.value:
#     case Format.LIMITED:
#         return maxsize

#     case (
#         Format.BRAWL
#         | Format.COMMANDER
#         | Format.DUEL
#         | Format.GLADIATOR
#         | Format.HISTORICBRAWL
#         | Format.OATHBREAKER
#         | Format.PAUPERCOMMANDER
#         | Format.PREDH
#     ):
#         return 1

#     case (
#         Format.ALCHEMY
#         | Format.EXPLORER
#         | Format.FUTURE
#         | Format.HISTORIC
#         | Format.LEGACY
#         | Format.MODERN
#         | Format.OLDSCHOOL
#         | Format.PAUPER
#         | Format.PENNY
#         | Format.PIONEER
#         | Format.PREMODERN
#         | Format.STANDARD
#         | Format.VINTAGE
#     ):
#         return 4

#     case Format.NONE | _:
#         return maxsize


@pytest.mark.card_quantity
def test_fmt_alchemy_max_card_quantity():
    assert max_card_quantity(Format.ALCHEMY) == 4


@pytest.mark.card_quantity
def test_fmt_brawl_max_card_quantity():
    assert max_card_quantity(Format.BRAWL) == 1


@pytest.mark.card_quantity
def test_fmt_commander_max_card_quantity():
    assert max_card_quantity(Format.COMMANDER) == 1


@pytest.mark.card_quantity
def test_fmt_duel_max_card_quantity():
    assert max_card_quantity(Format.DUEL) == 1


@pytest.mark.card_quantity
def test_fmt_explorer_max_card_quantity():
    assert max_card_quantity(Format.EXPLORER) == 4


@pytest.mark.card_quantity
def test_fmt_future_max_card_quantity():
    assert max_card_quantity(Format.FUTURE) == 4


@pytest.mark.card_quantity
def test_fmt_gladiator_max_card_quantity():
    assert max_card_quantity(Format.GLADIATOR) == 1


@pytest.mark.card_quantity
def test_fmt_historic_max_card_quantity():
    assert max_card_quantity(Format.HISTORIC) == 4


@pytest.mark.card_quantity
def test_fmt_historicbrawl_max_card_quantity():
    assert max_card_quantity(Format.HISTORICBRAWL) == 1


@pytest.mark.card_quantity
def test_fmt_legacy_max_card_quantity():
    assert max_card_quantity(Format.LEGACY) == 4


@pytest.mark.card_quantity
def test_fmt_modern_max_card_quantity():
    assert max_card_quantity(Format.MODERN) == 4


@pytest.mark.card_quantity
def test_fmt_oathbreaker_max_card_quantity():
    assert max_card_quantity(Format.OATHBREAKER) == 1


@pytest.mark.card_quantity
def test_fmt_oldschool_max_card_quantity():
    assert max_card_quantity(Format.OLDSCHOOL) == 4


@pytest.mark.card_quantity
def test_fmt_pauper_max_card_quantity():
    assert max_card_quantity(Format.PAUPER) == 4


@pytest.mark.card_quantity
def test_fmt_paupercommander_max_card_quantity():
    assert max_card_quantity(Format.PAUPERCOMMANDER) == 1


@pytest.mark.card_quantity
def test_fmt_penny_max_card_quantity():
    assert max_card_quantity(Format.PENNY) == 4


@pytest.mark.card_quantity
def test_fmt_pioneer_max_card_quantity():
    assert max_card_quantity(Format.PIONEER) == 4


@pytest.mark.card_quantity
def test_fmt_predh_max_card_quantity():
    assert max_card_quantity(Format.PREDH) == 1


@pytest.mark.card_quantity
def test_fmt_premodern_max_card_quantity():
    assert max_card_quantity(Format.PREMODERN) == 4


@pytest.mark.card_quantity
def test_fmt_standard_max_card_quantity():
    assert max_card_quantity(Format.STANDARD) == 4


@pytest.mark.card_quantity
def test_fmt_vintage_max_card_quantity():
    assert max_card_quantity(Format.VINTAGE) == 4


@pytest.mark.card_quantity
def test_fmt_limited_max_card_quantity():
    assert max_card_quantity(Format.LIMITED) == maxsize


@pytest.mark.card_quantity
def test_fmt_none_max_card_quantity():
    assert max_card_quantity(Format.NONE) == maxsize


# endregion

# endregion

# region Test Format Deck Size

# region Main Size


@pytest.mark.deck_size
def test_fmt_alchemy_main_size(main_size_60):
    assert main_size(Format.ALCHEMY) == main_size_60


@pytest.mark.deck_size
def test_fmt_brawl_main_size(main_size_99):
    assert main_size(Format.BRAWL) == main_size_99


@pytest.mark.deck_size
def test_fmt_commander_main_size(main_size_98):
    assert main_size(Format.COMMANDER) == main_size_98


@pytest.mark.deck_size
def test_fmt_duel_main_size(main_size_98):
    assert main_size(Format.DUEL) == main_size_98


@pytest.mark.deck_size
def test_fmt_explorer_main_size(main_size_60):
    assert main_size(Format.EXPLORER) == main_size_60


@pytest.mark.deck_size
def test_fmt_future_main_size(main_size_60):
    assert main_size(Format.FUTURE) == main_size_60


@pytest.mark.deck_size
def test_fmt_gladiator_main_size(main_size_100):
    assert main_size(Format.GLADIATOR) == main_size_100


@pytest.mark.deck_size
def test_fmt_historic_main_size(main_size_60):
    assert main_size(Format.HISTORIC) == main_size_60


@pytest.mark.deck_size
def test_fmt_historicbrawl_main_size(main_size_99):
    assert main_size(Format.HISTORICBRAWL) == main_size_99


@pytest.mark.deck_size
def test_fmt_legacy_main_size(main_size_60):
    assert main_size(Format.LEGACY) == main_size_60


@pytest.mark.deck_size
def test_fmt_modern_main_size(main_size_60):
    assert main_size(Format.MODERN) == main_size_60


@pytest.mark.deck_size
def test_fmt_oathbreaker_main_size(main_size_58):
    assert main_size(Format.OATHBREAKER) == main_size_58


@pytest.mark.deck_size
def test_fmt_oldschool_main_size(main_size_60):
    assert main_size(Format.OLDSCHOOL) == main_size_60


@pytest.mark.deck_size
def test_fmt_pauper_main_size(main_size_60):
    assert main_size(Format.PAUPER) == main_size_60


@pytest.mark.deck_size
def test_fmt_paupercommander_main_size(main_size_99):
    assert main_size(Format.PAUPERCOMMANDER) == main_size_99


@pytest.mark.deck_size
def test_fmt_penny_main_size(main_size_60):
    assert main_size(Format.PENNY) == main_size_60


@pytest.mark.deck_size
def test_fmt_pioneer_main_size(main_size_60):
    assert main_size(Format.PIONEER) == main_size_60


@pytest.mark.deck_size
def test_fmt_predh_main_size(main_size_99):
    assert main_size(Format.PREDH) == main_size_99


@pytest.mark.deck_size
def test_fmt_premodern_main_size(main_size_60):
    assert main_size(Format.PREMODERN) == main_size_60


@pytest.mark.deck_size
def test_fmt_standard_main_size(main_size_60):
    assert main_size(Format.STANDARD) == main_size_60


@pytest.mark.deck_size
def test_fmt_vintage_main_size(main_size_60):
    assert main_size(Format.VINTAGE) == main_size_60


@pytest.mark.deck_size
def test_fmt_limited_main_size(main_size_40):
    assert main_size(Format.LIMITED) == main_size_40


@pytest.mark.deck_size
def test_fmt_none_main_size(main_size_any):
    assert main_size(Format.NONE) == main_size_any


# endregion

# region Side Size


@pytest.mark.deck_size
def test_fmt_alchemy_side_size(side_size_15):
    assert side_size(Format.ALCHEMY) == side_size_15


@pytest.mark.deck_size
def test_fmt_brawl_side_size(side_size_0):
    assert side_size(Format.BRAWL) == side_size_0


@pytest.mark.deck_size
def test_fmt_commander_side_size(side_size_0):
    assert side_size(Format.COMMANDER) == side_size_0


@pytest.mark.deck_size
def test_fmt_duel_side_size(side_size_0):
    assert side_size(Format.DUEL) == side_size_0


@pytest.mark.deck_size
def test_fmt_explorer_side_size(side_size_15):
    assert side_size(Format.EXPLORER) == side_size_15


@pytest.mark.deck_size
def test_fmt_future_side_size(side_size_15):
    assert side_size(Format.FUTURE) == side_size_15


@pytest.mark.deck_size
def test_fmt_gladiator_side_size(side_size_0):
    assert side_size(Format.GLADIATOR) == side_size_0


@pytest.mark.deck_size
def test_fmt_historic_side_size(side_size_15):
    assert side_size(Format.HISTORIC) == side_size_15


@pytest.mark.deck_size
def test_fmt_historicbrawl_side_size(side_size_0):
    assert side_size(Format.HISTORICBRAWL) == side_size_0


@pytest.mark.deck_size
def test_fmt_legacy_side_size(side_size_15):
    assert side_size(Format.LEGACY) == side_size_15


@pytest.mark.deck_size
def test_fmt_modern_side_size(side_size_15):
    assert side_size(Format.MODERN) == side_size_15


@pytest.mark.deck_size
def test_fmt_oathbreaker_side_size(side_size_0):
    assert side_size(Format.OATHBREAKER) == side_size_0


@pytest.mark.deck_size
def test_fmt_oldschool_side_size(side_size_15):
    assert side_size(Format.OLDSCHOOL) == side_size_15


@pytest.mark.deck_size
def test_fmt_pauper_side_size(side_size_15):
    assert side_size(Format.PAUPER) == side_size_15


@pytest.mark.deck_size
def test_fmt_paupercommander_side_size(side_size_0):
    assert side_size(Format.PAUPERCOMMANDER) == side_size_0


@pytest.mark.deck_size
def test_fmt_penny_side_size(side_size_15):
    assert side_size(Format.PENNY) == side_size_15


@pytest.mark.deck_size
def test_fmt_pioneer_side_size(side_size_15):
    assert side_size(Format.PIONEER) == side_size_15


@pytest.mark.deck_size
def test_fmt_predh_side_size(side_size_0):
    assert side_size(Format.PREDH) == side_size_0


@pytest.mark.deck_size
def test_fmt_premodern_side_size(side_size_15):
    assert side_size(Format.PREMODERN) == side_size_15


@pytest.mark.deck_size
def test_fmt_standard_side_size(side_size_15):
    assert side_size(Format.STANDARD) == side_size_15


@pytest.mark.deck_size
def test_fmt_vintage_side_size(side_size_15):
    assert side_size(Format.VINTAGE) == side_size_15


@pytest.mark.deck_size
def test_fmt_limited_side_size(side_size_any):
    assert side_size(Format.LIMITED) == side_size_any


@pytest.mark.deck_size
def test_fmt_none_side_size(side_size_any):
    assert side_size(Format.NONE) == side_size_any


# endregion

# region Cmdr Size


@pytest.mark.deck_size
def test_fmt_alchemy_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.ALCHEMY) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_brawl_cmdr_size(cmdr_size_1):
    assert cmdr_size(Format.BRAWL) == cmdr_size_1


@pytest.mark.deck_size
def test_fmt_commander_cmdr_size(cmdr_size_1_or_2):
    assert cmdr_size(Format.COMMANDER) == cmdr_size_1_or_2


@pytest.mark.deck_size
def test_fmt_duel_cmdr_size(cmdr_size_1_or_2):
    assert cmdr_size(Format.DUEL) == cmdr_size_1_or_2


@pytest.mark.deck_size
def test_fmt_explorer_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.EXPLORER) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_future_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.FUTURE) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_gladiator_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.GLADIATOR) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_historic_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.HISTORIC) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_historicbrawl_cmdr_size(cmdr_size_1):
    assert cmdr_size(Format.HISTORICBRAWL) == cmdr_size_1


@pytest.mark.deck_size
def test_fmt_legacy_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.LEGACY) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_modern_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.MODERN) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_oathbreaker_cmdr_size(cmdr_size_2):
    assert cmdr_size(Format.OATHBREAKER) == cmdr_size_2


@pytest.mark.deck_size
def test_fmt_oldschool_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.OLDSCHOOL) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_pauper_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.PAUPER) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_paupercommander_cmdr_size(cmdr_size_1):
    assert cmdr_size(Format.PAUPERCOMMANDER) == cmdr_size_1


@pytest.mark.deck_size
def test_fmt_penny_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.PENNY) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_pioneer_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.PIONEER) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_predh_cmdr_size(cmdr_size_1):
    assert cmdr_size(Format.PREDH) == cmdr_size_1


@pytest.mark.deck_size
def test_fmt_premodern_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.PREMODERN) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_standard_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.STANDARD) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_vintage_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.VINTAGE) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_limited_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.LIMITED) == cmdr_size_0


@pytest.mark.deck_size
def test_fmt_none_cmdr_size(cmdr_size_any):
    assert cmdr_size(Format.NONE) == cmdr_size_any


# endregion

# endregion

# region Mana symbology


def test_parse_mana_cost_one_symbol(mana_cost_one_symbol):
    assert parse_cost(mana_cost_one_symbol) == Counter({CostSymbol.WHITE: 1})


def test_parse_mana_cost_multiple_symbols(mana_cost_multiple_symbols):
    assert parse_cost(mana_cost_multiple_symbols) == Counter({CostSymbol.WHITE: 1, CostSymbol.BLACK: 1})


def test_parse_mana_cost_with_generic(mana_cost_with_generic):
    assert parse_cost(mana_cost_with_generic) == Counter(
        {CostSymbol.WHITE: 1, CostSymbol.BLACK: 1, CostSymbol.GENERIC_1: 2}
    )


# endregion

# endregion

# endregion
