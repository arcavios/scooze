from sys import maxsize

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
def main_size_40() -> tuple[int, int]:
    return (40, maxsize)


@pytest.fixture
def main_size_58() -> tuple[int, int]:
    return (58, 58)


@pytest.fixture
def main_size_60() -> tuple[int, int]:
    return (60, maxsize)


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
def side_size_1() -> tuple[int, int]:
    return (1, 1)


@pytest.fixture
def side_size_2() -> tuple[int, int]:
    return (2, 2)


@pytest.fixture
def side_size_15() -> tuple[int, int]:
    return (0, 15)


@pytest.fixture
def side_size_any() -> tuple[int, int]:
    return (0, maxsize)


# endregion

# endregion

# endregion


# region Test Format Deck Size

# region Main Size


@pytest.mark.format_size
def test_fmt_alchemy_main_size(fmt_alchemy, main_size_60):
    assert model_utils.main_size(fmt_alchemy) == main_size_60


@pytest.mark.format_size
def test_fmt_brawl_main_size(fmt_brawl, main_size_99):
    assert model_utils.main_size(fmt_brawl) == main_size_99


@pytest.mark.format_size
def test_fmt_commander_main_size(fmt_commander, main_size_99):
    assert model_utils.main_size(fmt_commander) == main_size_99


@pytest.mark.format_size
def test_fmt_duel_main_size(fmt_duel, main_size_99):
    assert model_utils.main_size(fmt_duel) == main_size_99


@pytest.mark.format_size
def test_fmt_explorer_main_size(fmt_explorer, main_size_60):
    assert model_utils.main_size(fmt_explorer) == main_size_60


@pytest.mark.format_size
def test_fmt_future_main_size(fmt_future, main_size_60):
    assert model_utils.main_size(fmt_future) == main_size_60


@pytest.mark.format_size
def test_fmt_gladiator_main_size(fmt_gladiator, main_size_100):
    assert model_utils.main_size(fmt_gladiator) == main_size_100


@pytest.mark.format_size
def test_fmt_historic_main_size(fmt_historic, main_size_60):
    assert model_utils.main_size(fmt_historic) == main_size_60


@pytest.mark.format_size
def test_fmt_historicbrawl_main_size(fmt_historicbrawl, main_size_99):
    assert model_utils.main_size(fmt_historicbrawl) == main_size_99


@pytest.mark.format_size
def test_fmt_legacy_main_size(fmt_legacy, main_size_60):
    assert model_utils.main_size(fmt_legacy) == main_size_60


@pytest.mark.format_size
def test_fmt_modern_main_size(fmt_modern, main_size_60):
    assert model_utils.main_size(fmt_modern) == main_size_60


@pytest.mark.format_size
def test_fmt_oathbreaker_main_size(fmt_oathbreaker, main_size_58):
    assert model_utils.main_size(fmt_oathbreaker) == main_size_58


@pytest.mark.format_size
def test_fmt_oldschool_main_size(fmt_oldschool, main_size_60):
    assert model_utils.main_size(fmt_oldschool) == main_size_60


@pytest.mark.format_size
def test_fmt_pauper_main_size(fmt_pauper, main_size_60):
    assert model_utils.main_size(fmt_pauper) == main_size_60


@pytest.mark.format_size
def test_fmt_paupercommander_main_size(fmt_paupercommander, main_size_99):
    assert model_utils.main_size(fmt_paupercommander) == main_size_99


@pytest.mark.format_size
def test_fmt_penny_main_size(fmt_penny, main_size_60):
    assert model_utils.main_size(fmt_penny) == main_size_60


@pytest.mark.format_size
def test_fmt_pioneer_main_size(fmt_pioneer, main_size_60):
    assert model_utils.main_size(fmt_pioneer) == main_size_60


@pytest.mark.format_size
def test_fmt_predh_main_size(fmt_predh, main_size_99):
    assert model_utils.main_size(fmt_predh) == main_size_99


@pytest.mark.format_size
def test_fmt_premodern_main_size(fmt_premodern, main_size_60):
    assert model_utils.main_size(fmt_premodern) == main_size_60


@pytest.mark.format_size
def test_fmt_standard_main_size(fmt_standard, main_size_60):
    assert model_utils.main_size(fmt_standard) == main_size_60


@pytest.mark.format_size
def test_fmt_vintage_main_size(fmt_vintage, main_size_60):
    assert model_utils.main_size(fmt_vintage) == main_size_60


