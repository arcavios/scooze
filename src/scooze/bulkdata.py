import os

import requests
from scooze.catalogs import ScryfallBulkFile
from scooze.utils import DEFAULT_BULK_FILE_DIR

SCRYFALL_BULK_INFO_ENDPOINT = "https://api.scryfall.com/bulk-data"


def download_bulk_data_file(
    uri: str,
    bulk_file_type: ScryfallBulkFile | None = None,
    bulk_file_dir: str = DEFAULT_BULK_FILE_DIR,
) -> None:
    """
    Download a single bulk data file from Scryfall.

    Args:
        uri: Location of bulk data file (generally found from bulk info
          endpoint).
        bulk_file_type: Type of bulk file, used to set filename.
        bulk_file_dir: Directory to save bulk files. Defaults to `./data/bulk` if
          not specified.

    Raises:
        HTTPError: If request for bulk file not successful.
    """

    # TODO(#74): flag for check vs existing file; don't overwrite with same file or older version
    with requests.get(uri, stream=True) as r:
        r.raise_for_status()
        os.makedirs(bulk_file_dir, exist_ok=True)
        file_name = f"{bulk_file_dir}/{bulk_file_type}.json"
        with open(file_name, "wb") as f:
            for chunk in r.iter_content(chunk_size=None):
                f.write(chunk)


def download_bulk_data_file_by_type(
    bulk_file_type: ScryfallBulkFile | None = None,
    bulk_file_dir: str = DEFAULT_BULK_FILE_DIR,
) -> None:
    """
    Get a bulk data file from Scryfall, specified by file type (from among ScryfallBulkFile).

    Args:
        bulk_file_type: Type of bulk file, used to set filename.
        bulk_file_dir: Directory to save bulk files. Defaults to `./data/bulk` if
          not specified.

    Raises:
        HTTPError: If request for bulk file not successful.
    """

    # get URI from Scryfall bulk endpoint

    with requests.get(SCRYFALL_BULK_INFO_ENDPOINT) as bulk_metadata_request:
        bulk_metadata_request.raise_for_status()
        bulk_metadata = bulk_metadata_request.json()["data"]
    bulk_files = {t["type"]: t["download_uri"] for t in bulk_metadata}
    if bulk_file_type not in bulk_files:
        return
    download_bulk_data_file(bulk_files[bulk_file_type], bulk_file_type, bulk_file_dir)


def download_all_bulk_data_files(
    bulk_file_dir: str = DEFAULT_BULK_FILE_DIR,
) -> None:
    """
    Download all supported Scryfall bulk data files to local filesystem.

    Args:
        bulk_file_dir: Directory to save bulk files. Defaults to `./data/bulk` if
          not specified.

    Raises:
        HTTPError: If request for bulk file not successful.
    """

    with requests.get(SCRYFALL_BULK_INFO_ENDPOINT) as bulk_metadata_request:
        bulk_metadata_request.raise_for_status()
        bulk_metadata = bulk_metadata_request.json()["data"]
    bulk_files = {t["type"]: t["download_uri"] for t in bulk_metadata}

    for bulk_type in ScryfallBulkFile.list():
        bulk_filename = bulk_files[bulk_type]
        download_bulk_data_file(
            uri=bulk_filename,
            bulk_file_type=bulk_type,
            bulk_file_dir=bulk_file_dir,
        )
