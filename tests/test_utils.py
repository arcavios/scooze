from sys import maxsize

import pytest
import scooze.models.utils as model_utils
from scooze.enums import Format
from scooze.utils import DictDiff

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


# endregion

# region Tests


@pytest.mark.dictdiff
def test_get_diff(dictA, dictB, diffAB):
    assert DictDiff.get_diff(dictA, dictB, NO_KEY=0).contents == diffAB


@pytest.mark.dictdiff
def test_dictdiff_eq(dictA, dictB, diffAB):
    dict_diff = DictDiff.get_diff(dictA, dictB, NO_KEY=0)
    assert dict_diff == DictDiff(diffAB)


@pytest.mark.dictdiff
def test_dictdiff_str(diffAB, diffAB_str):
    dict_diff = DictDiff(diffAB)
    assert str(dict_diff) == diffAB_str


# endregion

# endregion Utils

# region Model Utils

# region Fixtures

# region Format Deck Size

# region Main Size


@pytest.fixture
def main_size_40() -> tuple[int, int]:
    return (40, maxsize)


@pytest.fixture
def main_size_58() -> tuple[int, int]:
    return (58, 58)


@pytest.fixture
def main_size_60() -> tuple[int, int]:
    return (60, maxsize)


@pytest.fixture
def main_size_98() -> tuple[int, int]:
    return (98, 99)


@pytest.fixture
def main_size_99() -> tuple[int, int]:
    return (99, 99)


@pytest.fixture
def main_size_100() -> tuple[int, int]:
    return (100, 100)


@pytest.fixture
def main_size_any() -> tuple[int, int]:
    return (0, maxsize)


# endregion

# region Side Size


@pytest.fixture
def side_size_0() -> tuple[int, int]:
    return (0, 0)


@pytest.fixture
def side_size_15() -> tuple[int, int]:
    return (0, 15)


@pytest.fixture
def side_size_any() -> tuple[int, int]:
    return (0, maxsize)


# endregion

# region Cmdr Size


@pytest.fixture
def cmdr_size_0() -> tuple[int, int]:
    return (0, 0)


@pytest.fixture
def cmdr_size_1() -> tuple[int, int]:
    return (1, 1)


@pytest.fixture
def cmdr_size_1_or_2() -> tuple[int, int]:
    return (1, 2)


@pytest.fixture
def cmdr_size_2() -> tuple[int, int]:
    return (2, 2)


@pytest.fixture
def cmdr_size_any() -> tuple[int, int]:
    return (0, maxsize)


# endregion

# endregion

# endregion

# region Test Format Deck Size

# region Main Size


@pytest.mark.model_utils
def test_fmt_alchemy_main_size(main_size_60):
    assert model_utils.main_size(Format.ALCHEMY) == main_size_60


@pytest.mark.model_utils
def test_fmt_brawl_main_size(main_size_99):
    assert model_utils.main_size(Format.BRAWL) == main_size_99


@pytest.mark.model_utils
def test_fmt_commander_main_size(main_size_98):
    assert model_utils.main_size(Format.COMMANDER) == main_size_98


@pytest.mark.model_utils
def test_fmt_duel_main_size(main_size_98):
    assert model_utils.main_size(Format.DUEL) == main_size_98


@pytest.mark.model_utils
def test_fmt_explorer_main_size(main_size_60):
    assert model_utils.main_size(Format.EXPLORER) == main_size_60


@pytest.mark.model_utils
def test_fmt_future_main_size(main_size_60):
    assert model_utils.main_size(Format.FUTURE) == main_size_60


@pytest.mark.model_utils
def test_fmt_gladiator_main_size(main_size_100):
    assert model_utils.main_size(Format.GLADIATOR) == main_size_100


@pytest.mark.model_utils
def test_fmt_historic_main_size(main_size_60):
    assert model_utils.main_size(Format.HISTORIC) == main_size_60


@pytest.mark.model_utils
def test_fmt_historicbrawl_main_size(main_size_99):
    assert model_utils.main_size(Format.HISTORICBRAWL) == main_size_99