@pytest.mark.format_size
def test_fmt_limited_main_size(fmt_limited, main_size_40):
    assert model_utils.main_size(fmt_limited) == main_size_40


@pytest.mark.format_size
def test_fmt_none_main_size(fmt_none, main_size_any):
    assert model_utils.main_size(fmt_none) == main_size_any


# endregion

# region Side Size


@pytest.mark.format_size
def test_fmt_alchemy_side_size(fmt_alchemy, side_size_15):
    assert model_utils.side_size(fmt_alchemy) == side_size_15


@pytest.mark.format_size
def test_fmt_brawl_side_size(fmt_brawl, side_size_1):
    assert model_utils.side_size(fmt_brawl) == side_size_1


@pytest.mark.format_size
def test_fmt_commander_side_size(fmt_commander, side_size_1):
    assert model_utils.side_size(fmt_commander) == side_size_1


@pytest.mark.format_size
def test_fmt_duel_side_size(fmt_duel, side_size_1):
    assert model_utils.side_size(fmt_duel) == side_size_1


@pytest.mark.format_size
def test_fmt_explorer_side_size(fmt_explorer, side_size_15):
    assert model_utils.side_size(fmt_explorer) == side_size_15


@pytest.mark.format_size
def test_fmt_future_side_size(fmt_future, side_size_15):
    assert model_utils.side_size(fmt_future) == side_size_15


@pytest.mark.format_size
def test_fmt_gladiator_side_size(fmt_gladiator, side_size_0):
    assert model_utils.side_size(fmt_gladiator) == side_size_0


@pytest.mark.format_size
def test_fmt_historic_side_size(fmt_historic, side_size_15):
    assert model_utils.side_size(fmt_historic) == side_size_15


@pytest.mark.format_size
def test_fmt_historicbrawl_side_size(fmt_historicbrawl, side_size_1):
    assert model_utils.side_size(fmt_historicbrawl) == side_size_1


@pytest.mark.format_size
def test_fmt_legacy_side_size(fmt_legacy, side_size_15):
    assert model_utils.side_size(fmt_legacy) == side_size_15


@pytest.mark.format_size
def test_fmt_modern_side_size(fmt_modern, side_size_15):
    assert model_utils.side_size(fmt_modern) == side_size_15


@pytest.mark.format_size
def test_fmt_oathbreaker_side_size(fmt_oathbreaker, side_size_2):
    assert model_utils.side_size(fmt_oathbreaker) == side_size_2


@pytest.mark.format_size
def test_fmt_oldschool_side_size(fmt_oldschool, side_size_15):
    assert model_utils.side_size(fmt_oldschool) == side_size_15


@pytest.mark.format_size
def test_fmt_pauper_side_size(fmt_pauper, side_size_15):
    assert model_utils.side_size(fmt_pauper) == side_size_15


@pytest.mark.format_size
def test_fmt_paupercommander_side_size(fmt_paupercommander, side_size_1):
    assert model_utils.side_size(fmt_paupercommander) == side_size_1


@pytest.mark.format_size
def test_fmt_penny_side_size(fmt_penny, side_size_15):
    assert model_utils.side_size(fmt_penny) == side_size_15


@pytest.mark.format_size
def test_fmt_pioneer_side_size(fmt_pioneer, side_size_15):
    assert model_utils.side_size(fmt_pioneer) == side_size_15


@pytest.mark.format_size
def test_fmt_predh_side_size(fmt_predh, side_size_1):
    assert model_utils.side_size(fmt_predh) == side_size_1


@pytest.mark.format_size
def test_fmt_premodern_side_size(fmt_premodern, side_size_15):
    assert model_utils.side_size(fmt_premodern) == side_size_15


@pytest.mark.format_size
def test_fmt_standard_side_size(fmt_standard, side_size_15):
    assert model_utils.side_size(fmt_standard) == side_size_15


@pytest.mark.format_size
def test_fmt_vintage_side_size(fmt_vintage, side_size_15):
    assert model_utils.side_size(fmt_vintage) == side_size_15


@pytest.mark.format_size
def test_fmt_limited_side_size(fmt_limited, side_size_any):
    assert model_utils.side_size(fmt_limited) == side_size_any


@pytest.mark.format_size
def test_fmt_none_side_size(fmt_none, side_size_any):
    assert model_utils.side_size(fmt_none) == side_size_any


# endregion

# endregion
