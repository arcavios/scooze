from unittest.mock import MagicMock, patch

import pytest
import scooze.api.bulkdata as bulk_api
from bson import ObjectId
from scooze.catalogs import ScryfallBulkFile


@pytest.fixture(scope="module")
def file_type() -> ScryfallBulkFile:
    return ScryfallBulkFile.DEFAULT


@pytest.fixture(scope="module")
def bulk_file_dir() -> str:
    return "./data/test"


@patch("scooze.database.card.add_cards")
def test_load_card_file(mock_add: MagicMock, cards_full, file_type, bulk_file_dir, asyncio_runner, capfd):
    ids = [ObjectId() for _ in cards_full]
    mock_add.return_value: list[ObjectId] = ids
    asyncio_runner.run(bulk_api.load_card_file(file_type=file_type, bulk_file_dir=bulk_file_dir))
    captured = capfd.readouterr()
    expected = f"Loading {file_type} file into the database...\nLoaded {len(ids)} cards to the database.\n"
    assert captured.out == expected


@patch("scooze.database.card.add_cards")
def test_load_card_file_bad(mock_add: MagicMock, file_type, bulk_file_dir, asyncio_runner, capfd):
    mock_add.return_value = None
    asyncio_runner.run(bulk_api.load_card_file(file_type=file_type, bulk_file_dir=bulk_file_dir))
    captured = capfd.readouterr()
    expected = f"Loading {file_type} file into the database...\nNo cards loaded into database.\n"
    assert captured.out == expected


def test_load_card_file_bad(capfd):
    # TODO(#147): test the load_card_file except block which contains an input() call
    # bulk_api.load_card_file(file_type="not real", bulk_file_dir="not real")
    # captured = capfd.readouterr()
    # expected = f"Loading bulk_test_cards file into the database...\nNo cards loaded into database.\n"
    # assert captured.out == expected
    # https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
    pass
