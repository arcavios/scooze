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
    parse_symbols,
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


# region Mana costs
@pytest.fixture
def mana_cost_one_symbol() -> str:
    return "{W}"


@pytest.fixture
def mana_cost_multiple_symbols() -> str:
    return "{W}{B}"


@pytest.fixture
def mana_cost_with_generic() -> str:
    return "{2}{W}{B}"


@pytest.fixture
def mana_cost_with_multiple_generic() -> str:
    return "{1}{1}{U}{R}"


@pytest.fixture
def mana_cost_with_hybrid() -> str:
    return "{B/G}{B/G}"


# endregion

# endregion

# region Tests


def test_get_diff(dictA, dictB, diffAB):
    assert DictDiff.get_diff(dictA, dictB, NO_KEY=0).contents == diffAB


def test_dictdiff_eq(dictA, dictB, diffAB):
    dict_diff = DictDiff.get_diff(dictA, dictB, NO_KEY=0)
    assert dict_diff == DictDiff(diffAB)


def test_dictdiff_str(diffAB, diffAB_str):
    dict_diff = DictDiff(diffAB)
    assert str(dict_diff) == diffAB_str


# region Test Format Max Card Quantity


# region Relentless Cards


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


def test_sevendwarves_max_relentless_quantity():
    assert max_relentless_quantity("Seven Dwarves") == 7


def test_nazgul_max_relentless_quantity():
    assert max_relentless_quantity("Nazgûl") == 9
    assert max_relentless_quantity("Nazgul") == 9


def test_relentless_max_relentless_quantity():
    assert max_relentless_quantity("Relentless Rats") == maxsize
    assert max_relentless_quantity("Dragon's Approach") == maxsize
    assert max_relentless_quantity("Persistent Petitioners") == maxsize
    assert max_relentless_quantity("Rat Colony") == maxsize
    assert max_relentless_quantity("Relentless Rats") == maxsize
    assert max_relentless_quantity("Shadowborn Apostle") == maxsize


def test_normal_max_relentless_quantity():
    assert max_relentless_quantity("Python") == 0
    assert max_relentless_quantity("Scavenging Ooze") == 0


# endregion

# region Normal Cards


def test_fmt_alchemy_max_card_quantity():
    assert max_card_quantity(Format.ALCHEMY) == 4


def test_fmt_brawl_max_card_quantity():
    assert max_card_quantity(Format.BRAWL) == 1


def test_fmt_commander_max_card_quantity():
    assert max_card_quantity(Format.COMMANDER) == 1


def test_fmt_duel_max_card_quantity():
    assert max_card_quantity(Format.DUEL) == 1


def test_fmt_explorer_max_card_quantity():
    assert max_card_quantity(Format.EXPLORER) == 4


def test_fmt_future_max_card_quantity():
    assert max_card_quantity(Format.FUTURE) == 4


def test_fmt_gladiator_max_card_quantity():
    assert max_card_quantity(Format.GLADIATOR) == 1


def test_fmt_historic_max_card_quantity():
    assert max_card_quantity(Format.HISTORIC) == 4


def test_fmt_legacy_max_card_quantity():
    assert max_card_quantity(Format.LEGACY) == 4


def test_fmt_modern_max_card_quantity():
    assert max_card_quantity(Format.MODERN) == 4


def test_fmt_oathbreaker_max_card_quantity():
    assert max_card_quantity(Format.OATHBREAKER) == 1


def test_fmt_oldschool_max_card_quantity():
    assert max_card_quantity(Format.OLDSCHOOL) == 4


def test_fmt_pauper_max_card_quantity():
    assert max_card_quantity(Format.PAUPER) == 4


def test_fmt_paupercommander_max_card_quantity():
    assert max_card_quantity(Format.PAUPERCOMMANDER) == 1


def test_fmt_penny_max_card_quantity():
    assert max_card_quantity(Format.PENNY) == 4


def test_fmt_pioneer_max_card_quantity():
    assert max_card_quantity(Format.PIONEER) == 4


def test_fmt_predh_max_card_quantity():
    assert max_card_quantity(Format.PREDH) == 1


def test_fmt_premodern_max_card_quantity():
    assert max_card_quantity(Format.PREMODERN) == 4


def test_fmt_standard_max_card_quantity():
    assert max_card_quantity(Format.STANDARD) == 4


def test_fmt_standardbrawl_max_card_quantity():
    assert max_card_quantity(Format.STANDARDBRAWL) == 1


def test_fmt_timeless_max_card_quantity():
    assert max_card_quantity(Format.TIMELESS) == 4


def test_fmt_vintage_max_card_quantity():
    assert max_card_quantity(Format.VINTAGE) == 4


def test_fmt_limited_max_card_quantity():
    assert max_card_quantity(Format.LIMITED) == maxsize


