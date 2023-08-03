from sys import maxsize
from typing import Tuple

import pytest
import scooze.models.utils as model_utils
from scooze.enums import Format

# region Fixtures

# region Formats


@pytest.fixture
def fmt_alchemy() -> Format:
    return Format.ALCHEMY


@pytest.fixture
def fmt_brawl() -> Format:
    return Format.BRAWL


@pytest.fixture
def fmt_commander() -> Format:
    return Format.COMMANDER


@pytest.fixture
def fmt_duel() -> Format:
    return Format.DUEL


@pytest.fixture
def fmt_explorer() -> Format:
    return Format.EXPLORER


@pytest.fixture
def fmt_future() -> Format:
    return Format.FUTURE


@pytest.fixture
def fmt_gladiator() -> Format:
    return Format.GLADIATOR


@pytest.fixture
def fmt_historic() -> Format:
    return Format.HISTORIC


@pytest.fixture
def fmt_historicbrawl() -> Format:
    return Format.HISTORICBRAWL


@pytest.fixture
def fmt_legacy() -> Format:
    return Format.LEGACY


@pytest.fixture
def fmt_modern() -> Format:
    return Format.MODERN


@pytest.fixture
def fmt_oathbreaker() -> Format:
    return Format.OATHBREAKER


@pytest.fixture
def fmt_oldschool() -> Format:
    return Format.OLDSCHOOL


@pytest.fixture
def fmt_pauper() -> Format:
    return Format.PAUPER


@pytest.fixture
def fmt_paupercommander() -> Format:
    return Format.PAUPERCOMMANDER


@pytest.fixture
def fmt_penny() -> Format:
    return Format.PENNY


@pytest.fixture
def fmt_pioneer() -> Format:
    return Format.PIONEER


@pytest.fixture
def fmt_predh() -> Format:
    return Format.PREDH


@pytest.fixture
def fmt_premodern() -> Format:
    return Format.PREMODERN


@pytest.fixture
def fmt_standard() -> Format:
    return Format.STANDARD


@pytest.fixture
def fmt_vintage() -> Format:
    return Format.VINTAGE


# non-Scryfall formats


@pytest.fixture
def fmt_limited() -> Format:
    return Format.LIMITED


@pytest.fixture
def fmt_none() -> Format:
    return Format.NONE


# endregion

# region Format Deck Size

# region Main Size


@pytest.fixture
def main_size_40() -> Tuple[int, int]:
    return (40, maxsize)


@pytest.fixture
def main_size_58() -> Tuple[int, int]:
    return (58, 58)


@pytest.fixture
def main_size_60() -> Tuple[int, int]:
    return (60, maxsize)


@pytest.fixture
def main_size_99() -> Tuple[int, int]:
    return (99, 99)


@pytest.fixture
def main_size_100() -> Tuple[int, int]:
    return (100, 100)


@pytest.fixture
def main_size_any() -> Tuple[int, int]:
    return (0, maxsize)


# endregion

# region Side Size


@pytest.fixture
def side_size_0() -> Tuple[int, int]:
    return (0, 0)


@pytest.fixture
def side_size_1() -> Tuple[int, int]:
    return (1, 1)


@pytest.fixture
def side_size_2() -> Tuple[int, int]:
    return (2, 2)


@pytest.fixture
def side_size_15() -> Tuple[int, int]:
    return (0, 15)


@pytest.fixture
def side_size_any() -> Tuple[int, int]:
    return (0, maxsize)


# endregion

# endregion

# endregion


# region Test Format Deck Size

# region Main Size


@pytest.mark.format_size
def test_fmt_alchemy_size_main(fmt_alchemy, main_size_60):
    assert model_utils.main_size(fmt_alchemy) == main_size_60


@pytest.mark.format_size
def test_fmt_brawl_size_main(fmt_brawl, main_size_99):
    assert model_utils.main_size(fmt_brawl) == main_size_99


@pytest.mark.format_size
def test_fmt_commander_size_main(fmt_commander, main_size_99):
    assert model_utils.main_size(fmt_commander) == main_size_99


@pytest.mark.format_size
def test_fmt_duel_size_main(fmt_duel, main_size_99):
    assert model_utils.main_size(fmt_duel) == main_size_99


@pytest.mark.format_size
def test_fmt_explorer_size_main(fmt_explorer, main_size_60):
    assert model_utils.main_size(fmt_explorer) == main_size_60


@pytest.mark.format_size
def test_fmt_future_size_main(fmt_future, main_size_60):
    assert model_utils.main_size(fmt_future) == main_size_60


@pytest.mark.format_size
def test_fmt_gladiator_size_main(fmt_gladiator, main_size_100):
    assert model_utils.main_size(fmt_gladiator) == main_size_100


@pytest.mark.format_size
def test_fmt_historic_size_main(fmt_historic, main_size_60):
    assert model_utils.main_size(fmt_historic) == main_size_60


@pytest.mark.format_size
def test_fmt_historicbrawl_size_main(fmt_historicbrawl, main_size_99):
    assert model_utils.main_size(fmt_historicbrawl) == main_size_99


@pytest.mark.format_size
def test_fmt_legacy_size_main(fmt_legacy, main_size_60):
    assert model_utils.main_size(fmt_legacy) == main_size_60


@pytest.mark.format_size
def test_fmt_modern_size_main(fmt_modern, main_size_60):
    assert model_utils.main_size(fmt_modern) == main_size_60


@pytest.mark.format_size
def test_fmt_oathbreaker_size_main(fmt_oathbreaker, main_size_58):
    assert model_utils.main_size(fmt_oathbreaker) == main_size_58


@pytest.mark.format_size
def test_fmt_oldschool_size_main(fmt_oldschool, main_size_60):
    assert model_utils.main_size(fmt_oldschool) == main_size_60


