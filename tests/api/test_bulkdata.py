from unittest.mock import MagicMock, patch

import scooze.api.bulkdata as bulk_api
import pytest
from bson import ObjectId
from scooze.card import FullCard
from scooze.catalogs import ScryfallBulkFile
from scooze.utils import DEFAULT_BULK_FILE_DIR

@pytest.fixture(scope="module")
def file_type() -> str:
    return "bulk_test_cards"

@pytest.fixture(scope="module")
def bulk_file_dir() -> str:
    return "./data/test"


@patch("scooze.database.card.add_cards")
def test_load_card_file(mock_add: MagicMock, cards_full: list[FullCard], file_type, bulk_file_dir, capfd):
    ids = [ObjectId() for _ in cards_full]
    mock_add.return_value: list[ObjectId] = ids
    bulk_api.load_card_file(file_type=file_type, bulk_file_dir=bulk_file_dir)
    captured = capfd.readouterr()
    expected = f"Loading bulk_test_cards file into the database...\nLoaded {len(ids)} cards to the database.\n"
    assert captured.out == expected


@patch("scooze.database.card.add_cards")
def test_load_card_file_bad(mock_add: MagicMock, file_type, bulk_file_dir, capfd):
    mock_add.return_value = None
    bulk_api.load_card_file(file_type=file_type, bulk_file_dir=bulk_file_dir)
    captured = capfd.readouterr()
    expected = f"Loading bulk_test_cards file into the database...\nNo cards loaded into database.\n"
    assert captured.out == expected

def test_load_card_file_bad(capfd):
    # bulk_api.load_card_file(file_type="not real", bulk_file_dir="not real")
    # captured = capfd.readouterr()
    # expected = f"Loading bulk_test_cards file into the database...\nNo cards loaded into database.\n"
    # assert captured.out == expected
    # TODO: https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