@pytest.mark.model_utils
def test_fmt_legacy_main_size(main_size_60):
    assert model_utils.main_size(Format.LEGACY) == main_size_60


@pytest.mark.model_utils
def test_fmt_modern_main_size(main_size_60):
    assert model_utils.main_size(Format.MODERN) == main_size_60


@pytest.mark.model_utils
def test_fmt_oathbreaker_main_size(main_size_58):
    assert model_utils.main_size(Format.OATHBREAKER) == main_size_58


@pytest.mark.model_utils
def test_fmt_oldschool_main_size(main_size_60):
    assert model_utils.main_size(Format.OLDSCHOOL) == main_size_60


@pytest.mark.model_utils
def test_fmt_pauper_main_size(main_size_60):
    assert model_utils.main_size(Format.PAUPER) == main_size_60


@pytest.mark.model_utils
def test_fmt_paupercommander_main_size(main_size_99):
    assert model_utils.main_size(Format.PAUPERCOMMANDER) == main_size_99


@pytest.mark.model_utils
def test_fmt_penny_main_size(main_size_60):
    assert model_utils.main_size(Format.PENNY) == main_size_60


@pytest.mark.model_utils
def test_fmt_pioneer_main_size(main_size_60):
    assert model_utils.main_size(Format.PIONEER) == main_size_60


@pytest.mark.model_utils
def test_fmt_predh_main_size(main_size_99):
    assert model_utils.main_size(Format.PREDH) == main_size_99


@pytest.mark.model_utils
def test_fmt_premodern_main_size(main_size_60):
    assert model_utils.main_size(Format.PREMODERN) == main_size_60


@pytest.mark.model_utils
def test_fmt_standard_main_size(main_size_60):
    assert model_utils.main_size(Format.STANDARD) == main_size_60


@pytest.mark.model_utils
def test_fmt_vintage_main_size(main_size_60):
    assert model_utils.main_size(Format.VINTAGE) == main_size_60


@pytest.mark.model_utils
def test_fmt_limited_main_size(main_size_40):
    assert model_utils.main_size(Format.LIMITED) == main_size_40


@pytest.mark.model_utils
def test_fmt_none_main_size(main_size_any):
    assert model_utils.main_size(Format.NONE) == main_size_any


# endregion

# region Side Size


@pytest.mark.model_utils
def test_fmt_alchemy_side_size(side_size_15):
    assert model_utils.side_size(Format.ALCHEMY) == side_size_15


@pytest.mark.model_utils
def test_fmt_brawl_side_size(side_size_0):
    assert model_utils.side_size(Format.BRAWL) == side_size_0


@pytest.mark.model_utils
def test_fmt_commander_side_size(side_size_0):
    assert model_utils.side_size(Format.COMMANDER) == side_size_0


@pytest.mark.model_utils
def test_fmt_duel_side_size(side_size_0):
    assert model_utils.side_size(Format.DUEL) == side_size_0


@pytest.mark.model_utils
def test_fmt_explorer_side_size(side_size_15):
    assert model_utils.side_size(Format.EXPLORER) == side_size_15


@pytest.mark.model_utils
def test_fmt_future_side_size(side_size_15):
    assert model_utils.side_size(Format.FUTURE) == side_size_15


@pytest.mark.model_utils
def test_fmt_gladiator_side_size(side_size_0):
    assert model_utils.side_size(Format.GLADIATOR) == side_size_0


@pytest.mark.model_utils
def test_fmt_historic_side_size(side_size_15):
    assert model_utils.side_size(Format.HISTORIC) == side_size_15


@pytest.mark.model_utils
def test_fmt_historicbrawl_side_size(side_size_0):
    assert model_utils.side_size(Format.HISTORICBRAWL) == side_size_0


@pytest.mark.model_utils
def test_fmt_legacy_side_size(side_size_15):
    assert model_utils.side_size(Format.LEGACY) == side_size_15


@pytest.mark.model_utils
def test_fmt_modern_side_size(side_size_15):
    assert model_utils.side_size(Format.MODERN) == side_size_15


@pytest.mark.model_utils
def test_fmt_oathbreaker_side_size(side_size_0):
    assert model_utils.side_size(Format.OATHBREAKER) == side_size_0