def test_fmt_none_max_card_quantity():
    assert max_card_quantity(Format.NONE) == maxsize


# endregion

# endregion

# region Test Format Deck Size


# region Main.
def test_fmt_alchemy_main_size(main_size_60):
    assert main_size(Format.ALCHEMY) == main_size_60


def test_fmt_brawl_main_size(main_size_99):
    assert main_size(Format.BRAWL) == main_size_99


def test_fmt_commander_main_size(main_size_98):
    assert main_size(Format.COMMANDER) == main_size_98


def test_fmt_duel_main_size(main_size_98):
    assert main_size(Format.DUEL) == main_size_98


def test_fmt_explorer_main_size(main_size_60):
    assert main_size(Format.EXPLORER) == main_size_60


def test_fmt_future_main_size(main_size_60):
    assert main_size(Format.FUTURE) == main_size_60


def test_fmt_gladiator_main_size(main_size_100):
    assert main_size(Format.GLADIATOR) == main_size_100


def test_fmt_historic_main_size(main_size_60):
    assert main_size(Format.HISTORIC) == main_size_60


def test_fmt_legacy_main_size(main_size_60):
    assert main_size(Format.LEGACY) == main_size_60


def test_fmt_modern_main_size(main_size_60):
    assert main_size(Format.MODERN) == main_size_60


def test_fmt_oathbreaker_main_size(main_size_58):
    assert main_size(Format.OATHBREAKER) == main_size_58


def test_fmt_oldschool_main_size(main_size_60):
    assert main_size(Format.OLDSCHOOL) == main_size_60


def test_fmt_pauper_main_size(main_size_60):
    assert main_size(Format.PAUPER) == main_size_60


def test_fmt_paupercommander_main_size(main_size_99):
    assert main_size(Format.PAUPERCOMMANDER) == main_size_99


def test_fmt_penny_main_size(main_size_60):
    assert main_size(Format.PENNY) == main_size_60


def test_fmt_pioneer_main_size(main_size_60):
    assert main_size(Format.PIONEER) == main_size_60


def test_fmt_predh_main_size(main_size_99):
    assert main_size(Format.PREDH) == main_size_99


def test_fmt_premodern_main_size(main_size_60):
    assert main_size(Format.PREMODERN) == main_size_60


def test_fmt_standard_main_size(main_size_60):
    assert main_size(Format.STANDARD) == main_size_60


def test_fmt_standardbrawl_main_size(main_size_99):
    assert main_size(Format.STANDARDBRAWL) == main_size_99


def test_fmt_timeless_main_size(main_size_60):
    assert main_size(Format.TIMELESS) == main_size_60


def test_fmt_vintage_main_size(main_size_60):
    assert main_size(Format.VINTAGE) == main_size_60


def test_fmt_limited_main_size(main_size_40):
    assert main_size(Format.LIMITED) == main_size_40


def test_fmt_none_main_size(main_size_any):
    assert main_size(Format.NONE) == main_size_any


# endregion

# region Side Size


def test_fmt_alchemy_side_size(side_size_15):
    assert side_size(Format.ALCHEMY) == side_size_15


def test_fmt_brawl_side_size(side_size_0):
    assert side_size(Format.BRAWL) == side_size_0


def test_fmt_commander_side_size(side_size_0):
    assert side_size(Format.COMMANDER) == side_size_0


def test_fmt_duel_side_size(side_size_0):
    assert side_size(Format.DUEL) == side_size_0


def test_fmt_explorer_side_size(side_size_15):
    assert side_size(Format.EXPLORER) == side_size_15


def test_fmt_future_side_size(side_size_15):
    assert side_size(Format.FUTURE) == side_size_15


def test_fmt_gladiator_side_size(side_size_0):
    assert side_size(Format.GLADIATOR) == side_size_0


def test_fmt_historic_side_size(side_size_15):
    assert side_size(Format.HISTORIC) == side_size_15


def test_fmt_legacy_side_size(side_size_15):
    assert side_size(Format.LEGACY) == side_size_15


def test_fmt_modern_side_size(side_size_15):
    assert side_size(Format.MODERN) == side_size_15


def test_fmt_oathbreaker_side_size(side_size_0):
    assert side_size(Format.OATHBREAKER) == side_size_0


def test_fmt_oldschool_side_size(side_size_15):
    assert side_size(Format.OLDSCHOOL) == side_size_15


def test_fmt_pauper_side_size(side_size_15):
    assert side_size(Format.PAUPER) == side_size_15


def test_fmt_paupercommander_side_size(side_size_0):
    assert side_size(Format.PAUPERCOMMANDER) == side_size_0


def test_fmt_penny_side_size(side_size_15):
    assert side_size(Format.PENNY) == side_size_15


