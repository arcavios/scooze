from sys import maxsize

import pytest
import scooze.models.utils as model_utils
import scooze.utils as utils
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
        """Annihilating Glare: (0, 1)\n"""
        """Blackcleave Cliffs: (4, 2)\n"""
        """Unlucky Witness: (3, 4)\n"""
        """Urborg, Tomb of Yawgmoth: (0, 1)\n"""
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
def test_fmt_alchemy_main_size(format_alchemy, main_size_60):
    assert model_utils.main_size(format_alchemy) == main_size_60


@pytest.mark.model_utils
def test_fmt_brawl_main_size(format_brawl, main_size_99):
    assert model_utils.main_size(format_brawl) == main_size_99


@pytest.mark.model_utils
def test_fmt_commander_main_size(format_commander, main_size_98):
    assert model_utils.main_size(format_commander) == main_size_98


@pytest.mark.model_utils
def test_fmt_duel_main_size(format_duel, main_size_98):
    assert model_utils.main_size(format_duel) == main_size_98


@pytest.mark.model_utils
def test_fmt_explorer_main_size(format_explorer, main_size_60):
    assert model_utils.main_size(format_explorer) == main_size_60


@pytest.mark.model_utils
def test_fmt_future_main_size(format_future, main_size_60):
    assert model_utils.main_size(format_future) == main_size_60


@pytest.mark.model_utils
def test_fmt_gladiator_main_size(format_gladiator, main_size_100):
    assert model_utils.main_size(format_gladiator) == main_size_100


@pytest.mark.model_utils
def test_fmt_historic_main_size(format_historic, main_size_60):
    assert model_utils.main_size(format_historic) == main_size_60


@pytest.mark.model_utils
def test_fmt_historicbrawl_main_size(format_historicbrawl, main_size_99):
    assert model_utils.main_size(format_historicbrawl) == main_size_99


@pytest.mark.model_utils
def test_fmt_legacy_main_size(format_legacy, main_size_60):
    assert model_utils.main_size(format_legacy) == main_size_60


@pytest.mark.model_utils
def test_fmt_modern_main_size(format_modern, main_size_60):
    assert model_utils.main_size(format_modern) == main_size_60


@pytest.mark.model_utils
def test_fmt_oathbreaker_main_size(format_oathbreaker, main_size_58):
    assert model_utils.main_size(format_oathbreaker) == main_size_58


@pytest.mark.model_utils
def test_fmt_oldschool_main_size(format_oldschool, main_size_60):
    assert model_utils.main_size(format_oldschool) == main_size_60


@pytest.mark.model_utils
def test_fmt_pauper_main_size(format_pauper, main_size_60):
    assert model_utils.main_size(format_pauper) == main_size_60


@pytest.mark.model_utils
def test_fmt_paupercommander_main_size(format_paupercommander, main_size_99):
    assert model_utils.main_size(format_paupercommander) == main_size_99


@pytest.mark.model_utils
def test_fmt_penny_main_size(format_penny, main_size_60):
    assert model_utils.main_size(format_penny) == main_size_60


@pytest.mark.model_utils
def test_fmt_pioneer_main_size(format_pioneer, main_size_60):
    assert model_utils.main_size(format_pioneer) == main_size_60


@pytest.mark.model_utils
def test_fmt_predh_main_size(format_predh, main_size_99):
    assert model_utils.main_size(format_predh) == main_size_99


@pytest.mark.model_utils
def test_fmt_premodern_main_size(format_premodern, main_size_60):
    assert model_utils.main_size(format_premodern) == main_size_60


@pytest.mark.model_utils
def test_fmt_standard_main_size(format_standard, main_size_60):
    assert model_utils.main_size(format_standard) == main_size_60


@pytest.mark.model_utils
def test_fmt_vintage_main_size(format_vintage, main_size_60):
    assert model_utils.main_size(format_vintage) == main_size_60