@pytest.mark.format_size
def test_fmt_pauper_size_main(fmt_pauper, main_size_60):
    assert model_utils.main_size(fmt_pauper) == main_size_60


@pytest.mark.format_size
def test_fmt_paupercommander_size_main(fmt_paupercommander, main_size_99):
    assert model_utils.main_size(fmt_paupercommander) == main_size_99


@pytest.mark.format_size
def test_fmt_penny_size_main(fmt_penny, main_size_60):
    assert model_utils.main_size(fmt_penny) == main_size_60


@pytest.mark.format_size
def test_fmt_pioneer_size_main(fmt_pioneer, main_size_60):
    assert model_utils.main_size(fmt_pioneer) == main_size_60


@pytest.mark.format_size
def test_fmt_predh_size_main(fmt_predh, main_size_99):
    assert model_utils.main_size(fmt_predh) == main_size_99


@pytest.mark.format_size
def test_fmt_premodern_size_main(fmt_premodern, main_size_60):
    assert model_utils.main_size(fmt_premodern) == main_size_60


@pytest.mark.format_size
def test_fmt_standard_size_main(fmt_standard, main_size_60):
    assert model_utils.main_size(fmt_standard) == main_size_60


@pytest.mark.format_size
def test_fmt_vintage_size_main(fmt_vintage, main_size_60):
    assert model_utils.main_size(fmt_vintage) == main_size_60


@pytest.mark.format_size
def test_fmt_limited_size_main(fmt_limited, main_size_40):
    assert model_utils.main_size(fmt_limited) == main_size_40


@pytest.mark.format_size
def test_fmt_none_size_main(fmt_none, main_size_any):
    assert model_utils.main_size(fmt_none) == main_size_any


# endregion

# region Side Size


@pytest.mark.format_size
def test_fmt_alchemy_size_side(fmt_alchemy, side_size_15):
    assert model_utils.side_size(fmt_alchemy) == side_size_15


@pytest.mark.format_size
def test_fmt_brawl_size_side(fmt_brawl, side_size_1):
    assert model_utils.side_size(fmt_brawl) == side_size_1


@pytest.mark.format_size
def test_fmt_commander_size_side(fmt_commander, side_size_1):
    assert model_utils.side_size(fmt_commander) == side_size_1


@pytest.mark.format_size
def test_fmt_duel_size_side(fmt_duel, side_size_1):
    assert model_utils.side_size(fmt_duel) == side_size_1


@pytest.mark.format_size
def test_fmt_explorer_size_side(fmt_explorer, side_size_15):
    assert model_utils.side_size(fmt_explorer) == side_size_15


@pytest.mark.format_size
def test_fmt_future_size_side(fmt_future, side_size_15):
    assert model_utils.side_size(fmt_future) == side_size_15


@pytest.mark.format_size
def test_fmt_gladiator_size_side(fmt_gladiator, side_size_0):
    assert model_utils.side_size(fmt_gladiator) == side_size_0


@pytest.mark.format_size
def test_fmt_historic_size_side(fmt_historic, side_size_15):
    assert model_utils.side_size(fmt_historic) == side_size_15


@pytest.mark.format_size
def test_fmt_historicbrawl_size_side(fmt_historicbrawl, side_size_1):
    assert model_utils.side_size(fmt_historicbrawl) == side_size_1


@pytest.mark.format_size
def test_fmt_legacy_size_side(fmt_legacy, side_size_15):
    assert model_utils.side_size(fmt_legacy) == side_size_15


@pytest.mark.format_size
def test_fmt_modern_size_side(fmt_modern, side_size_15):
    assert model_utils.side_size(fmt_modern) == side_size_15


@pytest.mark.format_size
def test_fmt_oathbreaker_size_side(fmt_oathbreaker, side_size_2):
    assert model_utils.side_size(fmt_oathbreaker) == side_size_2


@pytest.mark.format_size
def test_fmt_oldschool_size_side(fmt_oldschool, side_size_15):
    assert model_utils.side_size(fmt_oldschool) == side_size_15


@pytest.mark.format_size
def test_fmt_pauper_size_side(fmt_pauper, side_size_15):
    assert model_utils.side_size(fmt_pauper) == side_size_15


@pytest.mark.format_size
def test_fmt_paupercommander_size_side(fmt_paupercommander, side_size_1):
    assert model_utils.side_size(fmt_paupercommander) == side_size_1


@pytest.mark.format_size
def test_fmt_penny_size_side(fmt_penny, side_size_15):
    assert model_utils.side_size(fmt_penny) == side_size_15


@pytest.mark.format_size
def test_fmt_pioneer_size_side(fmt_pioneer, side_size_15):
    assert model_utils.side_size(fmt_pioneer) == side_size_15


@pytest.mark.format_size
def test_fmt_predh_size_side(fmt_predh, side_size_1):
    assert model_utils.side_size(fmt_predh) == side_size_1


@pytest.mark.format_size
def test_fmt_premodern_size_side(fmt_premodern, side_size_15):
    assert model_utils.side_size(fmt_premodern) == side_size_15


@pytest.mark.format_size
def test_fmt_standard_size_side(fmt_standard, side_size_15):
    assert model_utils.side_size(fmt_standard) == side_size_15


@pytest.mark.format_size
def test_fmt_vintage_size_side(fmt_vintage, side_size_15):
    assert model_utils.side_size(fmt_vintage) == side_size_15


@pytest.mark.format_size
def test_fmt_limited_size_side(fmt_limited, side_size_any):
    assert model_utils.side_size(fmt_limited) == side_size_any


@pytest.mark.format_size
def test_fmt_none_size_side(fmt_none, side_size_any):
    assert model_utils.side_size(fmt_none) == side_size_any


# endregion

# endregion
