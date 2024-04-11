from unittest.mock import MagicMock, patch

import pytest
import scooze.api.bulkdata as bulk_api
from scooze.catalogs import ScryfallBulkFile
from scooze.models.card import CardModel


@pytest.fixture(scope="module")
def file_type() -> ScryfallBulkFile:
    return ScryfallBulkFile.DEFAULT


@pytest.fixture(scope="module")
def bulk_file_dir() -> str:
    return "./data/test"


class TestBulkDataWithEmptyDatabase:
    @pytest.fixture(scope="class", autouse=True)
    async def clean_db(self):
        yield
        await CardModel.delete_all()

    @patch("scooze.api.bulkdata.open")
    async def test_load_card_file_bad_no_download(
        self,
        mock_open: MagicMock,
        file_type: ScryfallBulkFile,
        bulk_file_dir: str,
    ):
        mock_open.side_effect = FileNotFoundError
        with pytest.raises(FileNotFoundError):
            await bulk_api.load_card_file(file_type=file_type, bulk_file_dir=bulk_file_dir)
