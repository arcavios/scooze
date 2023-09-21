from unittest.mock import MagicMock, patch

import scooze.api.bulkdata as bulk_api
from bson import ObjectId
from scooze.card import FullCard
from scooze.catalogs import ScryfallBulkFile
from scooze.utils import DEFAULT_BULK_FILE_DIR


@patch("scooze.database.card.add_cards")
def test_load_card_file(mock_add: MagicMock, cards_full: list[FullCard], capfd):
    ids = [ObjectId() for _ in cards_full]
    mock_add.return_value: list[ObjectId] = ids
    bulk_api.load_card_file(file_type="bulk_test_cards", bulk_file_dir="./data/test")
    captured = capfd.readouterr()
    expected = f"Loading bulk_test_cards file into the database...\nLoaded {len(ids)} cards to the database.\n"
    assert captured.out == expected


@patch("scooze.database.card.add_cards")
def test_load_card_file_bad(mock_add: MagicMock):
    mock_add.return_value = None
    # TODO: assert that bulk_api.load_card_file() prints "no cards loaded into database"
    pass


def test_load_card_file_error():
    # TODO: assert that bulk_api.looad_card_file("not a real file") raies error
    pass