def test_fmt_pioneer_side_size(side_size_15):
    assert side_size(Format.PIONEER) == side_size_15


def test_fmt_predh_side_size(side_size_0):
    assert side_size(Format.PREDH) == side_size_0


def test_fmt_premodern_side_size(side_size_15):
    assert side_size(Format.PREMODERN) == side_size_15


def test_fmt_standard_side_size(side_size_15):
    assert side_size(Format.STANDARD) == side_size_15


def test_fmt_standardbrawl_side_size(side_size_0):
    assert side_size(Format.STANDARDBRAWL) == side_size_0


def test_fmt_timeless_side_size(side_size_15):
    assert side_size(Format.TIMELESS) == side_size_15


def test_fmt_vintage_side_size(side_size_15):
    assert side_size(Format.VINTAGE) == side_size_15


def test_fmt_limited_side_size(side_size_any):
    assert side_size(Format.LIMITED) == side_size_any


def test_fmt_none_side_size(side_size_any):
    assert side_size(Format.NONE) == side_size_any


# endregion

# region Cmdr Size


def test_fmt_alchemy_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.ALCHEMY) == cmdr_size_0


def test_fmt_brawl_cmdr_size(cmdr_size_1):
    assert cmdr_size(Format.BRAWL) == cmdr_size_1


def test_fmt_commander_cmdr_size(cmdr_size_1_or_2):
    assert cmdr_size(Format.COMMANDER) == cmdr_size_1_or_2


def test_fmt_duel_cmdr_size(cmdr_size_1_or_2):
    assert cmdr_size(Format.DUEL) == cmdr_size_1_or_2


def test_fmt_explorer_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.EXPLORER) == cmdr_size_0


def test_fmt_future_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.FUTURE) == cmdr_size_0


def test_fmt_gladiator_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.GLADIATOR) == cmdr_size_0


def test_fmt_historic_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.HISTORIC) == cmdr_size_0


def test_fmt_legacy_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.LEGACY) == cmdr_size_0


def test_fmt_modern_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.MODERN) == cmdr_size_0


def test_fmt_oathbreaker_cmdr_size(cmdr_size_2):
    assert cmdr_size(Format.OATHBREAKER) == cmdr_size_2


def test_fmt_oldschool_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.OLDSCHOOL) == cmdr_size_0


def test_fmt_pauper_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.PAUPER) == cmdr_size_0


def test_fmt_paupercommander_cmdr_size(cmdr_size_1):
    assert cmdr_size(Format.PAUPERCOMMANDER) == cmdr_size_1


def test_fmt_penny_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.PENNY) == cmdr_size_0


def test_fmt_pioneer_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.PIONEER) == cmdr_size_0


def test_fmt_predh_cmdr_size(cmdr_size_1):
    assert cmdr_size(Format.PREDH) == cmdr_size_1


def test_fmt_premodern_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.PREMODERN) == cmdr_size_0


def test_fmt_standard_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.STANDARD) == cmdr_size_0


def test_fmt_standardbrawl_cmdr_size(cmdr_size_1):
    assert cmdr_size(Format.STANDARDBRAWL) == cmdr_size_1


def test_fmt_timeless_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.TIMELESS) == cmdr_size_0


def test_fmt_vintage_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.VINTAGE) == cmdr_size_0


def test_fmt_limited_cmdr_size(cmdr_size_0):
    assert cmdr_size(Format.LIMITED) == cmdr_size_0


def test_fmt_none_cmdr_size(cmdr_size_any):
    assert cmdr_size(Format.NONE) == cmdr_size_any


# endregion

# endregion

# region Mana symbology


def test_parse_symbols_one_symbol(mana_cost_one_symbol):
    assert parse_symbols(mana_cost_one_symbol) == {CostSymbol.WHITE: 1}


def test_parse_symbols_multiple_symbols(mana_cost_multiple_symbols):
    assert parse_symbols(mana_cost_multiple_symbols) == {CostSymbol.WHITE: 1, CostSymbol.BLACK: 1}


def test_parse_symbols_with_generic(mana_cost_with_generic):
    assert parse_symbols(mana_cost_with_generic) == {CostSymbol.WHITE: 1, CostSymbol.BLACK: 1, CostSymbol.GENERIC_2: 1}


def test_parse_symbols_with_multiple_generic(mana_cost_with_multiple_generic):
    assert parse_symbols(mana_cost_with_multiple_generic) == {
        CostSymbol.BLUE: 1,
        CostSymbol.RED: 1,
        CostSymbol.GENERIC_1: 2,
    }


def test_parse_symbols_with_hybrid(mana_cost_with_hybrid):
    assert parse_symbols(mana_cost_with_hybrid) == {
        CostSymbol.HYBRID_BG: 2,
    }


# endregion

# endregion

# endregion