@pytest.mark.model_utils
def test_fmt_limited_main_size(format_limited, main_size_40):
    assert model_utils.main_size(format_limited) == main_size_40


@pytest.mark.model_utils
def test_fmt_none_main_size(format_none, main_size_any):
    assert model_utils.main_size(format_none) == main_size_any


# endregion

# region Side Size


@pytest.mark.model_utils
def test_fmt_alchemy_side_size(format_alchemy, side_size_15):
    assert model_utils.side_size(format_alchemy) == side_size_15


@pytest.mark.model_utils
def test_fmt_brawl_side_size(format_brawl, side_size_0):
    assert model_utils.side_size(format_brawl) == side_size_0


@pytest.mark.model_utils
def test_fmt_commander_side_size(format_commander, side_size_0):
    assert model_utils.side_size(format_commander) == side_size_0


@pytest.mark.model_utils
def test_fmt_duel_side_size(format_duel, side_size_0):
    assert model_utils.side_size(format_duel) == side_size_0


@pytest.mark.model_utils
def test_fmt_explorer_side_size(format_explorer, side_size_15):
    assert model_utils.side_size(format_explorer) == side_size_15


@pytest.mark.model_utils
def test_fmt_future_side_size(format_future, side_size_15):
    assert model_utils.side_size(format_future) == side_size_15


@pytest.mark.model_utils
def test_fmt_gladiator_side_size(format_gladiator, side_size_0):
    assert model_utils.side_size(format_gladiator) == side_size_0


@pytest.mark.model_utils
def test_fmt_historic_side_size(format_historic, side_size_15):
    assert model_utils.side_size(format_historic) == side_size_15


@pytest.mark.model_utils
def test_fmt_historicbrawl_side_size(format_historicbrawl, side_size_0):
    assert model_utils.side_size(format_historicbrawl) == side_size_0


@pytest.mark.model_utils
def test_fmt_legacy_side_size(format_legacy, side_size_15):
    assert model_utils.side_size(format_legacy) == side_size_15


@pytest.mark.model_utils
def test_fmt_modern_side_size(format_modern, side_size_15):
    assert model_utils.side_size(format_modern) == side_size_15


@pytest.mark.model_utils
def test_fmt_oathbreaker_side_size(format_oathbreaker, side_size_0):
    assert model_utils.side_size(format_oathbreaker) == side_size_0


@pytest.mark.model_utils
def test_fmt_oldschool_side_size(format_oldschool, side_size_15):
    assert model_utils.side_size(format_oldschool) == side_size_15


@pytest.mark.model_utils
def test_fmt_pauper_side_size(format_pauper, side_size_15):
    assert model_utils.side_size(format_pauper) == side_size_15


@pytest.mark.model_utils
def test_fmt_paupercommander_side_size(format_paupercommander, side_size_0):
    assert model_utils.side_size(format_paupercommander) == side_size_0


@pytest.mark.model_utils
def test_fmt_penny_side_size(format_penny, side_size_15):
    assert model_utils.side_size(format_penny) == side_size_15


@pytest.mark.model_utils
def test_fmt_pioneer_side_size(format_pioneer, side_size_15):
    assert model_utils.side_size(format_pioneer) == side_size_15


@pytest.mark.model_utils
def test_fmt_predh_side_size(format_predh, side_size_0):
    assert model_utils.side_size(format_predh) == side_size_0


@pytest.mark.model_utils
def test_fmt_premodern_side_size(format_premodern, side_size_15):
    assert model_utils.side_size(format_premodern) == side_size_15


@pytest.mark.model_utils
def test_fmt_standard_side_size(format_standard, side_size_15):
    assert model_utils.side_size(format_standard) == side_size_15


@pytest.mark.model_utils
def test_fmt_vintage_side_size(format_vintage, side_size_15):
    assert model_utils.side_size(format_vintage) == side_size_15


