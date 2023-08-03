import scooze.models.utils as model_utils
from scooze.enums import Format
from typing import Tuple
from sys import maxsize
import pytest

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

# endregion

# region Side Size

# endregion

# endregion
