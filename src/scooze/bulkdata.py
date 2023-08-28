import os

import requests
from scooze.enums import ScryfallBulkFile

SCRYFALL_BULK_INFO_ENDPOINT = "https://api.scryfall.com/bulk-data"


def download_bulk_data_file(
    uri: str,
    bulk_file_type: ScryfallBulkFile | None = None,
    file_path: str = "data/bulk/",
) -> None:
    """
    Download a single bulk data file from Scryfall.
    Parameters:
        uri (str): Location of bulk data file (generally found from bulk info endpoint).
        bulk_file_type (ScryfallBulkFile): Type of bulk file, used to set filename.
        file_path (str): Directory to save bulk files. Defaults to `data/bulk/` if not specified.
    """
    # TODO(#74): flag for check vs existing file; don't overwrite with same file or older version
    with requests.get(uri, stream=True) as r:
        r.raise_for_status()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file_name = f"{file_path}{bulk_file_type}.json"
        with open(file_name, "wb") as f:
            for chunk in r.iter_content(chunk_size=None):
                f.write(chunk)


def download_all_bulk_data_files(
    file_path: str = "data/bulk/",
) -> None:
    """
    Download all supported Scryfall bulk data files to local filesystem.
    Parameters:
        file_path (str): Directory to save bulk files. Defaults to `data/bulk/` if not specified.
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
            file_path=file_path,
        )