@pytest.mark.model_utils
def test_fmt_limited_side_size(format_limited, side_size_any):
    assert model_utils.side_size(format_limited) == side_size_any


@pytest.mark.model_utils
def test_fmt_none_side_size(format_none, side_size_any):
    assert model_utils.side_size(format_none) == side_size_any


# endregion

# region Cmdr Size


@pytest.mark.model_utils
def test_fmt_alchemy_cmdr_size(format_alchemy, cmdr_size_0):
    assert model_utils.cmdr_size(format_alchemy) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_brawl_cmdr_size(format_brawl, cmdr_size_1):
    assert model_utils.cmdr_size(format_brawl) == cmdr_size_1


@pytest.mark.model_utils
def test_fmt_commander_cmdr_size(format_commander, cmdr_size_1_or_2):
    assert model_utils.cmdr_size(format_commander) == cmdr_size_1_or_2


@pytest.mark.model_utils
def test_fmt_duel_cmdr_size(format_duel, cmdr_size_1_or_2):
    assert model_utils.cmdr_size(format_duel) == cmdr_size_1_or_2


@pytest.mark.model_utils
def test_fmt_explorer_cmdr_size(format_explorer, cmdr_size_0):
    assert model_utils.cmdr_size(format_explorer) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_future_cmdr_size(format_future, cmdr_size_0):
    assert model_utils.cmdr_size(format_future) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_gladiator_cmdr_size(format_gladiator, cmdr_size_0):
    assert model_utils.cmdr_size(format_gladiator) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_historic_cmdr_size(format_historic, cmdr_size_0):
    assert model_utils.cmdr_size(format_historic) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_historicbrawl_cmdr_size(format_historicbrawl, cmdr_size_1):
    assert model_utils.cmdr_size(format_historicbrawl) == cmdr_size_1


@pytest.mark.model_utils
def test_fmt_legacy_cmdr_size(format_legacy, cmdr_size_0):
    assert model_utils.cmdr_size(format_legacy) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_modern_cmdr_size(format_modern, cmdr_size_0):
    assert model_utils.cmdr_size(format_modern) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_oathbreaker_cmdr_size(format_oathbreaker, cmdr_size_2):
    assert model_utils.cmdr_size(format_oathbreaker) == cmdr_size_2


@pytest.mark.model_utils
def test_fmt_oldschool_cmdr_size(format_oldschool, cmdr_size_0):
    assert model_utils.cmdr_size(format_oldschool) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_pauper_cmdr_size(format_pauper, cmdr_size_0):
    assert model_utils.cmdr_size(format_pauper) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_paupercommander_cmdr_size(format_paupercommander, cmdr_size_1):
    assert model_utils.cmdr_size(format_paupercommander) == cmdr_size_1


@pytest.mark.model_utils
def test_fmt_penny_cmdr_size(format_penny, cmdr_size_0):
    assert model_utils.cmdr_size(format_penny) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_pioneer_cmdr_size(format_pioneer, cmdr_size_0):
    assert model_utils.cmdr_size(format_pioneer) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_predh_cmdr_size(format_predh, cmdr_size_1):
    assert model_utils.cmdr_size(format_predh) == cmdr_size_1


@pytest.mark.model_utils
def test_fmt_premodern_cmdr_size(format_premodern, cmdr_size_0):
    assert model_utils.cmdr_size(format_premodern) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_standard_cmdr_size(format_standard, cmdr_size_0):
    assert model_utils.cmdr_size(format_standard) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_vintage_cmdr_size(format_vintage, cmdr_size_0):
    assert model_utils.cmdr_size(format_vintage) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_limited_cmdr_size(format_limited, cmdr_size_0):
    assert model_utils.cmdr_size(format_limited) == cmdr_size_0


@pytest.mark.model_utils
def test_fmt_none_cmdr_size(format_none, cmdr_size_any):
    assert model_utils.cmdr_size(format_none) == cmdr_size_any


# endregion

# endregion

# endregion
