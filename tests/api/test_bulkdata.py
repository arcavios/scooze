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

    async def test_load_card_file(self, file_type: ScryfallBulkFile, bulk_file_dir: str, capfd):
        await bulk_api.load_card_file(file_type=file_type, bulk_file_dir=bulk_file_dir)
        captured = capfd.readouterr()
        expected = f"Loading {file_type} file into the database...\nLoaded 9 cards to the database.\n"
        assert captured.out == expected

    @patch("scooze.api.bulkdata.open")
    @patch("scooze.api.bulkdata.input")
    async def test_load_card_file_bad_no_download(
        self,
        mock_input: MagicMock,
        mock_open: MagicMock,
        file_type: ScryfallBulkFile,
        bulk_file_dir: str,
        capfd,
    ):
        mock_open.side_effect = FileNotFoundError
        mock_input.return_value = "N"
        await bulk_api.load_card_file(file_type=file_type, bulk_file_dir=bulk_file_dir)
        captured = capfd.readouterr()
        expected = f"Loading {file_type} file into the database...\n{bulk_file_dir}/{file_type}.json\nNo cards loaded into database.\n"
        assert captured.out == expected

    @patch("scooze.api.bulkdata.open")
    @patch("scooze.api.bulkdata.input")
    @patch("scooze.api.bulkdata.download_bulk_data_file_by_type")
    async def test_load_card_file_bad_with_download(
        self,
        mock_download: MagicMock,
        mock_input: MagicMock,
        mock_open_custom: MagicMock,
        file_type: ScryfallBulkFile,
        bulk_file_dir: str,
        capfd,
    ):
        # NOTE: Wrapping all of this test with the file open lets us use the actual
        # file we're testing with as the second side effect for the 'open' mock
        with open(f"{bulk_file_dir}/{file_type}.json", "rb") as test_file:
            mock_open_custom.return_value.__enter__.side_effect = [FileNotFoundError, test_file]
            mock_input.return_value = "Y"
            mock_download.return_value = None
            await bulk_api.load_card_file(file_type=file_type, bulk_file_dir=bulk_file_dir)
            captured = capfd.readouterr()
            expected = (
                f"Loading {file_type} file into the database...\n{bulk_file_dir}/{file_type}.json\n"
                f"Loading {file_type} file into the database...\nLoaded 9 cards to the database.\n"
            )
            assert captured.out == expected