@pytest.mark.model_utils
def test_fmt_oldschool_side_size(side_size_15):
    assert model_utils.side_size(Format.OLDSCHOOL) == side_size_15


@pytest.mark.model_utils
def test_fmt_pauper_side_size(side_size_15):
    assert model_utils.side_size(Format.PAUPER) == side_size_15


@pytest.mark.model_utils
def test_fmt_paupercommander_side_size(side_size_0):
    assert model_utils.side_size(Format.PAUPERCOMMANDER) == side_size_0


@pytest.mark.model_utils
def test_fmt_penny_side_size(side_size_15):
    assert model_utils.side_size(Format.PENNY) == side_size_15


@pytest.mark.model_utils
def test_fmt_pioneer_side_size(side_size_15):
    assert model_utils.side_size(Format.PIONEER) == side_size_15


@pytest.mark.model_utils
def test_fmt_predh_side_size(side_size_0):
    assert model_utils.side_size(Format.PREDH) == side_size_0


@pytest.mark.model_utils
def test_fmt_premodern_side_size(side_size_15):
    assert model_utils.side_size(Format.PREMODERN) == side_size_15


@pytest.mark.model_utils
def test_fmt_standard_side_size(side_size_15):
    assert model_utils.side_size(Format.STANDARD) == side_size_15


@pytest.mark.model_utils
def test_fmt_vintage_side_size(side_size_15):
    assert model_utils.side_size(Format.VINTAGE) == side_size_15


@pytest.mark.model_utils
def test_fmt_limited_side_size(side_size_any):
    assert model_utils.side_size(Format.LIMITED) == side_size_any


@pytest.mark.model_utils
def test_fmt_none_side_size(side_size_any):
    assert model_utils.side_size(Format.NONE) == side_size_any


# endregion

# region Cmdr Size


@pytest.mark.model_utils
def test_fmt_alchemy_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.ALCHEMY) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_brawl_cmdr_size(cmdr_size_1):
    assert model_utils.cmdr_size(Format.BRAWL) == cmdr_size_1


@pytest.mark.model_utils
def test_fmt_commander_cmdr_size(cmdr_size_1_or_2):
    assert model_utils.cmdr_size(Format.COMMANDER) == cmdr_size_1_or_2


@pytest.mark.model_utils
def test_fmt_duel_cmdr_size(cmdr_size_1_or_2):
    assert model_utils.cmdr_size(Format.DUEL) == cmdr_size_1_or_2


@pytest.mark.model_utils
def test_fmt_explorer_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.EXPLORER) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_future_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.FUTURE) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_gladiator_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.GLADIATOR) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_historic_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.HISTORIC) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_historicbrawl_cmdr_size(cmdr_size_1):
    assert model_utils.cmdr_size(Format.HISTORICBRAWL) == cmdr_size_1


@pytest.mark.model_utils
def test_fmt_legacy_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.LEGACY) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_modern_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.MODERN) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_oathbreaker_cmdr_size(cmdr_size_2):
    assert model_utils.cmdr_size(Format.OATHBREAKER) == cmdr_size_2


@pytest.mark.model_utils
def test_fmt_oldschool_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.OLDSCHOOL) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_pauper_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.PAUPER) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_paupercommander_cmdr_size(cmdr_size_1):
    assert model_utils.cmdr_size(Format.PAUPERCOMMANDER) == cmdr_size_1


@pytest.mark.model_utils
def test_fmt_penny_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.PENNY) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_pioneer_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.PIONEER) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_predh_cmdr_size(cmdr_size_1):
    assert model_utils.cmdr_size(Format.PREDH) == cmdr_size_1


@pytest.mark.model_utils
def test_fmt_premodern_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.PREMODERN) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_standard_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.STANDARD) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_vintage_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.VINTAGE) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_limited_cmdr_size(cmdr_size_0):
    assert model_utils.cmdr_size(Format.LIMITED) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_none_cmdr_size(cmdr_size_any):
    assert model_utils.cmdr_size(Format.NONE) == cmdr_size_any


# endregion

# endregion

# endregion
